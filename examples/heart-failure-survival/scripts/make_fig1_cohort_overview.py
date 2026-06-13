"""Figure 1 — Cohort overview and why survival analysis is needed.

Stage 2 claim: "Outcomes accrue over a variable follow-up, so we must analyse
time-to-event, not just death proportions."
Stage 3: (A) age distribution by outcome (overlaid histograms); (B) follow-up time
by outcome (box + points) — survivors are censored at varying times, deaths occur
throughout, which is exactly why a Kaplan-Meier / Cox approach is appropriate.
Data: heart_failure_clinical_records.csv (one row = one patient).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR
from figstyle import apply_preset, save_figure, get_preset

rng = np.random.default_rng(0)
ps = apply_preset("generic", column="double", aspect=0.42)
colors = get_preset("generic")["palette_colors"]
oc_color = {"Survived": colors[2], "Died": colors[6]}  # blue / vermillion
df = load_clean()

fig, (ax1, ax2) = plt.subplots(1, 2)

# A: age distribution by outcome
bins = np.linspace(df.age.min(), df.age.max(), 16)
for oc in ["Survived", "Died"]:
    ax1.hist(df.loc[df.outcome == oc, "age"], bins=bins, alpha=0.55,
             color=oc_color[oc], label=oc, edgecolor="white", linewidth=0.3)
ax1.set_xlabel("Age (years)"); ax1.set_ylabel("Patients")
ax1.legend(frameon=False)

# B: follow-up time by outcome (box + jittered points)
for i, oc in enumerate(["Survived", "Died"]):
    v = df.loc[df.outcome == oc, "time"].values
    bp = ax2.boxplot([v], positions=[i], widths=0.5, showfliers=False,
                     patch_artist=True, medianprops=dict(color="black"))
    bp["boxes"][0].set_facecolor(oc_color[oc]); bp["boxes"][0].set_alpha(0.35)
    bp["boxes"][0].set_edgecolor("black")
    ax2.scatter(np.full_like(v, i) + rng.uniform(-0.16, 0.16, len(v)), v,
                s=4, color=oc_color[oc], alpha=0.7, zorder=3)
ax2.set_xticks([0, 1]); ax2.set_xticklabels(["Survived", "Died"])
ax2.set_xlabel("Outcome"); ax2.set_ylabel("Follow-up time (days)")

for ax, lab in zip((ax1, ax2), "AB"):
    ax.text(-0.16, 1.04, lab, transform=ax.transAxes, fontweight="bold",
            fontsize=ps["title_pt"], va="bottom")

save_figure(fig, number="1", preset="generic", outdir=str(FIGDIR), kind="line")
n, d = len(df), int(df.death_event.sum())
print(f"Fig1 done — n={n}, deaths={d} ({d/n*100:.0f}%)")
