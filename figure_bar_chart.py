"""
ELO Rankings — vertical grouped bars, default matplotlib font,
palette: #F26076, #FF9760, #FFD150, #458B73
Run: python elo_figure_final.py
Outputs: elo_main.png, elo_wdl.png (+ .pdf)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Palette from screenshot 2 ─────────────────────────────────────────────────
C_MOS2     = '#FFD150'   # yellow
C_GRAPHENE = '#458B73'   # teal green
C_HBN      = '#F26076'   # coral/pink-red
C_WSE2     = '#FF9760'   # orange

SAMPLE_LABELS = ['MoS\u2082', 'Graphene', 'h-BN', 'WSe\u2082']
COLORS        = [C_MOS2, C_GRAPHENE, C_HBN, C_WSE2]
MODEL_LETTERS = list('abcdefghi')

WIN_C  = '#458B73'
DRAW_C = '#FFD150'
LOSS_C = '#F26076'

# ── Data ──────────────────────────────────────────────────────────────────────
elo_data = {
    'a': [ 51.4,  36.1,  14.2,   6.4],
    'b': [ 79.2,  65.6,  95.2,  57.2],
    'c': [100.0,  78.9,  51.2,  65.1],
    'd': [ 21.3,  14.2, 100.0,  44.2],
    'e': [ 56.5,  93.0,  64.2, 100.0],
    'f': [ 43.4, 100.0,  78.5,  99.9],
    'g': [  0.0,   0.0,   0.0,   5.6],
    'h': [ 93.2,  14.3,  27.9,   6.5],
    'i': [  7.4,  50.7,  21.9,  64.1],
}

wdl_data = {
    'a': {'w': [4, 3, 1, 0], 'd': [0, 0, 1, 2], 'l': [4, 5, 6, 6]},
    'b': {'w': [6, 5, 7, 4], 'd': [0, 0, 0, 1], 'l': [2, 3, 1, 3]},
    'c': {'w': [8, 6, 4, 4], 'd': [0, 0, 0, 2], 'l': [0, 2, 4, 2]},
    'd': {'w': [2, 1, 8, 3], 'd': [0, 1, 0, 1], 'l': [6, 6, 0, 4]},
    'e': {'w': [4, 7, 5, 7], 'd': [1, 0, 0, 1], 'l': [3, 1, 3, 0]},
    'f': {'w': [3, 8, 6, 7], 'd': [1, 0, 0, 1], 'l': [4, 0, 2, 0]},
    'g': {'w': [0, 0, 0, 0], 'd': [0, 0, 0, 2], 'l': [8, 8, 8, 6]},
    'h': {'w': [7, 1, 2, 0], 'd': [0, 1, 1, 2], 'l': [1, 6, 5, 6]},
    'i': {'w': [1, 4, 1, 4], 'd': [0, 0, 2, 2], 'l': [7, 4, 5, 2]},
}

N = len(MODEL_LETTERS)
S = len(SAMPLE_LABELS)


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 1 — ELO Rankings (single panel, grouped vertical bars)
# ═══════════════════════════════════════════════════════════════════════════
def make_elo_figure():
    fig, ax = plt.subplots(figsize=(13, 6), facecolor='white')

    bar_w     = 0.18
    group_gap = 0.08
    group_w   = S * bar_w + group_gap
    xs        = np.arange(N) * group_w

    for s_idx, (sample, color) in enumerate(zip(SAMPLE_LABELS, COLORS)):
        offsets = xs + s_idx * bar_w
        elos    = [elo_data[m][s_idx] for m in MODEL_LETTERS]

        bars = ax.bar(
            offsets, elos,
            width=bar_w * 0.88,
            color=color,
            edgecolor='white',
            linewidth=0.6,
            alpha=0.88,
            label=sample,
            zorder=3,
        )

        for bar, elo in zip(bars, elos):
            if elo > 1:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1.5,
                    f'{elo:.0f}',
                    ha='center', va='bottom',
                    fontsize=7.2, color='#333333',
                )

    tick_pos = xs + (S * bar_w) / 2 - bar_w / 2
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(MODEL_LETTERS, fontsize=12, fontweight='bold')

    ax.axhline(50, color='#aaaaaa', lw=1.0, ls='--', zorder=2)
    ax.text(xs[-1] + S * bar_w - 0.05, 51.5, 'Start ELO (50)',
            va='bottom', ha='right', fontsize=8, color='#aaaaaa', style='italic')

    ax.set_xlabel('Model', fontsize=11, labelpad=6)
    ax.set_ylabel('ELO Rating', fontsize=11, labelpad=6)
    ax.set_title(
        'Raman Classification ELO Rankings by Model\n'
        'Judge: claude-sonnet-4-6 with extended thinking',
        fontsize=12, pad=10,
    )

    ax.set_xlim(-0.15, xs[-1] + S * bar_w + 0.1)
    ax.set_ylim(0, 118)
    ax.yaxis.grid(True, color='#e8e8e8', lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    legend_patches = [
        mpatches.Patch(color=color, alpha=0.88, label=sample)
        for color, sample in zip(COLORS, SAMPLE_LABELS)
    ]
    ax.legend(
        handles=legend_patches,
        title='Sample',
        title_fontsize=9,
        fontsize=9,
        loc='upper right',
        framealpha=0.9,
        edgecolor='#cccccc',
    )

    fig.tight_layout()
    plt.savefig('elo_main.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('elo_main.pdf', dpi=300, bbox_inches='tight', facecolor='white')
    print("Saved: elo_main.png / elo_main.pdf")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 2 — W/D/L breakdown (4 horizontal stacked-bar panels, 1x4)
# ═══════════════════════════════════════════════════════════════════════════
def make_wdl_figure():
    fig, axes = plt.subplots(
        1, 4,
        figsize=(18, 5.5),
        facecolor='white',
        sharey=True,
    )
    fig.subplots_adjust(wspace=0.18, left=0.06, right=0.97, top=0.87, bottom=0.11)

    panel_labels = ['a)', 'b)', 'c)', 'd)']

    for ax, s_idx, label_str, panel_lbl in zip(
            axes, range(4), SAMPLE_LABELS, panel_labels):

        accent = COLORS[s_idx]
        wins   = [wdl_data[m]['w'][s_idx] for m in MODEL_LETTERS]
        draws  = [wdl_data[m]['d'][s_idx] for m in MODEL_LETTERS]
        losses = [wdl_data[m]['l'][s_idx] for m in MODEL_LETTERS]

        ys = np.arange(N)
        bh = 0.60

        ax.barh(ys, wins, height=bh,
                color=WIN_C,  edgecolor='white', linewidth=0.6,
                alpha=0.88, zorder=3, label='Wins')
        ax.barh(ys, draws, height=bh, left=wins,
                color=DRAW_C, edgecolor='white', linewidth=0.6,
                alpha=0.88, zorder=3, label='Draws')
        ax.barh(ys, losses, height=bh,
                left=[w + d for w, d in zip(wins, draws)],
                color=LOSS_C, edgecolor='white', linewidth=0.6,
                alpha=0.88, zorder=3, label='Losses')

        for i, (w, d, l) in enumerate(zip(wins, draws, losses)):
            if w > 0:
                ax.text(w / 2, i, str(w), ha='center', va='center',
                        fontsize=9, fontweight='bold', color='white', zorder=4)
            if d > 0:
                ax.text(w + d / 2, i, str(d), ha='center', va='center',
                        fontsize=9, color='#444444', zorder=4)
            if l > 0:
                ax.text(w + d + l / 2, i, str(l), ha='center', va='center',
                        fontsize=9, fontweight='bold', color='white', zorder=4)

        ax.set_yticks(ys)
        ax.set_yticklabels(MODEL_LETTERS, fontsize=11)
        ax.set_xlabel('Games', fontsize=10, labelpad=4)
        ax.set_title(f'{panel_lbl}  {label_str}', fontsize=11, pad=8)

        ax.set_xlim(0, 9.5)
        ax.set_xticks([0, 2, 4, 6, 8])
        ax.xaxis.grid(True, color='#e8e8e8', lw=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.invert_yaxis()

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(accent)
        ax.spines['left'].set_linewidth(2.8)

    legend_handles = [
        mpatches.Patch(color=WIN_C,  alpha=0.88, label='Wins'),
        mpatches.Patch(color=DRAW_C, alpha=0.88, label='Draws'),
        mpatches.Patch(color=LOSS_C, alpha=0.88, label='Losses'),
    ]
    axes[-1].legend(
        handles=legend_handles,
        loc='lower right',
        fontsize=9,
        title='Outcome',
        title_fontsize=9,
        framealpha=0.9,
        edgecolor='#cccccc',
    )

    fig.suptitle(
        'Raman Spectroscopy Classification — Win / Draw / Loss Breakdown',
        fontsize=13, fontweight='bold', y=1.00,
    )

    plt.savefig('elo_wdl.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('elo_wdl.pdf', dpi=300, bbox_inches='tight', facecolor='white')
    print("Saved: elo_wdl.png / elo_wdl.pdf")
    plt.close()


if __name__ == '__main__':
    make_elo_figure()
    make_wdl_figure()