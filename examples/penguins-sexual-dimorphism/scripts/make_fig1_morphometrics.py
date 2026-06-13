"""Figure 1 — Body size differs among the three Pygoscelis species.

Stage 2 claim: "Flipper length and body mass separate the three penguin species."
Stage 3: one quantitative outcome by a 3-level group -> box + jittered points
         (show every bird; n is modest). Omnibus test = Kruskal-Wallis (robust,
         no normality assumption) reported per panel.
Data: Gorman et al. 2014, penguins_raw.csv (one row = one penguin).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

rng = np.random.default_rng(0)
spec = apply_preset("generic", column="double", aspect=0.45)
colors = get_preset("generic")["palette_colors"]

df = load_clean()
panels = [
    ("flipper_length_mm", "Flipper length (mm)"),
    ("body_mass_g", "Body mass (g)"),
]

fig, axes = plt.subplots(1, 2)
for ax, (col, ylab) in zip(axes, panels):
    groups = [df.loc[df["species"] == s, col].dropna().values for s in SPECIES_ORDER]
    bp = ax.boxplot(groups, showfliers=False, widths=0.55, patch_artist=True,
                    medianprops=dict(color="black"))
    for patch, c in zip(bp["boxes"], colors[1:4]):
        patch.set_facecolor(c); patch.set_alpha(0.35); patch.set_edgecolor("black")
    for i, (g, c) in enumerate(zip(groups, colors[1:4]), 1):
        ax.scatter(np.full_like(g, i) + rng.uniform(-0.13, 0.13, len(g)), g,
                   s=3, color=c, edgecolor="none", alpha=0.8, zorder=3)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(SPECIES_ORDER)
    ax.set_ylabel(ylab); ax.set_xlabel("Species")
    H, p = stats.kruskal(*groups)
    ax.set_title(f"Kruskal–Wallis H={H:.1f}, p={'<0.001' if p < 1e-3 else f'{p:.3f}'}",
                 fontsize=get_preset("generic")["tick_label_pt"])

# panel labels A, B
for ax, lab in zip(axes, "AB"):
    ax.text(-0.18, 1.04, lab, transform=ax.transAxes, fontweight="bold",
            fontsize=get_preset("generic")["title_pt"], va="bottom")

save_figure(fig, number="1", preset="generic", outdir=str(FIGDIR), kind="line")
print("n per species:", {s: int((df['species'] == s).sum()) for s in SPECIES_ORDER})
