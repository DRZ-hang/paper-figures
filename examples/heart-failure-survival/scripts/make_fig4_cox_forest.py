"""Figure 4 — Multivariable Cox proportional-hazards model (forest plot).

Stage 2 claim: "Adjusting for all covariates, which factors independently predict
mortality hazard?"
Stage 3: hazard ratios from a multivariable Cox model -> forest plot on a log scale
with 95% CIs and a reference line at HR = 1. Continuous predictors are standardized
so HRs are per 1 SD and comparable. Data: heart_failure_*.csv. Uses lifelines.
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter

from _common import load_clean, FIGDIR, CONTINUOUS, BINARY
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=1.05)
df = load_clean()

cont = [c for c, *_ in CONTINUOUS]
binv = [c for c, _ in BINARY]
X = df[cont + binv + ["time", "death_event"]].copy()
X[cont] = (X[cont] - X[cont].mean()) / X[cont].std()  # standardize -> HR per 1 SD

cph = CoxPHFitter()
cph.fit(X, duration_col="time", event_col="death_event")
s = cph.summary  # index = covariate
labels = {c: f"{lab} (per SD)" for c, lab, _ in CONTINUOUS}
labels.update({c: lab for c, lab in BINARY})

order = cont + binv
hr = np.exp(s.loc[order, "coef"]).values
lo = np.exp(s.loc[order, "coef lower 95%"]).values
hi = np.exp(s.loc[order, "coef upper 95%"]).values
pvals = s.loc[order, "p"].values
names = [labels[c] for c in order]

fig, ax = plt.subplots()
ys = np.arange(len(order))[::-1]
for y, h, l, u, pv in zip(ys, hr, lo, hi, pvals):
    sig = pv < 0.05
    col = get_preset("generic")["palette_colors"][6] if sig else "grey"
    ax.plot([l, u], [y, y], color=col, lw=1.0)
    ax.plot(h, y, "s", color=col, ms=4.5)
    ax.text(8.5, y, f"{h:.2f} [{l:.2f}, {u:.2f}]" + ("*" if sig else ""),
            va="center", fontsize=ps["tick_label_pt"] - 1)
ax.axvline(1, color="grey", lw=0.6, ls="--")
ax.set_xscale("log")
ax.set_xticks([0.5, 1, 2, 4]); ax.set_xticklabels(["0.5", "1", "2", "4"])
ax.set_xlim(0.4, 16)
ax.set_yticks(ys); ax.set_yticklabels(names)
ax.set_xlabel("Hazard ratio (95% CI), log scale")
ax.set_title(f"Cox model — C-index = {cph.concordance_index_:.2f}", fontsize=ps["title_pt"])

save_figure(fig, number="4", preset="generic", outdir=str(FIGDIR), kind="line")
print(f"Fig4 done — Cox C-index={cph.concordance_index_:.3f}")
