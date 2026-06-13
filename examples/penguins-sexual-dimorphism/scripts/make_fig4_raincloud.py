"""Figure 4 — Flipper length by species (raincloud: half-violin + box + points).

Stage 3: comparing a distribution across groups where shape matters -> a raincloud
shows density (violin), summary (box), and raw data (points) at once — more honest
than a bare bar. Chart family: violin / raincloud. Data: penguins_raw.csv.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

rng = np.random.default_rng(0)
ps = apply_preset("generic", column="single", aspect=0.85)
colors = get_preset("generic")["palette_colors"][1:4]
df = load_clean().dropna(subset=["flipper_length_mm"])

fig, ax = plt.subplots()
for i, (s, c) in enumerate(zip(SPECIES_ORDER, colors)):
    vals = df.loc[df["species"] == s, "flipper_length_mm"].values
    # half violin (right side)
    vp = ax.violinplot(vals, positions=[i], widths=0.9, showextrema=False)
    for body in vp["bodies"]:
        verts = body.get_paths()[0].vertices
        verts[:, 0] = np.clip(verts[:, 0], i, np.inf)  # keep right half only
        body.set_facecolor(c); body.set_alpha(0.4); body.set_edgecolor("none")
    # narrow box just left of centre
    bp = ax.boxplot([vals], positions=[i - 0.12], widths=0.12, showfliers=False,
                    patch_artist=True, medianprops=dict(color="black"))
    bp["boxes"][0].set_facecolor("white"); bp["boxes"][0].set_edgecolor("black")
    # rain: jittered points further left
    ax.scatter(np.full_like(vals, i - 0.30) + rng.uniform(-0.06, 0.06, len(vals)),
               vals, s=3, color=c, alpha=0.8, zorder=3)

ax.set_xticks(range(len(SPECIES_ORDER)))
ax.set_xticklabels(SPECIES_ORDER)
ax.set_xlabel("Species")
ax.set_ylabel("Flipper length (mm)")
save_figure(fig, number="4", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig4 done — raincloud")
