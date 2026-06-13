"""Figure 5 — Correlations among continuous clinical variables (heatmap).

Stage 3: several continuous measurements, want to see co-variation and check for
collinearity before/after modelling -> Spearman correlation heatmap (robust to the
skew in creatinine/CPK), diverging colormap centred at 0, r annotated.
Data: heart_failure_*.csv.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR, CONTINUOUS
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.95)
df = load_clean()

cols = [c for c, *_ in CONTINUOUS] + ["time"]
short = {c: lab.split(" (")[0] for c, lab, _ in CONTINUOUS}
short["time"] = "Follow-up"
labels = [short[c].replace(" ", "\n") for c in cols]
corr = df[cols].corr(method="spearman")

fig, ax = plt.subplots()
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=ps["tick_label_pt"] - 1)
ax.set_yticks(range(len(labels))); ax.set_yticklabels(labels, fontsize=ps["tick_label_pt"] - 1)
for i in range(len(labels)):
    for j in range(len(labels)):
        r = corr.values[i, j]
        ax.text(j, i, f"{r:.2f}", ha="center", va="center",
                color="white" if abs(r) > 0.6 else "black", fontsize=ps["tick_label_pt"] - 1)
cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("Spearman ρ")
ax.set_title("Correlations among clinical variables", fontsize=ps["title_pt"])

save_figure(fig, number="5", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig5 done — correlation heatmap")
