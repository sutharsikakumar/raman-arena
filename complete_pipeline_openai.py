import sys
import os
import json
from pathlib import Path
import numpy as np
from scipy import signal
from scipy.ndimage import median_filter as scipy_median_filter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import openai


env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

# Configure OpenAI with API key from environment
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found in environment or .env file.")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

try:
    import pywt
    PYWT_AVAILABLE = True
except ImportError:
    PYWT_AVAILABLE = False

# Model name — change to preferred OpenAI model
MODEL_NAME = os.environ.get('OPENAI_MODEL', 'gpt-4o')


def load_spectrum(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        data = json.load(f)
    for key in ['x', 'y']:
        if key not in data:
            raise ValueError(f"Missing required key '{key}'")
    x = np.array(data['x'], dtype=float)
    y = np.array(data['y'], dtype=float)
    if len(x) == 0 or len(y) == 0:
        raise ValueError("Empty spectrum arrays")
    if len(x) != len(y):
        raise ValueError(f"Length mismatch: x={len(x)}, y={len(y)}")
    return {
        'spectrum_id': data.get('spectrum_id', 'unknown'),
        'x_unit': data.get('x_unit', 'cm^-1'),
        'y_unit': data.get('y_unit', 'counts'),
        'x': x,
        'y': y
    }


def compute_diagnostics(x: np.ndarray, y: np.ndarray) -> dict:
    diff = np.diff(y)
    noise_std = np.std(diff) / np.sqrt(2)
    signal_range = np.max(y) - np.min(y)
    snr = signal_range / (noise_std + 1e-10)

    if snr > 100:
        noise_level = "low"
    elif snr > 20:
        noise_level = "moderate"
    else:
        noise_level = "high"

    window = min(11, len(y) // 10 * 2 + 1)
    if window < 3:
        window = 3
    local_median = scipy_median_filter(y, size=window)
    spike_threshold = 5 * noise_std
    spike_noise = bool(np.any(np.abs(y - local_median) > spike_threshold))
    spike_score = float(np.sum(np.abs(y - local_median) > spike_threshold) / len(y))

    x_norm = np.linspace(0, 1, len(x))
    poly_coeffs = np.polyfit(x_norm, y, 3)
    baseline_fit = np.polyval(poly_coeffs, x_norm)
    baseline_variation = np.std(baseline_fit)
    baseline_drift = bool(baseline_variation > 0.1 * signal_range)
    baseline_drift_score = float(baseline_variation / (signal_range + 1e-10))

    rough_peaks, _ = signal.find_peaks(y, height=np.percentile(y, 75), distance=5)
    peak_density_ratio = len(rough_peaks) / (len(x) / 100)
    peak_density = "low" if peak_density_ratio < 1 else ("medium" if peak_density_ratio < 3 else "high")

    avg_width = 0.0
    if len(rough_peaks) > 0:
        widths = signal.peak_widths(y, rough_peaks, rel_height=0.5)[0]
        avg_width = float(np.mean(widths))
    peak_sharpness = "sharp" if avg_width < 10 else ("moderate" if avg_width < 30 else "broad")

    x_range = float(x[-1] - x[0]) if len(x) > 1 else 0.0

    return {
        'num_points': int(len(x)),
        'x_range': x_range,
        'x_resolution_cm-1': float(x_range / len(x)) if len(x) > 1 else 0.0,
        'y_min': float(np.min(y)),
        'y_max': float(np.max(y)),
        'snr_estimate': float(snr),
        'noise_level': noise_level,
        'spike_noise': spike_noise,
        'spike_noise_score': spike_score,
        'baseline_drift': baseline_drift,
        'baseline_drift_score': baseline_drift_score,
        'peak_density': peak_density,
        'peak_sharpness': peak_sharpness,
        'num_rough_peaks': int(len(rough_peaks))
    }


def call_llm_for_denoising(diagnostics: dict) -> dict:
    prompt = f"""You are an expert in Raman spectroscopy signal processing.
Analyze these spectrum diagnostics and decide the optimal denoising strategy.

Diagnostics:
{json.dumps(diagnostics, indent=2)}

Available methods: savitzky_golay, median_filter, wavelet, moving_average, none

Consider:
- noise_level: high noise needs stronger smoothing
- spike_noise: True suggests median_filter
- peak_sharpness: sharp peaks need shape-preserving methods (savitzky_golay)
- baseline_drift: affects method selection
- peak_density: dense peaks need narrower windows

Return ONLY valid JSON, no markdown:
{{
  "diagnostics": {{
    "noise_level": "{diagnostics.get('noise_level', 'moderate')}",
    "spike_noise": {str(diagnostics.get('spike_noise', False)).lower()},
    "baseline_drift": {str(diagnostics.get('baseline_drift', False)).lower()},
    "peak_density": "{diagnostics.get('peak_density', 'low')}"
  }},
  "denoise_method": "savitzky_golay",
  "parameters": {{"window_length": 21, "polyorder": 3}},
  "reason": "Brief explanation",
  "analysis_steps": [
    "SNR observation",
    "Noise type assessment",
    "Method selection rationale",
    "Parameter justification"
  ]
}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1024
    )
    raw = response.choices[0].message.content.strip()

    if raw.startswith('```'):
        lines = raw.split('\n')
        raw = '\n'.join(lines[1:-1])

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = None

    valid_methods = ['savitzky_golay', 'median_filter', 'wavelet', 'moving_average', 'none']
    if result is None or result.get('denoise_method') not in valid_methods:
        result = {
            "diagnostics": {
                "noise_level": diagnostics.get('noise_level', 'moderate'),
                "spike_noise": diagnostics.get('spike_noise', False),
                "baseline_drift": diagnostics.get('baseline_drift', False),
                "peak_density": diagnostics.get('peak_density', 'low')
            },
            "denoise_method": "savitzky_golay",
            "parameters": {"window_length": 21, "polyorder": 3},
            "reason": "Fallback: Savitzky-Golay preserves peak shapes while smoothing moderate noise.",
            "analysis_steps": ["Fallback to default denoising due to invalid LLM response."]
        }

    return result


def apply_denoising(y: np.ndarray, method: str, parameters: dict) -> np.ndarray:
    if method == 'none':
        return y.copy()

    elif method == 'savitzky_golay':
        wl = parameters.get('window_length', 21)
        po = parameters.get('polyorder', 3)
        if wl % 2 == 0:
            wl += 1
        if wl <= po:
            wl = po + 2
            if wl % 2 == 0:
                wl += 1
        wl = min(wl, len(y) if len(y) % 2 == 1 else len(y) - 1)
        return signal.savgol_filter(y, window_length=wl, polyorder=po)

    elif method == 'median_filter':
        ks = parameters.get('kernel_size', 5)
        if ks % 2 == 0:
            ks += 1
        ks = max(3, min(ks, len(y) // 2 * 2 - 1))
        return scipy_median_filter(y, size=ks)

    elif method == 'moving_average':
        ws = parameters.get('window_size', 11)
        ws = max(3, min(ws, len(y) // 4))
        kernel = np.ones(ws) / ws
        smoothed = np.convolve(y, kernel, mode='same')
        half_w = ws // 2
        for i in range(half_w):
            smoothed[i] = np.mean(y[:i*2+1]) if i > 0 else y[0]
            smoothed[-(i+1)] = np.mean(y[-(i*2+2):]) if i > 0 else y[-1]
        return smoothed

    elif method == 'wavelet':
        if not PYWT_AVAILABLE:
            return signal.savgol_filter(y, window_length=21, polyorder=3)
        wavelet = parameters.get('wavelet', 'db4')
        level = parameters.get('level', 3)
        threshold_mode = parameters.get('threshold_mode', 'soft')
        available = pywt.wavelist()
        if wavelet not in available:
            wavelet = 'db4'
        max_level = pywt.dwt_max_level(len(y), wavelet)
        level = min(level, max_level)
        coeffs = pywt.wavedec(y, wavelet, level=level)
        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        threshold = sigma * np.sqrt(2 * np.log(len(y)))
        coeffs_thresh = [coeffs[0]] + [pywt.threshold(c, threshold, mode=threshold_mode) for c in coeffs[1:]]
        reconstructed = pywt.waverec(coeffs_thresh, wavelet)
        if len(reconstructed) > len(y):
            reconstructed = reconstructed[:len(y)]
        elif len(reconstructed) < len(y):
            reconstructed = np.pad(reconstructed, (0, len(y) - len(reconstructed)), mode='edge')
        return reconstructed

    else:
        return y.copy()


def plot_spectrum(x: np.ndarray, y_raw: np.ndarray, y_denoised: np.ndarray,
                 peak_indices: np.ndarray, output_path: str, spectrum_id: str) -> None:
    plt.rcParams.update({
        'font.family': 'serif',
        'font.size': 11,
        'axes.linewidth': 1.5,
        'axes.spines.top': True,
        'axes.spines.right': True,
        'xtick.direction': 'in',
        'ytick.direction': 'in',
        'xtick.major.width': 1.5,
        'ytick.major.width': 1.5,
        'xtick.minor.visible': True,
        'ytick.minor.visible': True,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
    })

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x, y_raw, color='#AAAAAA', linewidth=1.0, alpha=0.7, label='Raw spectrum', zorder=2)
    ax.plot(x, y_denoised, color='#1A5276', linewidth=1.5, label='Denoised spectrum', zorder=3)

    if len(peak_indices) > 0:
        ax.scatter(x[peak_indices], y_denoised[peak_indices],
                   color='#C0392B', s=40, zorder=4, label='Detected peaks', marker='v')
        for idx in peak_indices:
            ax.annotate(f'{x[idx]:.0f}',
                        xy=(x[idx], y_denoised[idx]),
                        xytext=(0, 10),
                        textcoords='offset points',
                        ha='center', va='bottom',
                        fontsize=7.5, color='#C0392B')

    ax.set_xlabel('Raman Shift (cm⁻¹)', fontsize=12, labelpad=8)
    ax.set_ylabel('Intensity (a.u.)', fontsize=12, labelpad=8)
    ax.set_title(f'Raman Spectrum — {spectrum_id}', fontsize=13, pad=10)

    ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.5, color='#CCCCCC', zorder=1)
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())

    legend = ax.legend(frameon=True, framealpha=0.9, edgecolor='#AAAAAA',
                       loc='upper right', fontsize=10)
    legend.get_frame().set_linewidth(0.8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()


def extract_peaks(x: np.ndarray, y_denoised: np.ndarray) -> dict:
    y_range = np.max(y_denoised) - np.min(y_denoised)
    min_height = np.min(y_denoised) + 0.05 * y_range
    min_prominence = 0.02 * y_range
    min_distance = max(5, len(x) // 200)

    peak_indices, properties = signal.find_peaks(
        y_denoised,
        height=min_height,
        prominence=min_prominence,
        distance=min_distance
    )

    return {
        'indices': peak_indices,
        'prominences': properties.get('prominences', np.zeros(len(peak_indices)))
    }


def compute_fwhm(x: np.ndarray, y_denoised: np.ndarray,
                 peak_indices: np.ndarray, prominences: np.ndarray) -> list:
    if len(peak_indices) == 0:
        return []

    widths, _, left_ips, right_ips = signal.peak_widths(y_denoised, peak_indices, rel_height=0.5)
    avg_x_spacing = float(np.mean(np.abs(np.diff(x))))
    peaks_list = []

    for i, idx in enumerate(peak_indices):
        li = max(0, min(int(np.floor(left_ips[i])), len(x) - 1))
        ri = max(0, min(int(np.ceil(right_ips[i])), len(x) - 1))
        fwhm_cm1 = float(x[ri] - x[li]) if li < ri else float(widths[i] * avg_x_spacing)

        peaks_list.append({
            'index': int(idx),
            'raman_shift_cm-1': float(x[idx]),
            'intensity': float(y_denoised[idx]),
            'prominence': float(prominences[i]),
            'fwhm_cm-1': abs(fwhm_cm1)
        })

    peaks_list.sort(key=lambda p: p['intensity'], reverse=True)
    return peaks_list


def call_llm_for_material_id(spectrum_id: str, processing_info: dict,
                              peaks_list: list, diagnostics: dict) -> dict:
    sorted_peaks = sorted(peaks_list, key=lambda p: p.get('raman_shift_cm-1', 0))
    peak_lines = []
    peak_shifts = [p.get('raman_shift_cm-1', 0) for p in sorted_peaks]

    for p in sorted_peaks:
        peak_lines.append(
            f"  shift={p.get('raman_shift_cm-1', 0):.2f} cm^-1 | "
            f"fwhm={p.get('fwhm_cm-1', 0):.2f} cm^-1 | "
            f"prominence={p.get('prominence', 0):.2f} | "
            f"intensity={p.get('intensity', 0):.2f}"
        )

    peak_table = "\n".join(peak_lines) if peak_lines else "  (no peaks detected)"

    prompt = f"""You are an expert Raman spectroscopist. Identify the material from this spectrum.

SPECTRUM ID: {spectrum_id}

PREPROCESSING:
  method: {processing_info.get('denoise_method', 'unknown')}
  parameters: {json.dumps(processing_info.get('parameters', {}))}
  diagnostics: {json.dumps(diagnostics)}

DETECTED PEAKS (ascending by Raman shift):
{peak_table}

Analyze the peaks and identify:
- material (lowercase)
- phase (e.g., crystalline, amorphous, polycrystalline)
- layer_number (e.g., monolayer, bilayer, few-layer, bulk)
- stacking_order (e.g., AB, AA, random, N/A)
- sample_purity (pure, mixed, contaminated, unknown)

Rules:
- Prefer simplest explanation consistent with peaks
- Reference specific peaks by shift in reasoning
- If uncertain, use "unknown" with low confidence
- decision_trace: 3-8 concise bullet facts
- top_candidates: exactly 3 entries
- analysis_steps: 6-8 concise reasoning steps (not long chain-of-thought)

Return ONLY valid JSON, no markdown:
{{
  "material_prediction": {{
    "material": "silicon",
    "phase": "crystalline",
    "layer_number": "bulk",
    "stacking_order": "diamond cubic",
    "sample_purity": "pure"
  }},
  "confidence": 0.95,
  "reasoning": "Short paragraph referencing peak shifts",
  "decision_trace": [
    "Fact 1",
    "Fact 2",
    "Fact 3"
  ],
  "top_candidates": [
    {{"material": "silicon", "confidence": 0.95}},
    {{"material": "germanium", "confidence": 0.03}},
    {{"material": "unknown", "confidence": 0.02}}
  ],
  "analysis_steps": [
    "Step 1",
    "Step 2",
    "Step 3",
    "Step 4",
    "Step 5",
    "Step 6"
  ]
}}"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=1500
    )
    raw = response.choices[0].message.content.strip()

    if raw.startswith('```'):
        lines = raw.split('\n')
        raw = '\n'.join(lines[1:-1])

    parsed = None
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find('{')
        end = raw.rfind('}')
        if start != -1 and end != -1:
            try:
                parsed = json.loads(raw[start:end+1])
            except json.JSONDecodeError:
                pass

    if parsed is None:
        repair_prompt = f"Fix this JSON and return ONLY valid JSON:\n{raw[:3000]}"
        repair_response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": repair_prompt}],
            max_completion_tokens=1500
        )
        repair_raw = repair_response.choices[0].message.content.strip()
        if repair_raw.startswith('```'):
            lines = repair_raw.split('\n')
            repair_raw = '\n'.join(lines[1:-1])
        try:
            parsed = json.loads(repair_raw)
        except json.JSONDecodeError:
            parsed = None

    fallback_candidates = [
        {"material": "unknown", "confidence": 0.0},
        {"material": "unknown", "confidence": 0.0},
        {"material": "unknown", "confidence": 0.0}
    ]

    if parsed is None:
        return {
            "material_prediction": {
                "material": "unknown",
                "phase": "unknown",
                "layer_number": "unknown",
                "stacking_order": "unknown",
                "sample_purity": "unknown"
            },
            "confidence": 0.0,
            "reasoning": "Model output invalid or could not be parsed.",
            "decision_trace": ["Invalid model output."],
            "top_candidates": fallback_candidates,
            "analysis_steps": ["Invalid model output."],
            "peak_shifts": sorted(peak_shifts)
        }

    mp = parsed.get('material_prediction', {})
    if isinstance(mp.get('material'), str):
        mp['material'] = mp['material'].lower()

    candidates = parsed.get('top_candidates', fallback_candidates)
    while len(candidates) < 3:
        candidates.append({"material": "unknown", "confidence": 0.0})
    candidates = candidates[:3]
    for c in candidates:
        if isinstance(c.get('material'), str):
            c['material'] = c['material'].lower()

    dt = parsed.get('decision_trace', ["No decision trace."])
    if not isinstance(dt, list) or len(dt) < 1:
        dt = ["No decision trace."]

    return {
        "material_prediction": mp,
        "confidence": float(parsed.get('confidence', 0.0)),
        "reasoning": parsed.get('reasoning', ''),
        "decision_trace": dt,
        "top_candidates": candidates,
        "analysis_steps": parsed.get('analysis_steps', []),
        "peak_shifts": sorted(peak_shifts)
    }


def save_outputs(output_dir: str, spectrum_id: str, processing_info: dict,
                 peaks_list: list, material_result: dict) -> None:
    os.makedirs(output_dir, exist_ok=True)

    processed = {
        "spectrum_id": spectrum_id,
        "processing": processing_info,
        "num_peaks": len(peaks_list),
        "peaks": peaks_list
    }
    with open(os.path.join(output_dir, 'processed_spectrum.json'), 'w') as f:
        json.dump(processed, f, indent=2)

    classification = {
        "spectrum_id": spectrum_id,
        "model": MODEL_NAME,
        "material_prediction": material_result.get('material_prediction', {}),
        "confidence": material_result.get('confidence', 0.0),
        "reasoning": material_result.get('reasoning', ''),
        "top_candidates": material_result.get('top_candidates', []),
        "observed_peaks_cm-1": material_result.get('peak_shifts', [])
    }
    with open(os.path.join(output_dir, 'classification_result.json'), 'w') as f:
        json.dump(classification, f, indent=2)

    chain = {
        "spectrum_id": spectrum_id,
        "model": MODEL_NAME,
        "analysis_steps": material_result.get('analysis_steps', []),
        "decision_trace": material_result.get('decision_trace', [])
    }
    with open(os.path.join(output_dir, 'chain_of_thought.json'), 'w') as f:
        json.dump(chain, f, indent=2)


def main():
    if len(sys.argv) != 3:
        print("Usage: python solution.py input_spectrum.json output_dir/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2].rstrip('/')

    print(f"[Stage 1] Loading spectrum from: {input_path}")
    spectrum = load_spectrum(input_path)
    x = spectrum['x']
    y = spectrum['y']
    spectrum_id = spectrum['spectrum_id']
    print(f"  Spectrum ID: {spectrum_id} | Points: {len(x)} | Range: {x[0]:.1f}–{x[-1]:.1f} cm^-1")

    print("[Stage 2] Computing signal diagnostics...")
    diagnostics = compute_diagnostics(x, y)
    print(f"  SNR: {diagnostics['snr_estimate']:.1f} | Noise: {diagnostics['noise_level']} | "
          f"Spikes: {diagnostics['spike_noise']} | Baseline drift: {diagnostics['baseline_drift']}")

    print("[Stage 3] Querying LLM for denoising strategy...")
    llm_denoise = call_llm_for_denoising(diagnostics)
    method = llm_denoise['denoise_method']
    params = llm_denoise['parameters']
    print(f"  Method: {method} | Params: {params}")
    print(f"  Reason: {llm_denoise.get('reason', '')}")

    print("[Stage 4] Applying denoising...")
    y_denoised = apply_denoising(y, method, params)
    print(f"  Done. Output range: [{y_denoised.min():.1f}, {y_denoised.max():.1f}]")

    print("[Stage 6] Extracting peaks...")
    peak_data = extract_peaks(x, y_denoised)
    peak_indices = peak_data['indices']
    prominences = peak_data['prominences']
    print(f"  Found {len(peak_indices)} peaks")

    print("[Stage 7] Computing FWHM...")
    peaks_list = compute_fwhm(x, y_denoised, peak_indices, prominences)

    print("[Stage 5] Generating spectrum plot...")
    os.makedirs(output_dir, exist_ok=True)
    plot_path = os.path.join(output_dir, 'spectrum_plot.png')
    plot_spectrum(x, y, y_denoised, peak_indices, plot_path, spectrum_id)
    print(f"  Saved: {plot_path}")

    print("[Stage 8] Querying LLM for material identification...")
    processing_info = {
        "denoise_method": method,
        "parameters": params,
        "reason": llm_denoise.get('reason', ''),
        "llm_diagnostics": llm_denoise.get('diagnostics', {})
    }
    material_result = call_llm_for_material_id(spectrum_id, processing_info, peaks_list, diagnostics)
    mp = material_result.get('material_prediction', {})
    print(f"  Material: {mp.get('material', 'unknown')} | "
          f"Phase: {mp.get('phase', 'unknown')} | "
          f"Confidence: {material_result.get('confidence', 0.0):.2f}")

    print("[Stage 9] Saving benchmark outputs...")
    save_outputs(output_dir, spectrum_id, processing_info, peaks_list, material_result)
    print(f"  processed_spectrum.json")
    print(f"  classification_result.json")
    print(f"  chain_of_thought.json")
    print(f"  spectrum_plot.png")
    print(f"\nPipeline complete. Results in: {output_dir}/")


if __name__ == '__main__':
    main()