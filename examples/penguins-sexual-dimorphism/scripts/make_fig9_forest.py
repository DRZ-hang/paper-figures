"""Figure 9 — Effect size of sexual dimorphism per species (forest plot).

Stage 3: comparing an effect size across groups with uncertainty -> forest plot:
point estimate + 95% CI per species, a null reference line at g = 0. Effect =
standardized male-female body-mass difference (Hedges' g). Chart family: forest /
effect sizes. Data: penguins_raw.csv.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _common import load_clean, FIGDIR, SPECIES_ORDER
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.6)
df = load_clean().dropna(subset=["sex", "body_mass_g"])


def hedges_g_ci(a, b):
    """g for (b - a) with 95% CI (a=female, b=male)."""
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    d = (b.mean() - a.mean()) / sp
    J = 1 - 3 / (4 * (na + nb) - 9)
    g = d * J
    se = np.sqrt((na + nb) / (na * nb) + g ** 2 / (2 * (na + nb)))
    return g, g - 1.96 * se, g + 1.96 * se


rows = []
for s in SPECIES_ORDER:
    sub = df[df["species"] == s]
    f = sub.loc[sub["sex"] == "Female", "body_mass_g"].values
    m = sub.loc[sub["sex"] == "Male", "body_mass_g"].values
    g, lo, hi = hedges_g_ci(f, m)
    rows.append((s, len(f) + len(m), g, lo, hi))

fig, ax = plt.subplots()
ys = np.arange(len(rows))[::-1]
for y, (s, n, g, lo, hi) in zip(ys, rows):
    ax.plot([lo, hi], [y, y], color="black", lw=0.9)
    ax.plot(g, y, "s", color=get_preset("generic")["palette_colors"][5], ms=5)
    ax.text(hi + 0.08, y, f"g = {g:.2f} [{lo:.2f}, {hi:.2f}]",
            va="center", fontsize=ps["tick_label_pt"])
ax.axvline(0, color="grey", lw=0.6, ls="--")
ax.set_yticks(ys); ax.set_yticklabels([f"{s} (n={n})" for s, n, *_ in rows])
ax.set_xlabel("Hedges' g  (male − female body mass)")
ax.set_xlim(-0.3, max(r[4] for r in rows) + 1.4)
ax.set_title("Sexual dimorphism effect size by species", fontsize=ps["title_pt"])
save_figure(fig, number="9", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig9 done — forest plot")
