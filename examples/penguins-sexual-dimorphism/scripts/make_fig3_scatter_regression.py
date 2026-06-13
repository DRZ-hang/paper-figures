"""Figure 3 — Culmen shape relationship, by species (scatter + linear fit).

Stage 3: two quantitative variables -> scatter; we claim a within-species linear
relationship -> per-species OLS fit with 95% CI band. Pooling all species would
reverse the slope (a Simpson's paradox), so we fit within species and say so.
Chart family: scatter + regression. Data: penguins_raw.csv.
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
df = load_clean().dropna(subset=["culmen_length_mm", "culmen_depth_mm"])

fig, ax = plt.subplots()
for s, c in zip(SPECIES_ORDER, colors):
    sub = df[df["species"] == s]
    x, y = sub["culmen_length_mm"].values, sub["culmen_depth_mm"].values
    ax.scatter(x, y, s=6, color=c, alpha=0.75, edgecolor="none", label=s)
    # OLS fit + CI band
    res = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 100)
    ys = res.intercept + res.slope * xs
    # 95% CI for the mean prediction
    n = len(x); dof = n - 2
    tval = stats.t.ppf(0.975, dof)
    se_line = np.sqrt(np.sum((y - (res.intercept + res.slope * x)) ** 2) / dof) * \
        np.sqrt(1 / n + (xs - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2))
    ax.plot(xs, ys, color=c, lw=1.0)
    ax.fill_between(xs, ys - tval * se_line, ys + tval * se_line, color=c, alpha=0.15)

ax.set_xlabel("Culmen length (mm)")
ax.set_ylabel("Culmen depth (mm)")
ax.legend(title="Species", frameon=False, loc="lower right")
save_figure(fig, number="3", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig3 done — per-species scatter + OLS fit")
