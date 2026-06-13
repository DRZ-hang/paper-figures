"""Table 2 — Multivariable Cox proportional-hazards model (three-line table).

Reports the adjusted hazard ratio (HR), 95% CI and p for every covariate, plus the
model's concordance index. Continuous predictors are standardized so HR is per 1 SD.
This is the inferential complement to the Fig 4 forest plot. Data: heart_failure_*.csv.
"""
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter

from _common import load_clean, FIGDIR, CONTINUOUS, BINARY, three_line_table

df = load_clean()
cont = [c for c, *_ in CONTINUOUS]
binv = [c for c, _ in BINARY]
X = df[cont + binv + ["time", "death_event"]].copy()
X[cont] = (X[cont] - X[cont].mean()) / X[cont].std()

cph = CoxPHFitter()
cph.fit(X, duration_col="time", event_col="death_event")
s = cph.summary

labels = {c: f"{lab.split(' (')[0]} (per SD)" for c, lab, _ in CONTINUOUS}
labels.update({c: lab for c, lab in BINARY})


def pfmt(p):
    return "< 0.001" if p < 1e-3 else f"{p:.3f}"


rows = []
for c in cont + binv:
    hr = np.exp(s.loc[c, "coef"])
    lo = np.exp(s.loc[c, "coef lower 95%"])
    hi = np.exp(s.loc[c, "coef upper 95%"])
    rows.append({
        "Predictor": labels[c],
        "HR [95% CI]": f"{hr:.2f} [{lo:.2f}, {hi:.2f}]",
        "p": pfmt(s.loc[c, "p"]),
    })

table = pd.DataFrame(rows)
FIGDIR.mkdir(parents=True, exist_ok=True)
table.to_csv(FIGDIR / "Table2.csv", index=False)
three_line_table(
    table, FIGDIR / "Table2.docx",
    title="Table 2. Multivariable Cox proportional-hazards model for mortality.",
    note=f"HR = hazard ratio; continuous predictors standardized (HR per 1 SD). "
         f"Model concordance index = {cph.concordance_index_:.2f}; n = {len(df)}, "
         f"events = {int(df.death_event.sum())}. Data: Chicco & Jurman (2020).",
)
print(table.to_string(index=False))
print(f"\nC-index = {cph.concordance_index_:.3f}")
print(f"wrote {FIGDIR / 'Table2.docx'}")
