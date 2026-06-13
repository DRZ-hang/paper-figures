"""Figure 2 — Sexual size dimorphism: males are heavier within every species.

Stage 2 claim: "Within each species, males are heavier than females."
Stage 3: continuous outcome (body mass), 2 independent groups (sex) within each
         species -> grouped box + points; per-species Welch's t-test (unequal
         variance, no equal-variance assumption); Hedges' g effect size with CI.
         This mirrors the paper's sexual-dimorphism theme (Gorman et al. 2014).
Data: penguins_raw.csv (one row = one penguin; birds with unknown sex dropped).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

rng = np.random.default_rng(0)
ps = apply_preset("generic", column="single", aspect=0.85)
colors = get_preset("generic")["palette_colors"]
sex_color = {"Female": colors[2], "Male": colors[6]}  # blue / vermillion (CB-safe)

df = load_clean().dropna(subset=["sex", "body_mass_g"])


def hedges_g(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    d = (b.mean() - a.mean()) / sp
    return d * (1 - 3 / (4 * (na + nb) - 9))  # small-sample correction


fig, ax = plt.subplots()
positions, results = [], []
for i, s in enumerate(SPECIES_ORDER):
    sub = df[df["species"] == s]
    for j, sex in enumerate(["Female", "Male"]):
        vals = sub.loc[sub["sex"] == sex, "body_mass_g"].values
        pos = i * 2.6 + j
        positions.append(pos)
        bp = ax.boxplot([vals], positions=[pos], widths=0.7, showfliers=False,
                        patch_artist=True, medianprops=dict(color="black"))
        bp["boxes"][0].set_facecolor(sex_color[sex]); bp["boxes"][0].set_alpha(0.35)
        bp["boxes"][0].set_edgecolor("black")
        ax.scatter(np.full_like(vals, pos) + rng.uniform(-0.18, 0.18, len(vals)),
                   vals, s=3, color=sex_color[sex], alpha=0.85, zorder=3)
    f = sub.loc[sub["sex"] == "Female", "body_mass_g"].values
    m = sub.loc[sub["sex"] == "Male", "body_mass_g"].values
    t, p = stats.ttest_ind(m, f, equal_var=False)  # Welch
    g = hedges_g(f, m)
    results.append((s, len(f), len(m), t, p, g))
    # significance bracket
    x1, x2 = i * 2.6, i * 2.6 + 1
    y = max(m.max(), f.max()) * 1.04
    ax.plot([x1, x1, x2, x2], [y, y * 1.01, y * 1.01, y], lw=0.7, color="black")
    stars = "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 0.05 else "ns"
    ax.text((x1 + x2) / 2, y * 1.015, stars, ha="center", va="bottom",
            fontsize=ps["axes_label_pt"])

ax.set_xticks([i * 2.6 + 0.5 for i in range(3)])
ax.set_xticklabels(SPECIES_ORDER)
ax.set_ylabel("Body mass (g)"); ax.set_xlabel("Species")
# legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(facecolor=sex_color["Female"], alpha=0.35, edgecolor="black", label="Female"),
                   Patch(facecolor=sex_color["Male"], alpha=0.35, edgecolor="black", label="Male")],
          loc="upper left", frameon=False)

save_figure(fig, number="2", preset="generic", outdir=str(FIGDIR), kind="line")
print("species  nF  nM   Welch t      p        Hedges g")
for s, nf, nm, t, p, g in results:
    print(f"{s:<9} {nf:>3} {nm:>3}  {t:>7.2f}  {p:.2e}   {g:+.2f}")
