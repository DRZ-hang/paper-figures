"""Figure 2 — Survival by ejection-fraction category (Kaplan-Meier).

Stage 2 claim: "Lower ejection fraction predicts worse survival."
Stage 3: time-to-event outcome stratified by a clinically meaningful grouping ->
Kaplan-Meier curves with a numbers-at-risk table and an overall log-rank test.
EF groups: reduced (<30%), mid-range (30-45%), preserved (>=45%).
Data: heart_failure_clinical_records.csv. Uses lifelines.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import multivariate_logrank_test
from lifelines.plotting import add_at_risk_counts

from _common import load_clean, FIGDIR
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.95)
colors = get_preset("generic")["palette_colors"]
df = load_clean()

bins = [0, 30, 45, 100]
labels = ["Reduced (<30%)", "Mid (30–45%)", "Preserved (≥45%)"]
df["ef_group"] = __import__("pandas").cut(df["ejection_fraction"], bins=bins, labels=labels, right=False)
grp_color = {labels[0]: colors[6], labels[1]: colors[1], labels[2]: colors[3]}

# taller figure to fit the at-risk table beneath
import matplotlib as mpl
w, h = mpl.rcParams["figure.figsize"]
fig, ax = plt.subplots(figsize=(w, h * 1.25))
kms = []
for lab in labels:
    m = df["ef_group"] == lab
    km = KaplanMeierFitter(label=lab)
    km.fit(df.loc[m, "time"], df.loc[m, "death_event"])
    km.plot_survival_function(ax=ax, ci_show=True, color=grp_color[lab], linewidth=1.2)
    kms.append(km)

lr = multivariate_logrank_test(df["time"], df["ef_group"], df["death_event"])
ax.set_xlabel("Time (days)")
ax.set_ylabel("Survival probability")
ax.set_ylim(0, 1.02)
ax.legend(frameon=False, fontsize=ps["tick_label_pt"], loc="lower left")
p = lr.p_value
ax.set_title(f"Log-rank p {'< 0.001' if p < 1e-3 else f'= {p:.3f}'}", fontsize=ps["title_pt"])
add_at_risk_counts(*kms, ax=ax, fontsize=ps["tick_label_pt"] - 1)

save_figure(fig, number="2", preset="generic", outdir=str(FIGDIR), kind="line")
print(f"Fig2 done — log-rank p={lr.p_value:.2e}")
