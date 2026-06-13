"""Figure 7 — Correlations among morphometric traits (annotated heatmap).

Stage 3: many variables, want to see co-variation -> correlation heatmap with a
diverging colormap centred at 0 and r annotated in each cell. Chart family:
heatmap. Data: penguins_raw.csv (Pearson r, complete cases).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.92)
df = load_clean()

cols = {"culmen_length_mm": "Culmen\nlength",
        "culmen_depth_mm": "Culmen\ndepth",
        "flipper_length_mm": "Flipper\nlength",
        "body_mass_g": "Body\nmass"}
corr = df[list(cols)].corr(method="pearson")
labels = list(cols.values())

fig, ax = plt.subplots()
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels)
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels)
for i in range(len(labels)):
    for j in range(len(labels)):
        r = corr.values[i, j]
        ax.text(j, i, f"{r:.2f}", ha="center", va="center",
                color="white" if abs(r) > 0.6 else "black",
                fontsize=ps["axes_label_pt"])
cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Pearson r")
ax.set_title("Morphometric correlations", fontsize=ps["title_pt"])
save_figure(fig, number="7", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig7 done — correlation heatmap")
