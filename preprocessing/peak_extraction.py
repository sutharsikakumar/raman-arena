import sys
import json
import argparse
import numpy as np
from scipy import signal
from scipy.ndimage import median_filter as scipy_median_filter
import anthropic
import os
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

try:
    import pywt
    PYWT_AVAILABLE = True
except ImportError:
    PYWT_AVAILABLE = False


def load_spectrum(filepath: str) -> dict:
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    required_keys = ['x', 'y']
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required key '{key}' in spectrum JSON")
    
    x = np.array(data['x'], dtype=float)
    y = np.array(data['y'], dtype=float)
    
    if len(x) == 0 or len(y) == 0:
        raise ValueError("Spectrum contains empty x or y arrays")
    
    if len(x) != len(y):
        raise ValueError(f"Length mismatch: x has {len(x)} points, y has {len(y)} points")
    
    return {
        'spectrum_id': data.get('spectrum_id', 'unknown'),
        'x_unit': data.get('x_unit', 'cm^-1'),
        'y_unit': data.get('y_unit', 'counts'),
        'x': x,
        'y': y
    }


def compute_signal_diagnostics(x: np.ndarray, y: np.ndarray) -> dict:
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
    
    x_norm = np.linspace(0, 1, len(x))
    poly_coeffs = np.polyfit(x_norm, y, 3)
    baseline_fit = np.polyval(poly_coeffs, x_norm)
    baseline_variation = np.std(baseline_fit)
    baseline_drift = bool(baseline_variation > 0.1 * signal_range)
    
    rough_peaks, _ = signal.find_peaks(y, height=np.percentile(y, 75), distance=5)
    peak_density_ratio = len(rough_peaks) / (len(x) / 100)
    
    if peak_density_ratio < 1:
        peak_density = "low"
    elif peak_density_ratio < 3:
        peak_density = "medium"
    else:
        peak_density = "high"
    
    peak_widths_rough = []
    if len(rough_peaks) > 0:
        widths = signal.peak_widths(y, rough_peaks, rel_height=0.5)[0]
        peak_widths_rough = widths.tolist()
    
    avg_width = np.mean(peak_widths_rough) if peak_widths_rough else float('inf')
    peak_sharpness = "sharp" if avg_width < 10 else ("moderate" if avg_width < 30 else "broad")
    
    x_range = float(x[-1] - x[0]) if len(x) > 1 else 0.0
    x_resolution = float(x_range / len(x)) if len(x) > 1 else 0.0
    
    return {
        'num_points': int(len(x)),
        'x_range': x_range,
        'x_resolution_cm-1': x_resolution,
        'y_min': float(np.min(y)),
        'y_max': float(np.max(y)),
        'snr_estimate': float(snr),
        'noise_level': noise_level,
        'spike_noise': spike_noise,
        'baseline_drift': baseline_drift,
        'peak_density': peak_density,
        'peak_sharpness': peak_sharpness,
        'num_rough_peaks': int(len(rough_peaks))
    }


def call_llm_for_denoising(diagnostics: dict) -> dict:
    client = anthropic.Anthropic()
    
    prompt = f"""You are an expert in Raman spectroscopy signal processing. 
Analyze the following spectrum diagnostics and decide the optimal denoising strategy.

Spectrum Diagnostics:
{json.dumps(diagnostics, indent=2)}

Based on these diagnostics, choose the best denoising method and parameters.

Available methods:
- savitzky_golay: Best for preserving peak shapes in moderate noise. Parameters: window_length (odd integer, 5-51), polyorder (2-5)
- median_filter: Best for spike/impulse noise removal. Parameters: kernel_size (odd integer, 3-15)
- wavelet: Best for mixed noise types. Parameters: wavelet (e.g., 'db4', 'sym4'), level (1-5), threshold_mode ('soft' or 'hard')
- moving_average: Simple smoothing for heavy noise. Parameters: window_size (3-51)
- none: If signal is already clean (SNR > 100 and no artifacts)

Consider:
1. noise_level: high noise needs stronger smoothing
2. spike_noise: True suggests median_filter is important
3. peak_sharpness: sharp peaks need methods that preserve shape (savitzky_golay)
4. baseline_drift: affects which method works best
5. peak_density: dense peaks need narrower windows

Return ONLY valid JSON with this exact structure (no markdown, no explanation):
{{
  "diagnostics": {{
    "noise_level": "{diagnostics.get('noise_level', 'moderate')}",
    "spike_noise": {str(diagnostics.get('spike_noise', False)).lower()},
    "baseline_drift": {str(diagnostics.get('baseline_drift', False)).lower()},
    "peak_density": "{diagnostics.get('peak_density', 'low')}"
  }},
  "denoise_method": "savitzky_golay",
  "parameters": {{
    "window_length": 21,
    "polyorder": 3
  }},
  "reason": "Brief explanation of why this method was chosen"
}}"""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    if response_text.startswith('```'):
        lines = response_text.split('\n')
        response_text = '\n'.join(lines[1:-1])
    
    try:
        llm_response = json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"Warning: LLM returned invalid JSON: {e}. Using fallback.")
        llm_response = None
    
    if llm_response is None or 'denoise_method' not in llm_response:
        print("Warning: Invalid LLM response structure. Using fallback denoising.")
        llm_response = {
            "diagnostics": {
                "noise_level": diagnostics.get('noise_level', 'moderate'),
                "spike_noise": diagnostics.get('spike_noise', False),
                "baseline_drift": diagnostics.get('baseline_drift', False),
                "peak_density": diagnostics.get('peak_density', 'low')
            },
            "denoise_method": "savitzky_golay",
            "parameters": {"window_length": 21, "polyorder": 3},
            "reason": "Fallback: Savitzky-Golay preserves peak shapes while smoothing moderate noise."
        }
    
    valid_methods = ['savitzky_golay', 'median_filter', 'wavelet', 'moving_average', 'none']
    if llm_response.get('denoise_method') not in valid_methods:
        print(f"Warning: Invalid denoise method '{llm_response.get('denoise_method')}'. Using savitzky_golay.")
        llm_response['denoise_method'] = 'savitzky_golay'
        llm_response['parameters'] = {'window_length': 21, 'polyorder': 3}
    
    return llm_response


def apply_denoising(y: np.ndarray, method: str, parameters: dict) -> np.ndarray:
    if method == 'none':
        return y.copy()
    
    elif method == 'savitzky_golay':
        window_length = parameters.get('window_length', 21)
        polyorder = parameters.get('polyorder', 3)
        
        if window_length % 2 == 0:
            window_length += 1
        
        if window_length <= polyorder:
            window_length = polyorder + 2
            if window_length % 2 == 0:
                window_length += 1
        
        window_length = min(window_length, len(y) if len(y) % 2 == 1 else len(y) - 1)
        
        return signal.savgol_filter(y, window_length=window_length, polyorder=polyorder)
    
    elif method == 'median_filter':
        kernel_size = parameters.get('kernel_size', 5)
        if kernel_size % 2 == 0:
            kernel_size += 1
        kernel_size = max(3, min(kernel_size, len(y) // 2 * 2 - 1))
        return scipy_median_filter(y, size=kernel_size)
    
    elif method == 'moving_average':
        window_size = parameters.get('window_size', 11)
        window_size = max(3, min(window_size, len(y) // 4))
        kernel = np.ones(window_size) / window_size
        smoothed = np.convolve(y, kernel, mode='same')
        half_w = window_size // 2
        for i in range(half_w):
            smoothed[i] = np.mean(y[:i*2+1]) if i > 0 else y[0]
            smoothed[-(i+1)] = np.mean(y[-(i*2+2):]) if i > 0 else y[-1]
        return smoothed
    
    elif method == 'wavelet':
        if not PYWT_AVAILABLE:
            print("Warning: pywt not available, falling back to Savitzky-Golay")
            return signal.savgol_filter(y, window_length=21, polyorder=3)
        
        wavelet = parameters.get('wavelet', 'db4')
        level = parameters.get('level', 3)
        threshold_mode = parameters.get('threshold_mode', 'soft')
        
        available_wavelets = pywt.wavelist()
        if wavelet not in available_wavelets:
            wavelet = 'db4'
        
        max_level = pywt.dwt_max_level(len(y), wavelet)
        level = min(level, max_level)
        
        coeffs = pywt.wavedec(y, wavelet, level=level)
        
        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        threshold = sigma * np.sqrt(2 * np.log(len(y)))
        
        coeffs_thresh = [coeffs[0]]
        for detail in coeffs[1:]:
            if threshold_mode == 'soft':
                thresh_detail = pywt.threshold(detail, threshold, mode='soft')
            else:
                thresh_detail = pywt.threshold(detail, threshold, mode='hard')
            coeffs_thresh.append(thresh_detail)
        
        reconstructed = pywt.waverec(coeffs_thresh, wavelet)
        
        if len(reconstructed) > len(y):
            reconstructed = reconstructed[:len(y)]
        elif len(reconstructed) < len(y):
            reconstructed = np.pad(reconstructed, (0, len(y) - len(reconstructed)), mode='edge')
        
        return reconstructed
    
    else:
        print(f"Warning: Unknown denoising method '{method}', returning original signal.")
        return y.copy()


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
    
    prominences = properties.get('prominences', np.zeros(len(peak_indices)))
    
    return {
        'indices': peak_indices,
        'prominences': prominences
    }


def compute_fwhm(x: np.ndarray, y_denoised: np.ndarray, peak_indices: np.ndarray, 
                 prominences: np.ndarray) -> list:
    if len(peak_indices) == 0:
        return []
    
    widths, width_heights, left_ips, right_ips = signal.peak_widths(
        y_denoised, peak_indices, rel_height=0.5
    )
    
    x_spacing = np.abs(np.diff(x))
    avg_x_spacing = np.mean(x_spacing)
    
    peaks_list = []
    for i, idx in enumerate(peak_indices):
        left_idx = int(np.floor(left_ips[i]))
        right_idx = int(np.ceil(right_ips[i]))
        
        left_idx = max(0, min(left_idx, len(x) - 1))
        right_idx = max(0, min(right_idx, len(x) - 1))
        
        if left_idx < right_idx:
            fwhm_cm1 = float(x[right_idx] - x[left_idx])
        else:
            fwhm_cm1 = float(widths[i] * avg_x_spacing)
        
        peaks_list.append({
            'index': int(idx),
            'raman_shift_cm-1': float(x[idx]),
            'intensity': float(y_denoised[idx]),
            'prominence': float(prominences[i]),
            'fwhm_cm-1': abs(fwhm_cm1)
        })
    
    peaks_list.sort(key=lambda p: p['intensity'], reverse=True)
    
    return peaks_list


def save_results(output_path: str, spectrum_id: str, llm_response: dict, 
                 peaks_list: list) -> None:
    results = {
        'spectrum_id': spectrum_id,
        'processing': {
            'denoise_method': llm_response.get('denoise_method', 'unknown'),
            'parameters': llm_response.get('parameters', {}),
            'reason': llm_response.get('reason', ''),
            'llm_diagnostics': llm_response.get('diagnostics', {})
        },
        'num_peaks': len(peaks_list),
        'peaks': peaks_list
    }
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Raman Spectrum Processing Pipeline with LLM-guided denoising'
    )
    parser.add_argument('input_json', help='Path to input spectrum JSON file')
    parser.add_argument('output_json', help='Path to output results JSON file')
    args = parser.parse_args()
    
    print(f"Loading spectrum from: {args.input_json}")
    spectrum = load_spectrum(args.input_json)
    x = spectrum['x']
    y = spectrum['y']
    spectrum_id = spectrum['spectrum_id']
    
    print(f"Spectrum ID: {spectrum_id}, Points: {len(x)}")
    print(f"X range: {x[0]:.1f} - {x[-1]:.1f} {spectrum['x_unit']}")
    
    print("\nComputing signal diagnostics...")
    diagnostics = compute_signal_diagnostics(x, y)
    print(f"  Noise level: {diagnostics['noise_level']}")
    print(f"  SNR estimate: {diagnostics['snr_estimate']:.1f}")
    print(f"  Spike noise: {diagnostics['spike_noise']}")
    print(f"  Baseline drift: {diagnostics['baseline_drift']}")
    print(f"  Peak density: {diagnostics['peak_density']}")
    print(f"  Rough peak count: {diagnostics['num_rough_peaks']}")
    
    print("\nQuerying Claude LLM for denoising strategy...")
    llm_response = call_llm_for_denoising(diagnostics)
    
    print(f"  Denoising method: {llm_response['denoise_method']}")
    print(f"  Parameters: {llm_response['parameters']}")
    print(f"  Reason: {llm_response['reason']}")
    
    print("\nApplying denoising...")
    y_denoised = apply_denoising(y, llm_response['denoise_method'], llm_response['parameters'])
    print(f"  Denoising complete. Output range: [{y_denoised.min():.1f}, {y_denoised.max():.1f}]")
    
    print("\nExtracting peaks...")
    peak_data = extract_peaks(x, y_denoised)
    peak_indices = peak_data['indices']
    prominences = peak_data['prominences']
    print(f"  Found {len(peak_indices)} peaks")
    
    print("\nComputing FWHM for each peak...")
    peaks_list = compute_fwhm(x, y_denoised, peak_indices, prominences)
    
    if peaks_list:
        print(f"  Top 5 peaks by intensity:")
        for i, peak in enumerate(peaks_list[:5]):
            print(f"    {i+1}. Shift: {peak['raman_shift_cm-1']:.1f} cm⁻¹, "
                  f"Intensity: {peak['intensity']:.1f}, "
                  f"FWHM: {peak['fwhm_cm-1']:.2f} cm⁻¹")
    
    print(f"\nSaving results to: {args.output_json}")
    save_results(args.output_json, spectrum_id, llm_response, peaks_list)
    
    print("\nPipeline complete!")
    print(f"  Total peaks detected: {len(peaks_list)}")
    print(f"  Results saved to: {args.output_json}")


if __name__ == '__main__':
    main()
