"""Figure 6 — Species composition across islands (grouped bar of counts).

Stage 3: counts across two categorical variables -> grouped bar (bars start at
zero, n shown on bars). A chi-square test summarizes the association. Chart family:
bar / counts. Data: penguins_raw.csv.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.8)
colors = get_preset("generic")["palette_colors"][1:4]
df = load_clean()

ct = df.pivot_table(index="Island", columns="species", aggfunc="size", fill_value=0,
                    observed=False)
ct = ct[SPECIES_ORDER]
islands = list(ct.index)
x = np.arange(len(islands)); w = 0.26

fig, ax = plt.subplots()
for k, (s, c) in enumerate(zip(SPECIES_ORDER, colors)):
    vals = ct[s].values
    bars = ax.bar(x + (k - 1) * w, vals, width=w, color=c, label=s, edgecolor="white", linewidth=0.4)
    for b, v in zip(bars, vals):
        if v:
            ax.text(b.get_x() + b.get_width() / 2, v + 1, str(int(v)),
                    ha="center", va="bottom", fontsize=ps["tick_label_pt"] - 1)

chi2, p, dof, _ = stats.chi2_contingency(ct.values)
ax.set_xticks(x); ax.set_xticklabels(islands)
ax.set_xlabel("Island"); ax.set_ylabel("Number of penguins")
ax.legend(frameon=False, title="Species")
ax.set_title(f"χ² = {chi2:.0f}, p {'< 0.001' if p < 1e-3 else f'= {p:.3f}'}",
             fontsize=ps["tick_label_pt"])
save_figure(fig, number="6", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig6 done — grouped bar counts")
