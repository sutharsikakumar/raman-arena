import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

def generate_compact_pub_figure():
    # Set standard academic style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(14, 8), facecolor='#121212') # Pure dark mode
    ax = fig.add_subplot(111)
    ax.axis('off')

    # --- BRANDED COLOR PALETTE ---
    C_TEXT = "#E0E0E0"
    C_HEADER = "#A2D9CE"     # Teal Mint
    C_SUB_HEADER = "#D4AC0D" # Gold
    C_BOX_EDGE = "#F9E79F"   # Soft Gold
    C_BOX_BG = "#1F1F1F"     # Slightly lighter dark box
    C_LM_BOX = "#FFF9E5"    # Original beige/cream
    C_LM_TEXT = "#2C3E50"    # Dark slate for contrast in cream boxes

    # 1. Main Figure Title
    plt.text(0.5, 0.96, "LLM-JUDGE: ELO EVAL PROMPT STRUCTURE", ha="center", 
             fontsize=18, fontweight="black", color=C_TEXT, letterspacing=2)

    # 2. LM Prompt (Hydration & Node Logic)
    prompt_w, prompt_h = 0.45, 0.75
    rect_p = patches.RoundedRectangle((0.02, 0.08), prompt_w, prompt_h, 
                                     lw=1.5, edgecolor=C_BOX_EDGE, facecolor=C_BOX_BG)
    ax.add_patch(rect_p)
    
    # Sub-Headers in Gold
    plt.text(0.04, 0.82, "[INPUTS] PROMPT HYDRATION", fontsize=11, color=C_SUB_HEADER, weight='bold')
    plt.text(0.04, 0.50, "[KERNEL] LLM REASONING FLOW", fontsize=11, color=C_SUB_HEADER, weight='bold')

    # Example Prompt Injections (Using Courier for code feel)
    prompt_props = dict(boxstyle='round,pad=1', facecolor=C_LM_BOX, edgecolor=C_BOX_EDGE, alpha=1)
    
    p_injection = "PROMPT = f'''\n... Analyze standard ...\n\n[DIAGNOSTICS]:\n    {diag_json}\n\n[PEAKS]:\n    {peak_table}\n'''"
    ax.text(0.04, 0.65, f"Input Data Injected:\n\n{p_injection}", 
            family='monospace', fontsize=10, verticalalignment='top', bbox=prompt_props, color=C_LM_TEXT)

    # Key Evaluation Logic (Simplified)
    ax.text(0.04, 0.15, textwrap.fill("EVALUATION CRITERIA:\n- Validated Correctness (correct phase? layer?)\n- Stacking Order Validation (AB/AA' order?)\n- Reasoning Depth (concise fact bullet counts?)\n- Verification (output references peaks by shift?)", width=45), 
            family='monospace', fontsize=9.5, verticalalignment='top', bbox=prompt_props, color=C_LM_TEXT)

    # 3. Aggregation & Consensus (Matching Lighter Figure Logic)
    consensus_w, consensus_h = 0.45, 0.35
    rect_c = patches.RoundedRectangle((0.52, 0.48), consensus_w, consensus_h, 
                                     lw=1.5, edgecolor=C_HEADER, facecolor=C_BOX_BG)
    ax.add_patch(rect_c)

    plt.text(0.54, 0.82, "[KERNEL] JUDGE CONSENSUS VOTE", fontsize=11, color=C_HEADER, weight='bold')
    
    # Sampling Multiple Judge Paths (CoT Self-Consistency)
    c_props = dict(boxstyle='round,pad=1', facecolor='#D5F5E3', edgecolor=C_HEADER, alpha=1) # Soft Green
    ax.text(0.54, 0.65, "VOTING PATHS (CoT):\n1. Verified AB Stacking [WIN]\n2. Incorrect Phase [LOSS]\n3. True Mono-layer [WIN]", 
            family='monospace', fontsize=10, verticalalignment='top', bbox=c_props, color=C_LM_TEXT)

    # 4. JSON Schema & Elo Update
    output_w, output_h = 0.45, 0.35
    rect_o = patches.RoundedRectangle((0.52, 0.08), output_w, output_h, 
                                     lw=1.5, edgecolor=C_BOX_EDGE, facecolor=C_BOX_BG)
    ax.add_patch(rect_o)
    
    plt.text(0.54, 0.42, "[OUTPUT] STRUCTURED CONSENSUS JSON", fontsize=11, color=C_SUB_HEADER, weight='bold')

    o_props = dict(boxstyle='round,pad=1', facecolor='#FADBD8', edgecolor='#E74C3C', alpha=1) # Soft Red
    o_schema = '{\n  "winner": "silicon",\n  "confidence": 0.95,\n  "stacking_ok": true,\n  "new_elo": +12\n}'
    ax.text(0.54, 0.25, f"Validated JSON Response:\n\n{o_schema}", 
            family='monospace', fontsize=10, verticalalignment='top', bbox=o_props, color=C_LM_TEXT)

    # Add descriptive arrow connecting Kernels
    ax.annotate('CONSENSUS VOTE', xy=(0.7, 0.52), xytext=(0.3, 0.52),
                ha='center', va='center', fontsize=10, fontweight='bold', color=C_HEADER,
                bbox=dict(boxstyle="larrow,pad=0.5", fc=C_BOX_BG, ec=C_HEADER, lw=1.5))

    plt.show()