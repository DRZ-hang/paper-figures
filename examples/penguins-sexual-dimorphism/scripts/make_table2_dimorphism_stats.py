"""Table 2 — Sexual dimorphism test results per species and trait.

Stage 3: a results table is the right format when readers need the exact test
statistics. For each species x trait: female and male mean ± SD, Welch's t,
degrees of freedom, p, and Hedges' g with 95% CI. Three-line Word + CSV.
Data: penguins_raw.csv.
"""
import numpy as np
import pandas as pd
from scipy import stats

from _common import load_clean, FIGDIR, SPECIES_ORDER, three_line_table

TRAITS = [
    ("culmen_length_mm", "Culmen length (mm)", 1),
    ("culmen_depth_mm", "Culmen depth (mm)", 1),
    ("flipper_length_mm", "Flipper length (mm)", 0),
    ("body_mass_g", "Body mass (g)", 0),
]
df = load_clean().dropna(subset=["sex"])


def hedges_g_ci(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na - 1) * a.std(ddof=1) ** 2 + (nb - 1) * b.std(ddof=1) ** 2) / (na + nb - 2))
    J = 1 - 3 / (4 * (na + nb) - 9)
    g = (b.mean() - a.mean()) / sp * J
    se = np.sqrt((na + nb) / (na * nb) + g ** 2 / (2 * (na + nb)))
    return g, g - 1.96 * se, g + 1.96 * se


def pfmt(p):
    return "< 0.001" if p < 1e-3 else f"{p:.3f}"


rows = []
for s in SPECIES_ORDER:
    sub = df[df["species"] == s]
    for col, label, dec in TRAITS:
        f = sub.loc[sub["sex"] == "Female", col].dropna().values
        m = sub.loc[sub["sex"] == "Male", col].dropna().values
        t, p = stats.ttest_ind(m, f, equal_var=False)
        dofw = (f.var(ddof=1) / len(f) + m.var(ddof=1) / len(m)) ** 2 / (
            (f.var(ddof=1) / len(f)) ** 2 / (len(f) - 1)
            + (m.var(ddof=1) / len(m)) ** 2 / (len(m) - 1))
        g, lo, hi = hedges_g_ci(f, m)
        rows.append({
            "Species": s,
            "Trait": label,
            "Female (mean ± SD)": f"{f.mean():.{dec}f} ± {f.std(ddof=1):.{dec}f}",
            "Male (mean ± SD)": f"{m.mean():.{dec}f} ± {m.std(ddof=1):.{dec}f}",
            "t": f"{t:.2f}",
            "df": f"{dofw:.1f}",
            "p": pfmt(p),
            "Hedges' g [95% CI]": f"{g:.2f} [{lo:.2f}, {hi:.2f}]",
        })

table = pd.DataFrame(rows)
FIGDIR.mkdir(parents=True, exist_ok=True)
table.to_csv(FIGDIR / "Table2.csv", index=False)
three_line_table(
    table, FIGDIR / "Table2.docx",
    title="Table 2. Sexual dimorphism by species and trait (Welch's t-test).",
    note="Male vs female; t = Welch's t, df = Welch–Satterthwaite; g = Hedges' g "
         "(positive = males larger). Data: Gorman et al. (2014).",
)
print(table.to_string(index=False))
print(f"\nwrote {FIGDIR / 'Table2.docx'}")
