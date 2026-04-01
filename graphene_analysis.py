"""
Nature-style multi-panel Raman spectroscopy LLM benchmarking figure.
Panels A–D, graphene-specific, matplotlib only.

File mapping:
  Panel A  ← /unmarked/<sample>.json + /denoised_spectra/<sample>_peaks.json
  Panel B  ← /ranking_sample_d/<letter>/classification_result.json  (all letters)
             /graphene_elo_results/all_games.json
  Panel C  ← same classification_result.json + chain_of_thought.json (best + worst ELO)
  Panel D  ← all classification_result.json + all chain_of_thought.json
             + /graphene_elo_results/all_games.json (ELO ordering)
"""

import json, os, re, warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.gridspec import GridSpec
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.lines import Line2D
from scipy.signal import find_peaks, savgol_filter
import networkx as nx

warnings.filterwarnings("ignore")

# ─── GLOBAL STYLE ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":       "sans-serif",
    "font.sans-serif":   ["Helvetica Neue", "Arial", "DejaVu Sans"],
    "font.size":         7,
    "axes.linewidth":    0.8,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size":  3,
    "ytick.major.size":  3,
    "xtick.direction":   "out",
    "ytick.direction":   "out",
    "pdf.fonttype":      42,
    "ps.fonttype":       42,
    "figure.dpi":        300,
    "savefig.dpi":       300,
})

# ─── COLOUR PALETTE ───────────────────────────────────────────────────────────
C = dict(
    correct   = "#2E7D5E",
    uncertain = "#C17D2A",
    wrong     = "#B03A3A",
    navy      = "#1A1A2E",
    bg        = "#FAFAF8",
    grid      = "#E0DFDB",
    text      = "#1A1A1E",
    muted     = "#888880",
    border    = "#C8C7C2",
    claude    = "#2E5C8A",
    openai    = "#2E7D5E",
    gemini    = "#8A5C2E",
)

ERROR_TYPES  = ["peak_misassign", "hallucinated_peak", "wrong_material",
                "wrong_layer", "reasoning_contradiction", "overconfidence"]
ERROR_LABELS = ["Peak\nmisassign.", "Halluc.\npeak", "Wrong\nmaterial",
                "Wrong\nlayer", "Reasoning\ncontrad.", "Over-\nconfidence"]
ERROR_COLORS = ["#C17D2A", "#8B3A3A", "#B03A3A", "#6B4C9A", "#2A6B8B", "#7A6E2A"]

# ─── GRAPHENE GROUND-TRUTH PEAK TABLE ─────────────────────────────────────────
GT_PEAKS = [
    dict(name="D",   pos=1345, gamma=18, A=0.18, fwhm=36,  valid=True,
         note="Defect-activated; absent in pristine"),
    dict(name="G",   pos=1582, gamma=12, A=1.00, fwhm=24,  valid=True,
         note="In-plane E\u2082g; always present"),
    dict(name="D'",  pos=1620, gamma=8,  A=0.09, fwhm=16,  valid=True,
         note="Defect-activated; near G"),
    dict(name="2D",  pos=2695, gamma=22, A=0.92, fwhm=44,  valid=True,
         note="I\u2082D/I_G\u22481 \u2192 monolayer"),
]
GT_MAT    = "graphene"
GT_LAYERS = 1          # monolayer ground-truth

# ─── SYNTHETIC DATA (replace with JSON loaders below) ─────────────────────────

def lorentzian(x, x0, gamma, A):
    return A / (1 + ((x - x0) / gamma) ** 2)

def make_spectrum():
    x = np.linspace(1150, 2900, 1400)
    rng = np.random.default_rng(42)
    signal = sum(lorentzian(x, p["pos"], p["gamma"], p["A"]) for p in GT_PEAKS)
    raw    = signal * 0.9 + rng.normal(0, 0.025, len(x))
    den    = savgol_filter(signal, 11, 3)
    return x, raw, den

def make_models():
    """
    Simulates what createModelData() would produce from your JSON files.
    Replace with real JSON loaders targeting:
      /ranking_sample_d/{letter}/classification_result.json
      /ranking_sample_d/{letter}/chain_of_thought.json
      /graphene_elo_results/all_games.json
    """
    base = [
        dict(id="a", family="Claude",  elo=1487, conf=0.94, mat="graphene",  layers=1,
             errors=[],
             best_step  ="G peak at 1582 cm\u207b\u00b9 (FWHM 24 cm\u207b\u00b9); I\u2082D/I_G\u22480.92 confirms monolayer.",
             worst_step ="",
             peak_assigns=[("D",1345,True),("G",1582,True),("D'",1620,True),("2D",2695,True)]),
        dict(id="b", family="OpenAI",  elo=1451, conf=0.89, mat="graphene",  layers=1,
             errors=["layer_uncertain"],
             best_step  ="Strong 2D feature; I\u2082D/I_G consistent with 1L graphene.",
             worst_step ="",
             peak_assigns=[("D",1345,True),("G",1582,True),("2D",2695,True)]),
        dict(id="c", family="Claude",  elo=1438, conf=0.85, mat="graphene",  layers=2,
             errors=["wrong_layer"],
             best_step  ="",
             worst_step ="Slight 2D broadening suggests bilayer.",
             peak_assigns=[("D",1345,True),("G",1582,True),("2D",2695,True)]),
        dict(id="d", family="Gemini",  elo=1412, conf=0.91, mat="graphene",  layers=1,
             errors=["overconfidence"],
             best_step  ="",
             worst_step ="",
             peak_assigns=[("G",1582,True),("2D",2695,True)]),
        dict(id="e", family="OpenAI",  elo=1398, conf=0.78, mat="graphene",  layers=1,
             errors=["peak_misassign"],
             best_step  ="",
             worst_step ="Peak at 1582 cm\u207b\u00b9 assigned to D band (error).",
             peak_assigns=[("D",1345,True),("D",1582,False),("2D",2695,True)]),
        dict(id="f", family="Gemini",  elo=1367, conf=0.72, mat="graphene",  layers=3,
             errors=["wrong_layer","overconfidence"],
             best_step  ="",
             worst_step ="",
             peak_assigns=[("G",1582,True),("2D",2695,True)]),
        dict(id="g", family="Claude",  elo=1334, conf=0.65, mat="hBN",       layers=1,
             errors=["wrong_material","hallucinated_peak"],
             best_step  ="",
             worst_step ="Peak at \u223c1366 cm\u207b\u00b9 = hBN E\u2082g; G at 1582 cm\u207b\u00b9 may be contamination.",
             peak_assigns=[("D",1345,False),("G",1582,False),("2D",2695,False)]),
        dict(id="h", family="OpenAI",  elo=1298, conf=0.81, mat="MoS\u2082",  layers=2,
             errors=["wrong_material","wrong_layer","hallucinated_peak"],
             best_step  ="",
             worst_step ="E\u00b2g at 383 cm\u207b\u00b9, A\u2081g at 408 cm\u207b\u00b9 \u2192 bilayer MoS\u2082.",
             peak_assigns=[]),
        dict(id="i", family="Gemini",  elo=1241, conf=0.88, mat="graphene",  layers=4,
             errors=["wrong_layer","reasoning_contradiction","overconfidence"],
             best_step  ="",
             worst_step ="Broad 2D \u2192 multilayer. [classifies as 1L \u2014 contradiction]",
             peak_assigns=[("G",1582,True),("2D",2695,True)]),
    ]
    return sorted(base, key=lambda m: m["elo"], reverse=True)

# ─── JSON LOADERS (wire to real files) ────────────────────────────────────────

def load_spectrum(sample_id="sample_a"):
    """Load raw spectrum data from unmarked JSON file."""
    with open(f'/Users/sutharsikakumar/raman-arena/unmarked/{sample_id}.json', 'r') as f:
        data = json.load(f)
    
    x = np.array(data['x'])
    raw = np.array(data['y'])
    
    # Apply simple denoising for display
    from scipy.signal import savgol_filter
    den = savgol_filter(raw, 11, 3)
    
    return x, raw, den

def load_peaks(sample_id="sample_a"):
    """Load peak data from denoised_spectra JSON file."""
    with open(f'/Users/sutharsikakumar/raman-arena/denoised_spectra/{sample_id}_peaks.json', 'r') as f:
        data = json.load(f)
    
    peaks = []
    for peak in data['peaks']:
        wavenumber = peak['raman_shift_cm-1']
        name = assign_peak_name(wavenumber)
        
        peaks.append(dict(
            name=name,
            pos=wavenumber,
            intensity=peak['intensity'],
            fwhm=peak['fwhm_cm-1'],
            gamma=peak['fwhm_cm-1']/2.355,  # Convert FWHM to gamma
            A=peak['intensity'],
            valid=is_valid_graphene_peak(wavenumber)
        ))
    
    return peaks

def assign_peak_name(wavenumber):
    """Assign peak name based on wavenumber range."""
    if 1300 <= wavenumber <= 1400:
        return "D"
    elif 1570 <= wavenumber <= 1600:
        return "G"
    elif 1600 <= wavenumber <= 1650:
        return "D'"
    elif 2650 <= wavenumber <= 2750:
        return "2D"
    else:
        return "?"

def is_valid_graphene_peak(wavenumber):
    """Check if wavenumber corresponds to valid graphene peak."""
    return (1300 <= wavenumber <= 1400) or (1570 <= wavenumber <= 1600) or \
           (1600 <= wavenumber <= 1650) or (2650 <= wavenumber <= 2750)

def load_models():
    """Load real model data from ranking_sample_d and ELO results."""
    models = []
    
    # Load ELO data
    with open('/Users/sutharsikakumar/raman-arena/graphene_elo_results/all_games.json', 'r') as f:
        elo_data = json.load(f)
    
    # Extract final ELO ratings
    elo_ratings = {}
    for game in elo_data:
        elo_ratings[game['model_a']] = game['elo_after'][game['model_a']]
        elo_ratings[game['model_b']] = game['elo_after'][game['model_b']]
    
    # Load classification and chain-of-thought data for each model
    for letter in 'abcdefghi':
        try:
            # Load classification result
            with open(f'/Users/sutharsikakumar/raman-arena/ranking_sample_d/{letter}/classification_result.json', 'r') as f:
                classification = json.load(f)
            
            # Load chain of thought
            with open(f'/Users/sutharsikakumar/raman-arena/ranking_sample_d/{letter}/chain_of_thought.json', 'r') as f:
                chain_of_thought = json.load(f)
            
            # Extract material and layer info
            material = classification.get('material_prediction', {}).get('material', 'unknown')
            layers = classification.get('material_prediction', {}).get('layer_number', 'unknown')
            
            # Convert layer number to numeric
            layer_num = 1
            if isinstance(layers, str):
                if layers.lower() == 'bulk':
                    layer_num = 10
                elif layers.lower() in ['monolayer', '1']:
                    layer_num = 1
                elif layers.lower() in ['bilayer', '2']:
                    layer_num = 2
                elif layers.isdigit():
                    layer_num = int(layers)
            
            # Determine model family
            if letter <= 'e':
                family = 'Claude'
            elif letter <= 'h':
                family = 'OpenAI'
            else:
                family = 'Gemini'
            
            # Extract peak assignments from observed_peaks_cm-1
            observed_peaks = classification.get('observed_peaks_cm-1', [])
            peak_assigns = []
            for peak_wavenumber in observed_peaks:
                if 1200 <= peak_wavenumber <= 3000:  # Focus on relevant range
                    peak_name = assign_peak_name(peak_wavenumber)
                    is_correct = is_valid_graphene_peak(peak_wavenumber)
                    peak_assigns.append((peak_name, peak_wavenumber, is_correct))
            
            # Detect errors
            errors = detect_model_errors(classification, chain_of_thought, material, layer_num)
            
            # Extract reasoning steps
            analysis_steps = chain_of_thought.get('analysis_steps', [])
            decision_trace = chain_of_thought.get('decision_trace', [])
            all_steps = analysis_steps + decision_trace
            
            # Find best and worst reasoning steps
            best_step = find_reasoning_step(all_steps, 'best')
            worst_step = find_reasoning_step(all_steps, 'worst')
            
            models.append(dict(
                id=letter,
                family=family,
                elo=elo_ratings.get(letter, 1200),
                conf=classification.get('confidence', 0.5),
                mat=material,
                layers=layer_num,
                errors=errors,
                reasoning=classification.get('reasoning', ''),
                peak_assigns=peak_assigns,
                best_step=best_step,
                worst_step=worst_step
            ))
            
        except Exception as e:
            print(f"Warning: Could not load data for model {letter}: {e}")
            continue
    
    return sorted(models, key=lambda m: m["elo"], reverse=True)

def detect_model_errors(classification, chain_of_thought, material, layers):
    """Detect various types of model errors."""
    errors = []
    
    # Check for wrong material
    if material.lower() not in ['graphene', 'graphene (few-layer)']:
        errors.append('wrong_material')
    
    # Check for wrong layer count
    if layers != GT_LAYERS:
        errors.append('wrong_layer')
    
    # Check for overconfidence
    confidence = classification.get('confidence', 0.5)
    if confidence > 0.9 and (material.lower() not in ['graphene', 'graphene (few-layer)'] or layers != GT_LAYERS):
        errors.append('overconfidence')
    
    # Check for reasoning contradictions
    reasoning = classification.get('reasoning', '')
    if ('multilayer' in reasoning.lower() or 'bilayer' in reasoning.lower()) and layers == 1:
        errors.append('reasoning_contradiction')
    
    # Check for hallucinated peaks
    observed_peaks = classification.get('observed_peaks_cm-1', [])
    has_hallucinated = any(peak < 200 or (400 < peak < 1200) or peak > 4000 for peak in observed_peaks)
    if has_hallucinated:
        errors.append('hallucinated_peak')
    
    # Check for peak misassignment
    if len(observed_peaks) > 0:
        graphene_peaks = [p for p in observed_peaks if 1200 <= p <= 3000]
        if len(graphene_peaks) < len(observed_peaks) * 0.5:  # Less than half are in relevant range
            errors.append('peak_misassign')
    
    return errors

def find_reasoning_step(steps, step_type):
    """Find relevant reasoning step based on type."""
    if not steps:
        return ""
    
    if step_type == 'best':
        # Look for G or 2D peak mentions
        for step in steps:
            step_lower = step.lower()
            if any(keyword in step_lower for keyword in ['g band', '2d', '1580', '2700', 'g peak']):
                return step
        return steps[0] if steps else ""
    
    elif step_type == 'worst':
        # Look for contradictions or wrong material assignments
        for step in steps:
            step_lower = step.lower()
            if any(keyword in step_lower for keyword in ['multilayer', 'bilayer', 'contradiction', 'mos2', 'hbn']):
                return step
        return steps[-1] if steps else ""
    
    return ""

# ─── MODEL COLOUR HELPER ──────────────────────────────────────────────────────

def model_color(m):
    mat  = m["mat"].lower().replace("\u2082","2")
    ok_m = "graphene" in mat
    ok_l = m["layers"] == GT_LAYERS
    if not ok_m:      return C["wrong"]
    if not ok_l:      return C["uncertain"]
    return C["correct"]

# ══════════════════════════════════════════════════════════════════════════════
#  PANEL A  — Ground-truth spectrum
# ══════════════════════════════════════════════════════════════════════════════

def draw_panel_A(ax, x, raw, den, peaks):
    ax.plot(x, raw, color="#BBBBBB", lw=0.6, alpha=0.7, zorder=1, label="Raw")
    ax.plot(x, den, color=C["navy"], lw=1.3, zorder=2, label="Denoised")

    ymax = max(den) * 1.15
    ax.set_ylim(-0.03, ymax)
    ax.set_xlim(x[0], x[-1])

    for p in peaks:
        # shaded peak region
        x_fill = np.linspace(p["pos"] - p["gamma"]*2.5, p["pos"] + p["gamma"]*2.5, 200)
        y_fill = lorentzian(x_fill, p["pos"], p["gamma"], p["A"])
        ax.fill_between(x_fill, 0, y_fill, color=C["correct"], alpha=0.10, zorder=0)

        # dashed line to peak top
        peak_y  = lorentzian(p["pos"], p["pos"], p["gamma"], p["A"])
        label_y = peak_y + ymax * 0.08
        ax.plot([p["pos"], p["pos"]], [peak_y, label_y - ymax*0.02],
                color=C["correct"], lw=0.7, ls="--", zorder=3)

        # peak name
        ax.text(p["pos"], label_y, p["name"],
                ha="center", va="bottom", fontsize=8, fontweight="bold",
                color=C["correct"], zorder=4)
        # wavenumber + FWHM
        ax.text(p["pos"], label_y - ymax*0.06,
                f'{p["pos"]} cm\u207b\u00b9\n({p["fwhm"]} cm\u207b\u00b9)',
                ha="center", va="top", fontsize=5.5, color=C["muted"], zorder=4,
                linespacing=1.3)

    # validity colour bar under x-axis
    bar_y = -0.025
    for p in peaks:
        col = C["correct"] if p["valid"] else C["wrong"]
        ax.barh(bar_y, p["gamma"]*4, left=p["pos"]-p["gamma"]*2,
                height=0.012, color=col, alpha=0.8)

    ax.set_xlabel("Raman shift (cm\u207b\u00b9)", fontsize=8)
    ax.set_ylabel("Intensity (norm.)", fontsize=8)
    ax.set_xlim(1150, 2900)
    ax.tick_params(labelsize=7)

    # I₂D/G annotation
    ratio_text = "I$_{2D}$/I$_G$ \u2248 0.92\n\u2192 monolayer"
    ax.annotate(ratio_text,
                xy=(2695, lorentzian(2695,2695,22,0.92)),
                xytext=(2500, 0.75),
                fontsize=6, color=C["navy"],
                arrowprops=dict(arrowstyle="-|>", color=C["navy"],
                                lw=0.7, mutation_scale=7),
                bbox=dict(boxstyle="round,pad=0.25", fc=C["bg"],
                          ec=C["border"], lw=0.6),
                ha="center")

    ax.legend(fontsize=6, frameon=False, loc="upper left",
              handlelength=1.5, handletextpad=0.4)

    # sample label
    ax.text(0.02, 0.97, "sample_a  ·  Graphene (1L ground-truth)",
            transform=ax.transAxes, fontsize=6, color=C["text"],
            va="top", style="italic")

    _panel_label(ax, "a")
    ax.set_title("Spectrum & peak annotations", fontsize=8,
                 fontweight="semibold", pad=4, color=C["text"])


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL B  — Model–peak agreement network
# ══════════════════════════════════════════════════════════════════════════════

def draw_panel_B(ax, models):
    ax.set_aspect("equal")
    ax.axis("off")

    G = nx.Graph()

    # Peak nodes (inner ring)
    peak_names  = ["D", "G", "D'", "2D"]
    peak_angles = np.linspace(90, 90 + 360, len(peak_names), endpoint=False)
    peak_r      = 0.30
    peak_pos    = {}
    for i, pn in enumerate(peak_names):
        θ = np.radians(peak_angles[i])
        peak_pos[pn] = (peak_r * np.cos(θ), peak_r * np.sin(θ))
        G.add_node(pn, ntype="peak")

    # Model nodes (outer ring)
    model_r     = 0.72
    n_models    = len(models)
    model_pos   = {}
    elo_vals    = [m["elo"] for m in models]
    elo_min, elo_max = min(elo_vals), max(elo_vals)
    for i, m in enumerate(models):
        θ = np.radians(-90 + i * 360 / n_models)
        model_pos[m["id"]] = (model_r * np.cos(θ), model_r * np.sin(θ))
        G.add_node(m["id"], ntype="model")

    # Draw edges
    for m in models:
        for (mode, wn, ok) in m.get("peak_assigns", []):
            pn = mode.split("(")[0]   # strip any suffix
            if pn not in peak_pos: continue
            ec = C["correct"] if ok else \
                 (C["wrong"] if not ok and m["mat"].lower()!="graphene" else C["uncertain"])
            x0, y0 = model_pos[m["id"]]
            x1, y1 = peak_pos[pn]
            ax.plot([x0, x1], [y0, y1], color=ec, lw=0.8, alpha=0.45, zorder=1)

    # Draw peak nodes
    for pn, (px, py) in peak_pos.items():
        wn_label = {"D":"1345","G":"1582","D'":"1620","2D":"2695"}[pn]
        circ = plt.Circle((px, py), 0.09, color=C["bg"],
                           ec=C["correct"], lw=1.4, zorder=3)
        ax.add_patch(circ)
        ax.text(px, py + 0.014, pn, ha="center", va="center",
                fontsize=8, fontweight="bold", color=C["correct"], zorder=4)
        ax.text(px, py - 0.046, f"{wn_label} cm\u207b\u00b9",
                ha="center", va="center", fontsize=5, color=C["muted"], zorder=4)

        # Consensus fraction bar
        n_correct = sum(
            1 for m in models
            if any(a[0] == pn and a[2] for a in m.get("peak_assigns", []))
        )
        frac = n_correct / len(models)
        bar_w, bar_h = 0.14, 0.022
        bar_x = px - bar_w / 2
        bar_y = py - 0.12
        ax.add_patch(mpatches.FancyBboxPatch(
            (bar_x, bar_y), bar_w, bar_h,
            boxstyle="round,pad=0", ec="none", fc=C["grid"], zorder=3))
        ax.add_patch(mpatches.FancyBboxPatch(
            (bar_x, bar_y), bar_w * frac, bar_h,
            boxstyle="round,pad=0", ec="none", fc=C["correct"], zorder=4))
        ax.text(px, bar_y - 0.025, f"{frac*100:.0f}%",
                ha="center", fontsize=5, color=C["muted"], zorder=4)

    # Draw model nodes
    for m in models:
        mp = model_pos[m["id"]]
        r  = 0.055 + 0.035 * (m["elo"] - elo_min) / max(elo_max - elo_min, 1)
        col = model_color(m)
        circ = plt.Circle(mp, r, color=col, alpha=0.87, zorder=5)
        ax.add_patch(circ)
        ax.text(mp[0], mp[1], m["id"],
                ha="center", va="center", fontsize=7, fontweight="bold",
                color="white", zorder=6)
        # family initial below node
        fam_col = C[m["family"].lower()] if m["family"].lower() in C else C["muted"]
        ax.text(mp[0], mp[1] - r - 0.038, m["family"][0],
                ha="center", fontsize=5, color=C["muted"], zorder=5)

    # ELO legend
    for size_label, r_ex in [("High ELO", 0.088), ("Low ELO", 0.056)]:
        pass   # handled in figure legend below

    # Edge legend
    leg_items = [
        Line2D([0],[0], color=C["correct"],  lw=1.5, label="Correct assignment"),
        Line2D([0],[0], color=C["uncertain"],lw=1.5, label="Uncertain / partial"),
        Line2D([0],[0], color=C["wrong"],    lw=1.5, label="Hallucinated"),
        Line2D([0],[0], color=C["correct"],  lw=0, marker="o", ms=7, alpha=0.85,
               label="Node size ∝ ELO"),
    ]
    ax.legend(handles=leg_items, fontsize=5.5, frameon=False,
              loc="lower center", bbox_to_anchor=(0.5, -0.06),
              ncol=2, handlelength=1.2, handletextpad=0.4, columnspacing=0.8)

    ax.set_xlim(-1.02, 1.02)
    ax.set_ylim(-1.02, 1.06)
    _panel_label_ax(ax, "b", x=0.01, y=0.97)
    ax.set_title("Model–peak agreement network", fontsize=8,
                 fontweight="semibold", pad=4, color=C["text"])


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL C  — Reasoning-chain overlay
# ══════════════════════════════════════════════════════════════════════════════

def draw_panel_C(ax, x, den, models):
    ax.plot(x, den, color=C["navy"], lw=1.1, alpha=0.45, zorder=1)
    ax.set_xlim(1150, 2900)
    ymax = max(den) * 1.15
    ax.set_ylim(-0.03, ymax)
    ax.set_xlabel("Raman shift (cm\u207b\u00b9)", fontsize=8)
    ax.set_ylabel("Intensity (norm.)", fontsize=8)
    ax.tick_params(labelsize=7)

    best  = models[0]
    worst = models[-1]

    # ── Best model callout at G peak ──
    g_y   = lorentzian(1582, 1582, 12, 1.00)
    best_txt = (best.get("best_step") or best.get("reasoning") or
                "G at 1582 cm\u207b\u00b9, FWHM 24 cm\u207b\u00b9; I\u2082D/I_G\u22480.92 \u2192 monolayer confirmed.")
    best_txt = _wrap(best_txt, 42)

    ax.annotate(
        f"Model {best['id']} (rank 1)\n{best_txt}",
        xy=(1582, g_y),
        xytext=(1582, g_y + ymax * 0.30),
        fontsize=5.8, color=C["text"],
        ha="center", va="bottom",
        arrowprops=dict(arrowstyle="-|>", color=C["correct"],
                        lw=0.8, mutation_scale=7),
        bbox=dict(boxstyle="round,pad=0.35", fc="#F0FAF5",
                  ec=C["correct"], lw=1.0, alpha=0.95),
        zorder=6
    )

    # ── Worst model callout ──
    d_y   = lorentzian(1345, 1345, 18, 0.18)
    worst_txt = (worst.get("worst_step") or
                 "Broad 2D \u2192 multilayer; yet classifies as 1L [contradiction]. "
                 "Cites MoS\u2082 peaks absent from spectrum.")
    worst_txt = _wrap(worst_txt, 42)

    ax.annotate(
        f"Model {worst['id']} (rank {len(models)}) \u26a0 contradiction\n{worst_txt}",
        xy=(1345, d_y),
        xytext=(1700, d_y + ymax * 0.28),
        fontsize=5.8, color=C["text"],
        ha="center", va="bottom",
        arrowprops=dict(arrowstyle="-|>", color=C["wrong"],
                        lw=0.8, mutation_scale=7, ls=(0,(3,2))),
        bbox=dict(boxstyle="round,pad=0.35", fc="#FFF5F5",
                  ec=C["wrong"], lw=1.0, ls=(0,(4,2)), alpha=0.95),
        zorder=6
    )

    # ── Reasoning quality ribbon ──
    ribbon_y = -0.018
    ribbon_h = 0.010
    for p in GT_PEAKS:
        # fraction of models with correct assignment at this peak
        n_ok = sum(1 for m in models
                   if any(a[0]==p["name"] and a[2] for a in m.get("peak_assigns",[])))
        frac_ok  = n_ok / len(models)
        frac_bad = 1 - frac_ok
        x_c = p["pos"]
        w   = p["gamma"] * 3.6
        ax.barh(ribbon_y, w * frac_ok,  left=x_c - w/2,
                height=ribbon_h, color=C["correct"], alpha=0.75)
        ax.barh(ribbon_y, w * frac_bad, left=x_c - w/2 + w*frac_ok,
                height=ribbon_h, color=C["wrong"], alpha=0.65)

    ax.text(1155, ribbon_y + ribbon_h/2, "reasoning quality",
            fontsize=5, color=C["muted"], va="center")

    _panel_label(ax, "c")
    ax.set_title("Reasoning-chain overlay", fontsize=8,
                 fontweight="semibold", pad=4, color=C["text"])


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL D  — Error taxonomy + Confidence calibration
# ══════════════════════════════════════════════════════════════════════════════

def draw_panel_D(ax_tax, ax_cal, models):

    # ── D-left: error taxonomy ─────────────────────────────────────────────
    sorted_m = sorted(models, key=lambda m: m["elo"], reverse=True)
    n        = len(sorted_m)
    elo_vals = [m["elo"] for m in sorted_m]
    elo_min, elo_max = min(elo_vals), max(elo_vals)

    for i, m in enumerate(sorted_m):
        y = n - 1 - i          # top = highest ELO
        col = model_color(m)
        # ELO label on left
        ax_tax.text(-0.5, y, f"{m['id']}", ha="right", va="center",
                    fontsize=8, fontweight="bold", color=col)
        ax_tax.text(-1.8, y, f"{m['elo']}", ha="right", va="center",
                    fontsize=5.5, color=C["muted"])

        # Error blocks
        x_off = 0
        bw    = len(ERROR_TYPES)  # full width = n error types
        for ei, et in enumerate(ERROR_TYPES):
            if et in m.get("errors", []):
                ax_tax.barh(y, 1, left=x_off, height=0.72,
                            color=ERROR_COLORS[ei], alpha=0.85)
            x_off += 1

        # thin separator line
        ax_tax.axhline(y - 0.5, color=C["grid"], lw=0.4)

    ax_tax.set_xlim(-2, len(ERROR_TYPES))
    ax_tax.set_ylim(-0.6, n - 0.4)
    ax_tax.set_xticks([])
    ax_tax.set_yticks([])
    ax_tax.spines["left"].set_visible(False)
    ax_tax.spines["bottom"].set_visible(False)
    ax_tax.set_title("Error taxonomy", fontsize=8,
                     fontweight="semibold", pad=4, color=C["text"])

    # legend
    patches = [mpatches.Patch(color=ERROR_COLORS[i], label=ERROR_LABELS[i].replace("\n"," "),
                               alpha=0.85)
               for i in range(len(ERROR_TYPES))]
    ax_tax.legend(handles=patches, fontsize=5.2, frameon=False,
                  loc="lower center", bbox_to_anchor=(0.5, -0.22),
                  ncol=3, handlelength=1, handletextpad=0.4, columnspacing=0.6)

    _panel_label(ax_tax, "d")

    # ELO rank arrow on right
    ax_tax.annotate("", xy=(len(ERROR_TYPES)+0.3, n-0.8),
                    xytext=(len(ERROR_TYPES)+0.3, 0.2),
                    arrowprops=dict(arrowstyle="-|>", color=C["muted"],
                                   lw=0.7, mutation_scale=7))
    ax_tax.text(len(ERROR_TYPES)+0.5, n/2, "ELO rank",
                fontsize=5.5, color=C["muted"], rotation=90, va="center")

    # ── D-right: confidence calibration ───────────────────────────────────
    bins       = np.arange(0.55, 1.05, 0.10)
    bin_mids   = bins[:-1] + 0.05
    accs, cnts = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        in_bin = [m for m in models if lo <= m["conf"] < hi]
        cnts.append(len(in_bin))
        if in_bin:
            ok = [m for m in in_bin
                  if "graphene" in m["mat"].lower() and m["layers"] == GT_LAYERS]
            accs.append(len(ok) / len(in_bin))
        else:
            accs.append(np.nan)

    # perfect calibration diagonal
    ax_cal.plot([0.5, 1.0], [0.5, 1.0], color=C["grid"], lw=0.9, ls="--",
                zorder=1, label="Perfect calibration")

    # overconfidence shading
    ax_cal.fill_between([0.5,1.0], [0.5,1.0], [0,0.5],
                        color=C["wrong"], alpha=0.04, zorder=0)
    ax_cal.text(0.87, 0.20, "over-confident", fontsize=5.5,
                color=C["wrong"], alpha=0.6, ha="center")

    # calibration curve
    valid = [(x, y) for x, y in zip(bin_mids, accs) if not np.isnan(y)]
    if valid:
        xs, ys = zip(*valid)
        ax_cal.plot(xs, ys, color=C["navy"], lw=1.4, marker="o",
                    ms=4, zorder=3, label="Models (this sample)")
        # count annotations
        for xi, yi, cnt in zip(bin_mids, accs, cnts):
            if not np.isnan(yi) and cnt > 0:
                ax_cal.text(xi, yi + 0.04, f"n={cnt}",
                            fontsize=5, color=C["muted"], ha="center")

    ax_cal.set_xlim(0.55, 1.02)
    ax_cal.set_ylim(0, 1.08)
    ax_cal.set_xlabel("Stated confidence", fontsize=8)
    ax_cal.set_ylabel("Empirical accuracy", fontsize=8)
    ax_cal.tick_params(labelsize=7)
    ax_cal.legend(fontsize=5.5, frameon=False, loc="upper left",
                  handlelength=1.2)
    ax_cal.set_title("Confidence calibration", fontsize=8,
                     fontweight="semibold", pad=4, color=C["text"])


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def _panel_label(ax, label):
    ax.text(-0.10, 1.05, label, transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=C["text"],
            va="top", ha="left")

def _panel_label_ax(ax, label, x=0.01, y=0.97):
    ax.text(x, y, label, transform=ax.transAxes,
            fontsize=11, fontweight="bold", color=C["text"],
            va="top", ha="left")

def _wrap(text, width=44):
    """Naive word-wrap for annotation text."""
    words, line, lines = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 <= width:
            line = (line + " " + w).lstrip()
        else:
            if line: lines.append(line)
            line = w
    if line: lines.append(line)
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
#  ASSEMBLE FIGURE
# ══════════════════════════════════════════════════════════════════════════════

def build_figure():
    x, raw, den = load_spectrum()
    peaks        = load_peaks()
    models       = load_models()

    fig = plt.figure(figsize=(11.8, 7.8), facecolor=C["bg"])
    fig.patch.set_facecolor(C["bg"])

    # Grid: 2 rows × 3 cols top; 1 row × 2 cols bottom
    # Use nested GridSpec for fine control
    outer = GridSpec(2, 1, figure=fig, hspace=0.46,
                     top=0.93, bottom=0.09, left=0.07, right=0.97)

    top_gs = outer[0].subgridspec(1, 3, wspace=0.42)
    bot_gs = outer[1].subgridspec(1, 2, wspace=0.44, width_ratios=[1.15, 1])

    ax_A = fig.add_subplot(top_gs[0])
    ax_B = fig.add_subplot(top_gs[1])
    ax_C = fig.add_subplot(top_gs[2])

    # Bottom-left: taxonomy needs its own split
    bot_left  = bot_gs[0].subgridspec(1, 1)
    ax_D_tax  = fig.add_subplot(bot_left[0])
    ax_D_cal  = fig.add_subplot(bot_gs[1])

    # Set background on all axes
    for ax in [ax_A, ax_B, ax_C, ax_D_tax, ax_D_cal]:
        ax.set_facecolor(C["bg"])

    # Draw panels
    draw_panel_A(ax_A, x, raw, den, peaks)
    draw_panel_B(ax_B, models)
    draw_panel_C(ax_C, x, den, models)
    draw_panel_D(ax_D_tax, ax_D_cal, models)

    # ── Figure-level title & caption ──────────────────────────────────────
    fig.text(0.5, 0.965,
             "Figure 3  |  Single-sample LLM benchmark evaluation  ·  Graphene",
             ha="center", va="top", fontsize=9, fontweight="bold", color=C["text"])

    caption = (
        r"$\bf{a}$, Denoised Raman spectrum (sample_a; graphene monolayer ground-truth); "
        r"shaded regions = extracted peak extents; FWHM in parentheses; validity bars below x-axis. "
        r"$\bf{b}$, Model–peak agreement network; inner nodes = graphene peaks (D, G, D$'$, 2D); "
        r"outer nodes = model letters a–i (size $\propto$ ELO); edge colour encodes assignment correctness "
        r"(teal: correct; amber: uncertain; crimson: hallucinated); consensus bars indicate % of models correct per peak. "
        r"$\bf{c}$, Reasoning-chain overlay; callout boxes contrast best-ranked (solid border) and worst-ranked "
        r"(dashed border) model reasoning; ribbon = per-peak reasoning quality across models. "
        r"$\bf{d}$, Left: error taxonomy for all 9 models ranked by ELO (six error categories); "
        r"right: confidence calibration curve vs. perfect-calibration diagonal (n = models per bin)."
    )
    fig.text(0.5, 0.025, caption, ha="center", va="bottom",
             fontsize=5.8, color=C["muted"], wrap=True,
             multialignment="center",
             transform=fig.transFigure,
             linespacing=1.5)

    return fig


if __name__ == "__main__":
    fig = build_figure()
    out = "/Users/sutharsikakumar/raman-arena/raman_benchmark_figure.pdf"
    fig.savefig(out, format="pdf", bbox_inches="tight", facecolor=C["bg"])
    # Also save high-res PNG for preview
    fig.savefig(out.replace(".pdf", ".png"), format="png",
                dpi=300, bbox_inches="tight", facecolor=C["bg"])
    print(f"Saved: {out}")
    plt.close(fig)