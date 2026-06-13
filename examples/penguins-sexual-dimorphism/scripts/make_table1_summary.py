"""Table 1 — Morphometric summary by species and sex (mean +/- SD, n).

Stage 3: a summary table is the right format here because readers look up exact
values per group. One statistic style per cell: mean +/- SD; n stated per group.
Exports Table1.docx (academic three-line table), Table1.csv, and Table1.md.
Data: penguins_raw.csv (Gorman et al. 2014).
"""
import pandas as pd

from _common import load_clean, FIGDIR, SPECIES_ORDER, three_line_table

METRICS = [
    ("culmen_length_mm", "Culmen length (mm)", 1),
    ("culmen_depth_mm", "Culmen depth (mm)", 1),
    ("flipper_length_mm", "Flipper length (mm)", 0),
    ("body_mass_g", "Body mass (g)", 0),
]

df = load_clean().dropna(subset=["sex"])

rows = []
for s in SPECIES_ORDER:
    for sex in ["Female", "Male"]:
        sub = df[(df["species"] == s) & (df["sex"] == sex)]
        row = {"Species": s, "Sex": sex, "n": len(sub)}
        for col, label, dec in METRICS:
            v = sub[col].dropna()
            row[label] = f"{v.mean():.{dec}f} ± {v.std(ddof=1):.{dec}f}"
        rows.append(row)

table = pd.DataFrame(rows)
FIGDIR.mkdir(parents=True, exist_ok=True)
csv_path = FIGDIR / "Table1.csv"
md_path = FIGDIR / "Table1.md"
docx_path = FIGDIR / "Table1.docx"
table.to_csv(csv_path, index=False)

three_line_table(
    table,
    docx_path,
    title="Table 1. Morphometric measurements (mean ± SD) by species and sex.",
    note="n = number of penguins. Data: Gorman et al. (2014).",
)

with open(md_path, "w", encoding="utf-8") as fh:
    fh.write("**Table 1.** Morphometric measurements (mean ± SD) by species and sex. "
             "n = number of penguins. Data: Gorman et al. (2014).\n\n")
    fh.write(table.to_markdown(index=False))
    fh.write("\n")

print(table.to_string(index=False))
print(f"\nwrote {docx_path}\nwrote {csv_path}\nwrote {md_path}")
