"""Table 3 — Sample composition: number of penguins by species, island and sex.

Stage 3: a composition table documents the dataset (the kind of "Table 1" that
describes the sample). Counts of birds per species x island, split by sex, with
row totals. Three-line Word + CSV. Data: penguins_raw.csv.
"""
import pandas as pd

from _common import load_clean, FIGDIR, SPECIES_ORDER, three_line_table

df = load_clean()

rows = []
for s in SPECIES_ORDER:
    sub = df[df["species"] == s]
    for island in sorted(sub["Island"].unique()):
        isl = sub[sub["Island"] == island]
        nf = int((isl["sex"] == "Female").sum())
        nm = int((isl["sex"] == "Male").sum())
        nu = int(isl["sex"].isna().sum())
        rows.append({
            "Species": s,
            "Island": island,
            "Female": nf,
            "Male": nm,
            "Unknown": nu,
            "Total": len(isl),
        })

table = pd.DataFrame(rows)
# append an overall total row
total = {"Species": "All", "Island": "—",
         "Female": int(table["Female"].sum()), "Male": int(table["Male"].sum()),
         "Unknown": int(table["Unknown"].sum()), "Total": int(table["Total"].sum())}
table = pd.concat([table, pd.DataFrame([total])], ignore_index=True)

FIGDIR.mkdir(parents=True, exist_ok=True)
table.to_csv(FIGDIR / "Table3.csv", index=False)
three_line_table(
    table, FIGDIR / "Table3.docx",
    title="Table 3. Sample composition by species, island and sex (number of penguins).",
    note="Unknown = sex not determined. Data: Gorman et al. (2014).",
)
print(table.to_string(index=False))
print(f"\nwrote {FIGDIR / 'Table3.docx'}")
