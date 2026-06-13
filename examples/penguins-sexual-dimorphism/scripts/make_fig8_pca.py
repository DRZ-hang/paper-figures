"""Figure 8 — Morphometric space via PCA (samples cluster by species).

Stage 3: several correlated measurements per sample, want to see structure ->
PCA scatter coloured by species, with % variance explained on the axes and trait
loadings drawn as a biplot. Chart family: dimensionality reduction. Data:
penguins_raw.csv (4 traits, z-scored, complete cases).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.85)
colors = get_preset("generic")["palette_colors"][1:4]

traits = ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"]
trait_lab = ["Culmen len.", "Culmen dep.", "Flipper len.", "Body mass"]
df = load_clean().dropna(subset=traits)

X = StandardScaler().fit_transform(df[traits].values)
pca = PCA(n_components=2).fit(X)
scores = pca.transform(X)
ev = pca.explained_variance_ratio_ * 100

fig, ax = plt.subplots()
for s, c in zip(SPECIES_ORDER, colors):
    m = (df["species"] == s).values
    ax.scatter(scores[m, 0], scores[m, 1], s=7, color=c, alpha=0.75,
               edgecolor="none", label=s)

# biplot loadings (scaled for visibility)
load = pca.components_.T * np.sqrt(pca.explained_variance_) * 1.8
for (lx, ly), name in zip(load, trait_lab):
    ax.arrow(0, 0, lx, ly, color="black", lw=0.6, head_width=0.08, length_includes_head=True)
    ax.text(lx * 1.12, ly * 1.12, name, fontsize=ps["tick_label_pt"] - 1,
            ha="center", va="center")

ax.axhline(0, color="grey", lw=0.4); ax.axvline(0, color="grey", lw=0.4)
ax.set_xlabel(f"PC1 ({ev[0]:.0f}% variance)")
ax.set_ylabel(f"PC2 ({ev[1]:.0f}% variance)")
ax.legend(frameon=False, title="Species", loc="upper right")
save_figure(fig, number="8", preset="generic", outdir=str(FIGDIR), kind="line")
print(f"Fig8 done — PCA biplot (PC1 {ev[0]:.0f}%, PC2 {ev[1]:.0f}%)")
