"""Figure 5 — Body-mass distribution by species (histogram + ECDF).

Stage 3: when the *shape* of one variable's distribution is the point, show it
directly. (A) overlaid histograms; (B) empirical CDF — no binning choice, ideal
for comparing groups. Chart family: distribution. Data: penguins_raw.csv.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="double", aspect=0.42)
colors = get_preset("generic")["palette_colors"][1:4]
df = load_clean().dropna(subset=["body_mass_g"])

fig, (ax1, ax2) = plt.subplots(1, 2)
bins = np.linspace(df["body_mass_g"].min(), df["body_mass_g"].max(), 22)
for s, c in zip(SPECIES_ORDER, colors):
    v = df.loc[df["species"] == s, "body_mass_g"].values
    ax1.hist(v, bins=bins, color=c, alpha=0.55, label=s, edgecolor="white", linewidth=0.3)
    xs = np.sort(v)
    ax2.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", color=c, lw=1.2, label=s)

ax1.set_xlabel("Body mass (g)"); ax1.set_ylabel("Count")
ax1.legend(frameon=False, title="Species")
ax2.set_xlabel("Body mass (g)"); ax2.set_ylabel("Cumulative proportion")
ax2.legend(frameon=False, title="Species", loc="lower right")
for ax, lab in zip((ax1, ax2), "AB"):
    ax.text(-0.16, 1.04, lab, transform=ax.transAxes, fontweight="bold",
            fontsize=ps["title_pt"], va="bottom")

save_figure(fig, number="5", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig5 done — histogram + ECDF")
