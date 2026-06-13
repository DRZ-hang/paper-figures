"""Table 1 — Baseline characteristics by survival status (three-line table).

The classic clinical "Table 1": each variable compared between survivors and those
who died. Continuous variables -> median [IQR] with Mann-Whitney U; binary
variables -> n (%) with chi-square. p-values flag univariable differences (not
adjusted for follow-up time — see Cox model, Table 2). Data: heart_failure_*.csv.
"""
import numpy as np
import pandas as pd
from scipy import stats

from _common import load_clean, FIGDIR, CONTINUOUS, BINARY, three_line_table

df = load_clean()
surv = df[df.death_event == 0]
died = df[df.death_event == 1]


def med_iqr(s, dec):
    return f"{s.median():.{dec}f} [{s.quantile(.25):.{dec}f}–{s.quantile(.75):.{dec}f}]"


def npct(s):
    n = int(s.sum())
    return f"{n} ({n / len(s) * 100:.0f}%)"


def pfmt(p):
    return "< 0.001" if p < 1e-3 else f"{p:.3f}"


rows = [{"Characteristic": "Patients, n",
         "Survived (n=203)": str(len(surv)), "Died (n=96)": str(len(died)), "p": ""}]

for col, label, dec in CONTINUOUS:
    _, p = stats.mannwhitneyu(surv[col], died[col])
    rows.append({
        "Characteristic": f"{label}, median [IQR]",
        "Survived (n=203)": med_iqr(surv[col], dec),
        "Died (n=96)": med_iqr(died[col], dec),
        "p": pfmt(p),
    })
for col, label in BINARY:
    ct = pd.crosstab(df[col], df.death_event)
    chi2, p, _, _ = stats.chi2_contingency(ct)
    rows.append({
        "Characteristic": f"{label}, n (%)",
        "Survived (n=203)": npct(surv[col]),
        "Died (n=96)": npct(died[col]),
        "p": pfmt(p),
    })

table = pd.DataFrame(rows)
FIGDIR.mkdir(parents=True, exist_ok=True)
table.to_csv(FIGDIR / "Table1.csv", index=False)
three_line_table(
    table, FIGDIR / "Table1.docx",
    title="Table 1. Baseline characteristics by survival status.",
    note="Continuous variables: median [IQR], Mann–Whitney U test; binary variables: "
         "n (%), chi-square test. Counts compare survivors vs. patients who died during "
         "follow-up. Data: Chicco & Jurman (2020).",
)
print(table.to_string(index=False))
print(f"\nwrote {FIGDIR / 'Table1.docx'}")
