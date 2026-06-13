"""Figure 3 — The two headline predictors differ by outcome.

Stage 2 claim: "Patients who died had lower ejection fraction and higher serum
creatinine" (the paper's two key features).
Stage 3: continuous variable by a 2-level outcome -> box + points; Mann-Whitney U
(non-parametric — serum creatinine is right-skewed). Data: heart_failure_*.csv.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from _common import load_clean, FIGDIR
from figstyle import apply_preset, save_figure, get_preset

rng = np.random.default_rng(0)
ps = apply_preset("generic", column="double", aspect=0.45)
colors = get_preset("generic")["palette_colors"]
oc_color = {"Survived": colors[2], "Died": colors[6]}
df = load_clean()

panels = [("ejection_fraction", "Ejection fraction (%)"),
          ("serum_creatinine", "Serum creatinine (mg/dL)")]

fig, axes = plt.subplots(1, 2)
for ax, (col, ylab) in zip(axes, panels):
    data = {}
    for i, oc in enumerate(["Survived", "Died"]):
        v = df.loc[df.outcome == oc, col].values
        data[oc] = v
        bp = ax.boxplot([v], positions=[i], widths=0.5, showfliers=False,
                        patch_artist=True, medianprops=dict(color="black"))
        bp["boxes"][0].set_facecolor(oc_color[oc]); bp["boxes"][0].set_alpha(0.35)
        bp["boxes"][0].set_edgecolor("black")
        ax.scatter(np.full_like(v, i) + rng.uniform(-0.16, 0.16, len(v)), v,
                   s=4, color=oc_color[oc], alpha=0.7, zorder=3)
    U, p = stats.mannwhitneyu(data["Survived"], data["Died"])
    y = max(np.concatenate(list(data.values())))
    ax.plot([0, 0, 1, 1], [y * 1.02, y * 1.04, y * 1.04, y * 1.02], lw=0.7, color="black")
    stars = "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 0.05 else "ns"
    ax.text(0.5, y * 1.045, stars, ha="center", va="bottom", fontsize=ps["axes_label_pt"])
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Survived", "Died"])
    ax.set_ylabel(ylab); ax.set_xlabel("Outcome")

for ax, lab in zip(axes, "AB"):
    ax.text(-0.18, 1.04, lab, transform=ax.transAxes, fontweight="bold",
            fontsize=ps["title_pt"], va="bottom")

save_figure(fig, number="3", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig3 done — predictors by outcome (Mann-Whitney)")
