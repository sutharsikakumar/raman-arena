"""
============================================================
  GRAPHENE ELO RANKING SYSTEM
  Judge: grok-4.20-0309-reasoning  (xAI API, OpenAI-compatible)
  Material: Graphene (mono_g_cu_001)
  Folder: ranking_sample_a / subfolders a–i
  Each subfolder: chain_of_thought.json + classification_result.json
============================================================
"""

from __future__ import annotations
import argparse
import json
import pathlib
import itertools
import re
import os
import textwrap
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

K_FACTOR    = 16          # gentler K for 0–100 range
START_ELO   = 50.0        # midpoint of 0–100 scale
ELO_MIN     = 0.0
ELO_MAX     = 100.0
MODEL       = "grok-4.20-0309-reasoning"
XAI_BASE    = "https://api.x.ai/v1"

# ── Hard-coded ground truth about the graphene sample ──────────────────────────
GRAPHENE_GROUND_TRUTH = """
GROUND TRUTH — Graphene Sample (mono_g_cu_001)
===============================================
Sample type       : Monolayer graphene grown by CVD on copper foil (Cu 001)
Abbreviation      : mono_g_cu_001

Expected Raman signature
  D  band  (~1350 cm⁻¹) : Defect-activated; should be LOW or absent in
                           high-quality monolayer graphene.
  G  band  (~1580 cm⁻¹) : E₂g phonon at Γ point; should be present and
                           moderately intense.
  2D band  (~2700 cm⁻¹) : Overtone of D; DOMINANT peak for monolayer —
                           I(2D)/I(G) > 2 is the canonical monolayer criterion.
  D' band  (~1620 cm⁻¹) : Defect-related shoulder on G; should be absent
                           in pristine graphene.

Key quality indicators
  • 2D peak: single Lorentzian, FWHM ≈ 25–35 cm⁻¹ for monolayer
  • I(2D)/I(G) ratio > 2 confirms monolayer character
  • Low D-band intensity → minimal defect density
  • G-band position ~1580 cm⁻¹ (strain shifts it slightly)
  • No D' band → absence of edge/grain-boundary defects

Classification target : GRAPHENE (monolayer)
Substrate            : Copper (Cu), orientation 001
"""

# ─────────────────────────────────────────────
#  ELO EVALUATION PROMPT  (Chain-of-Thought)
# ─────────────────────────────────────────────
EVAL_PROMPT = textwrap.dedent("""
You are an expert in Raman spectroscopy and 2-D materials science, tasked with
judging two AI model outputs that both attempted to classify and analyse the
*same* graphene Raman spectrum.

══════════════════════════════════════════════════════
  GROUND TRUTH (use this as the reference standard)
══════════════════════════════════════════════════════
{ground_truth}

══════════════════════════════════════════════════════
  CANDIDATE A  (model folder: {a_name})
══════════════════════════════════════════════════════
--- chain_of_thought.json ---
{a_cot}

--- classification_result.json ---
{a_result}

══════════════════════════════════════════════════════
  CANDIDATE B  (model folder: {b_name})
══════════════════════════════════════════════════════
--- chain_of_thought.json ---
{b_cot}

--- classification_result.json ---
{b_result}

══════════════════════════════════════════════════════
  YOUR EVALUATION TASK
══════════════════════════════════════════════════════
Step 1 – Scientific correctness
  • Did each candidate correctly identify the material as graphene (monolayer)?
  • Did they correctly identify the G, 2D (and optionally D) bands?
  • Are the reported peak positions, intensities, and ratios consistent with
    the ground truth? Flag any errors.

Step 2 – Reasoning quality (chain-of-thought)
  • Is the reasoning methodical, logically structured, and grounded in Raman
    physics?
  • Does the chain-of-thought lead coherently to the final classification?
  • Penalise hallucinations, circular reasoning, or missing steps.

Step 3 – Completeness & clarity of classification result
  • Does the final classification result clearly state: material, confidence,
    key evidence (peak ratios, band assignments)?
  • Is the uncertainty/confidence appropriately quantified?
  • Is the explanation concise yet thorough?

Step 4 – Holistic comparison
  • Weigh all three dimensions and decide which candidate is BETTER OVERALL.
  • If they are genuinely equal on every dimension, you may declare a draw.

══════════════════════════════════════════════════════
  RESPOND ONLY WITH VALID JSON — NO OTHER TEXT
══════════════════════════════════════════════════════
{{
  "thinking_summary": "<3-5 sentences summarising your step-by-step reasoning>",
  "step1_correctness": {{
    "A": "<brief verdict for A>",
    "B": "<brief verdict for B>"
  }},
  "step2_reasoning": {{
    "A": "<brief verdict for A>",
    "B": "<brief verdict for B>"
  }},
  "step3_completeness": {{
    "A": "<brief verdict for A>",
    "B": "<brief verdict for B>"
  }},
  "winner": "A" | "B" | "draw",
  "confidence": <float 0.0–1.0>,
  "justification": "<2-3 sentence final justification>"
}}
""").strip()


# ─────────────────────────────────────────────
#  ELO PLAYER
# ─────────────────────────────────────────────
class EloPlayer:
    def __init__(self, name: str):
        self.name    = name
        self.rating  = START_ELO
        self.wins:   List[str]   = []
        self.losses: List[str]   = []
        self.draws:  List[str]   = []
        self.history: List[Dict] = []

    def expected(self, opp: "EloPlayer") -> float:
        return 1 / (1 + 10 ** ((opp.rating - self.rating) / 400))

    def update(self, opp: "EloPlayer", score: float):
        """score: 1=win, 0.5=draw, 0=loss"""
        exp = self.expected(opp)
        delta = K_FACTOR * (score - exp)
        self.rating = max(ELO_MIN, min(ELO_MAX, self.rating + delta))


# ─────────────────────────────────────────────
#  LOAD MODELS
# ─────────────────────────────────────────────
def load_models(root: pathlib.Path) -> Dict[str, Dict]:
    """
    Expect: root/ranking_sample_a/{a,b,c,...}/
               chain_of_thought.json
               classification_result.json
    """
    sample_dir = root / "ranking_sample_a"
    if not sample_dir.is_dir():
        raise ValueError(f"Cannot find folder: {sample_dir}")

    data: Dict[str, Dict] = {}
    for sub in sorted(sample_dir.iterdir()):
        if not sub.is_dir():
            continue

        cot_path    = sub / "chain_of_thought.json"
        result_path = sub / "classification_result.json"

        # Allow one level of nesting (unnamed inner folder)
        if not cot_path.exists():
            inner_dirs = [d for d in sub.iterdir() if d.is_dir()]
            if inner_dirs:
                inner       = inner_dirs[0]
                cot_path    = inner / "chain_of_thought.json"
                result_path = inner / "classification_result.json"

        if not cot_path.exists() or not result_path.exists():
            print(f"  [SKIP] {sub.name}: missing json files")
            continue

        try:
            with open(cot_path)    as f: cot    = json.load(f)
            with open(result_path) as f: result = json.load(f)
            data[sub.name] = {
                "cot":    json.dumps(cot,    indent=2),
                "result": json.dumps(result, indent=2),
            }
            print(f"  [OK]   {sub.name}")
        except Exception as e:
            print(f"  [ERR]  {sub.name}: {e}")

    if len(data) < 2:
        raise ValueError(f"Need at least 2 models; found {len(data)}.")
    return data


# ─────────────────────────────────────────────
#  CALL GROK  (xAI OpenAI-compatible API)
# ─────────────────────────────────────────────
def call_grok(client: OpenAI, prompt: str) -> Dict:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    text = resp.choices[0].message.content.strip()

    # Strip markdown fences if present
    for marker in ["```json", "```"]:
        if marker in text:
            start = text.find(marker) + len(marker)
            end   = text.find("```", start)
            if end != -1:
                text = text[start:end].strip()
                break

    result = json.loads(text)
    if "confidence" not in result:
        result["confidence"] = 0.5
    return result


# ─────────────────────────────────────────────
#  RUN GAMES
# ─────────────────────────────────────────────
def run_games(
    data: Dict[str, Dict],
    out_dir: pathlib.Path,
    client: OpenAI,
):
    out_dir.mkdir(parents=True, exist_ok=True)
    players = {name: EloPlayer(name) for name in data}
    names   = sorted(players.keys())
    pairs   = list(itertools.combinations(names, 2))

    print("\n" + "=" * 64)
    print(" GRAPHENE ELO RANKING SYSTEM")
    print(f" Models : {len(players)}   →   {len(pairs)} head-to-head games")
    print(f" Judge  : {MODEL}")
    print(f" ELO    : {ELO_MIN}–{ELO_MAX}, start={START_ELO}")
    print("=" * 64 + "\n")

    all_games = []

    for game_id, (a_name, b_name) in enumerate(pairs, 1):
        a, b = players[a_name], players[b_name]

        prompt = EVAL_PROMPT.format(
            ground_truth = GRAPHENE_GROUND_TRUTH,
            a_name       = a_name,
            a_cot        = data[a_name]["cot"],
            a_result     = data[a_name]["result"],
            b_name       = b_name,
            b_cot        = data[b_name]["cot"],
            b_result     = data[b_name]["result"],
        )

        print(f"Game {game_id:3d}/{len(pairs)}: {a_name:<4} vs {b_name:<4}", end="  ", flush=True)

        try:
            judgment = call_grok(client, prompt)
        except Exception as e:
            print(f"→ API ERROR: {e}")
            continue

        winner_raw    = str(judgment.get("winner", "")).strip().upper()
        confidence    = float(judgment.get("confidence", 0.5))
        justification = judgment.get("justification", "")

        old_a, old_b = a.rating, b.rating

        if winner_raw == "A":
            a.update(b, 1.0); b.update(a, 0.0)
            winner_name = a_name
            a.wins.append(b_name); b.losses.append(a_name)
            outcome = f"{a_name} wins"
        elif winner_raw == "B":
            a.update(b, 0.0); b.update(a, 1.0)
            winner_name = b_name
            b.wins.append(a_name); a.losses.append(b_name)
            outcome = f"{b_name} wins"
        elif winner_raw == "DRAW":
            a.update(b, 0.5); b.update(a, 0.5)
            winner_name = "draw"
            a.draws.append(b_name); b.draws.append(a_name)
            outcome = "draw"
        else:
            print(f"→ BAD WINNER: {winner_raw}")
            continue

        delta_a = a.rating - old_a
        delta_b = b.rating - old_b
        print(f"→ {outcome:<12}  conf={confidence:.2f}  "
              f"{a_name}:{a.rating:.1f}({delta_a:+.1f})  "
              f"{b_name}:{b.rating:.1f}({delta_b:+.1f})")

        game_record = {
            "game_id":       game_id,
            "model_a":       a_name,
            "model_b":       b_name,
            "winner":        winner_raw,
            "winner_name":   winner_name,
            "confidence":    confidence,
            "justification": justification,
            "step1":         judgment.get("step1_correctness", {}),
            "step2":         judgment.get("step2_reasoning", {}),
            "step3":         judgment.get("step3_completeness", {}),
            "thinking":      judgment.get("thinking_summary", ""),
            "elo_before":    {a_name: round(old_a, 2), b_name: round(old_b, 2)},
            "elo_after":     {a_name: round(a.rating, 2), b_name: round(b.rating, 2)},
        }
        all_games.append(game_record)

        safe  = lambda s: re.sub(r"[^\w\-]", "_", s)
        gfile = out_dir / f"game_{game_id:03d}_{safe(a_name)}_vs_{safe(b_name)}.json"
        with open(gfile, "w") as f:
            json.dump(game_record, f, indent=2)

    # ── Final ranking ────────────────────────────────────────────────────────
    ranking = sorted(players.values(), key=lambda p: p.rating, reverse=True)

    print("\n" + " FINAL RANKING ".center(64, "="))
    for i, p in enumerate(ranking, 1):
        w, d, l = len(p.wins), len(p.draws), len(p.losses)
        print(f"  {i:2d}. {p.name:<6}  ELO={p.rating:5.1f}  {w}W-{d}D-{l}L")

    # ── Save markdown report ─────────────────────────────────────────────────
    md = _build_report(ranking, all_games, len(pairs))
    with open(out_dir / "FINAL_RANKING.md", "w") as f:
        f.write(md)

    # ── Save all games JSON ──────────────────────────────────────────────────
    with open(out_dir / "all_games.json", "w") as f:
        json.dump(all_games, f, indent=2)

    # ── Plot ─────────────────────────────────────────────────────────────────
    _plot(ranking, out_dir)

    print(f"\n✓ Done. Results saved to: {out_dir.resolve()}")


# ─────────────────────────────────────────────
#  REPORT BUILDER
# ─────────────────────────────────────────────
def _build_report(
    ranking: List[EloPlayer],
    games: List[Dict],
    total_games: int,
) -> str:
    lines = [
        "# Graphene ELO Ranking — Final Report",
        "",
        f"**Sample:** mono_g_cu_001 (Monolayer graphene on Cu)  ",
        f"**Judge:** {MODEL}  ",
        f"**ELO range:** {ELO_MIN}–{ELO_MAX} · Start: {START_ELO} · K={K_FACTOR}  ",
        f"**Total games played:** {total_games}  ",
        "",
        "## Ground Truth",
        "```",
        GRAPHENE_GROUND_TRUTH.strip(),
        "```",
        "",
        "## Final Rankings",
        "",
        "| Rank | Model | ELO | W | D | L | Win% |",
        "|------|-------|-----|---|---|---|------|",
    ]
    for i, p in enumerate(ranking, 1):
        w, d, l = len(p.wins), len(p.draws), len(p.losses)
        total = w + d + l or 1
        pct   = f"{100*(w + 0.5*d)/total:.0f}%"
        lines.append(f"| {i} | **{p.name}** | {p.rating:.1f} | {w} | {d} | {l} | {pct} |")

    lines += ["", "## Match Results", ""]
    for g in games:
        w    = g["winner_name"]
        conf = g["confidence"]
        lines.append(
            f"- **Game {g['game_id']}** · {g['model_a']} vs {g['model_b']} → "
            f"**{w}** wins (conf={conf:.2f})  "
        )
        if g.get("justification"):
            lines.append(f"  *{g['justification']}*")
        lines.append("")

    return "\n".join(lines)


# ─────────────────────────────────────────────
#  PLOT
# ─────────────────────────────────────────────
def _plot(ranking: List[EloPlayer], out_dir: pathlib.Path):
    names   = [p.name   for p in ranking]
    ratings = [p.rating for p in ranking]
    wins    = [len(p.wins)   for p in ranking]
    losses  = [len(p.losses) for p in ranking]
    draws   = [len(p.draws)  for p in ranking]

    n = len(names)
    x = np.arange(n)

    palette = []
    for i in range(n):
        if   i == 0: palette.append("#FFD700")
        elif i == 1: palette.append("#C0C0C0")
        elif i == 2: palette.append("#CD7F32")
        else:        palette.append("#4C8BB5")

    fig, axes = plt.subplots(
        2, 1, figsize=(max(10, n * 1.1), 11),
        gridspec_kw={"height_ratios": [3, 1.2]}
    )
    fig.patch.set_facecolor("#0D1117")
    for ax in axes:
        ax.set_facecolor("#161B22")
        for spine in ax.spines.values():
            spine.set_edgecolor("#30363D")

    # ── Top plot: ELO bars ───────────────────────────────────────────────────
    ax = axes[0]
    bars = ax.bar(x, ratings, color=palette, edgecolor="#30363D", linewidth=0.8, zorder=3)
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=12, color="white", fontweight="bold")
    ax.set_ylabel("ELO Rating", fontsize=12, color="#8B949E")
    ax.set_title(
        "Graphene Classification — ELO Rankings\n"
        f"Sample: mono_g_cu_001 · Judge: {MODEL}",
        fontsize=14, color="white", pad=14, fontweight="bold"
    )
    ax.tick_params(colors="#8B949E")
    ax.yaxis.set_tick_params(labelcolor="#8B949E")
    ax.grid(axis="y", color="#30363D", linewidth=0.6, zorder=0)
    ax.axhline(START_ELO, color="#F78166", linewidth=1.2,
               linestyle="--", zorder=2, label=f"Start ELO ({START_ELO})")
    ax.legend(fontsize=9, facecolor="#21262D", edgecolor="#30363D",
              labelcolor="white", loc="upper right")

    for bar, rating, name, rank in zip(bars, ratings, names, range(1, n + 1)):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.0,
            f"{rating:.1f}",
            ha="center", va="bottom", fontsize=11, color="white", fontweight="bold"
        )
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")
        if medal:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() / 2,
                medal, ha="center", va="center", fontsize=16
            )

    # ── Bottom plot: W/D/L stacked bars ─────────────────────────────────────
    ax2 = axes[1]
    ax2.bar(x, wins,  color="#3FB950", edgecolor="#30363D", label="Wins",  zorder=3)
    ax2.bar(x, draws, bottom=wins,
            color="#E3B341", edgecolor="#30363D", label="Draws", zorder=3)
    l_bot = [w + d for w, d in zip(wins, draws)]
    ax2.bar(x, losses, bottom=l_bot,
            color="#F85149", edgecolor="#30363D", label="Losses", zorder=3)

    ax2.set_xlim(-0.6, n - 0.4)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, fontsize=11, color="white")
    ax2.set_ylabel("Games", fontsize=11, color="#8B949E")
    ax2.set_title("Win / Draw / Loss per Model", fontsize=12, color="white", pad=8)
    ax2.tick_params(colors="#8B949E")
    ax2.yaxis.set_tick_params(labelcolor="#8B949E")
    ax2.grid(axis="y", color="#30363D", linewidth=0.6, zorder=0)
    ax2.legend(
        fontsize=9, facecolor="#21262D", edgecolor="#30363D",
        labelcolor="white", loc="upper right", ncol=3
    )

    plt.tight_layout(pad=2.5)
    chart_path = out_dir / "ELO_RANKING_CHART.png"
    plt.savefig(chart_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Chart saved → {chart_path}")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    load_dotenv()
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "XAI_API_KEY not found in environment / .env file."
        )

    parser = argparse.ArgumentParser(
        description="Graphene ELO ranking — Grok judge (xAI)"
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path("."),
        help="Folder that contains 'ranking_sample_a/' (default: current dir)"
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path("graphene_elo_results"),
        help="Where to write results (default: ./graphene_elo_results)"
    )
    args = parser.parse_args()

    client = OpenAI(
        api_key=api_key,
        base_url=XAI_BASE,
    )

    print("Loading models...")
    data = load_models(args.root)
    print(f"Loaded {len(data)} models: {', '.join(sorted(data.keys()))}\n")

    run_games(data, args.output, client)


if __name__ == "__main__":
    main()