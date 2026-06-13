---
name: paper-figures
description: >-
  Produce publication-quality statistical figures and tables for scientific
  papers, end-to-end from the paper's own raw data using Python. Use this skill
  whenever the user wants to make, redo, or improve charts, plots, graphs, or
  tables for a manuscript, thesis, or grant — including requests like "draw a
  figure for this dataset", "make a bar/box/violin/forest/Kaplan-Meier plot",
  "I need a results table", "format my figures for Nature/Science/Cell/IEEE",
  "what chart should I use for this data", or "turn my CSV/Excel results into a
  figure for my paper". Trigger even when the user only shares a manuscript and
  data and asks where figures are needed. The skill reads the paper, finds where
  visuals are needed, picks the right statistics and chart type for the data,
  applies journal formatting, renders with Python, self-checks the rendered
  image, exports numbered assets, and writes a bilingual (中文/English) figure
  report with captions, annotations, and in-text citation locations.
---

# Paper Figures — Scientific Figure & Table Studio

You turn a paper's **own raw data** into publication-ready figures and tables. Every
result must be reproducible from a Python script you write and run — never hand-drawn,
never faked, never eyeballed. If a number can't be traced to the raw data, it doesn't
go on the figure.

This skill is a **workflow**, not a single command. Walk through the seven stages below
in order. Each figure or table is one pass through stages 2–6; do stage 1 once for the
whole paper and stage 7 once at the end.

## Communication & language

Talk to the user in the language they write to you in (the user base is bilingual 中文/English).

The **output language of the deliverable** (captions, annotations, the figure report) is the
**user's choice** — different journals and readers need different things. Offer three modes and
ask which they want if it isn't already clear from the request:
- **English only** — for an English-language manuscript or international journal.
- **Chinese only / 全中文** — for a Chinese thesis or journal.
- **Bilingual (中文 + English)** — captions in both, useful while drafting or for a bilingual team.

If the user doesn't specify and you can't infer it (e.g. they wrote to you in Chinese about a
Chinese-language journal → Chinese; in English about *Nature* → English), default to **bilingual**
and say so. `scripts/report_docx.py` takes a `lang` argument (`"en"`, `"zh"`, `"bilingual"`) that
sets both which captions appear and the section-label language; write caption/annotation text in
the chosen language(s) accordingly.

## Guiding principles (read once, keep in mind throughout)

- **Data first, plot second.** The argument the figure makes must already be true in the
  data. The plot reveals it; it never manufactures it.
- **Honesty over beauty.** No truncated axes that exaggerate effects, no cherry-picked
  bins, no hidden n, no "representative" without saying how it was chosen. If you make a
  scale choice that affects interpretation (log axis, broken axis, zoom), say so in the
  caption.
- **Reproducible.** Save every script. Re-running it on the same data must reproduce the
  exact figure. Set random seeds. Record library versions.
- **Right tool for the data.** Let the data's *shape* and the *claim* pick the chart, not
  habit. A bar chart of means hides the distribution; show the data when you can.

---

## Stage 1 — Read the paper, find where visuals are needed

Read the manuscript (or abstract + results + methods if it's long) before touching data.
Build a quick mental model of the study: what's the question, what was measured, what are
the comparisons.

Then produce a **figure/table plan**: a list of every place a figure or table would
strengthen the paper. For each entry note:
- a working title and number (Fig 1, Fig 2, Table 1, …),
- the claim/result it supports,
- the section + sentence where it will be cited (the "in-text citation location"),
- whether it's a figure or a table, and roughly what kind.

Common cues that a visual is needed: a comparison between groups/conditions, a
time-course or dose-response, a correlation or association, a distribution, a model fit,
a survival/event analysis, a multi-variable summary, sample characteristics (usually a
table), or a list of model coefficients / test results (table).

Show the plan to the user and confirm scope before proceeding — don't silently decide to
make 12 figures. If the user already told you exactly which figures they want, skip the
proposal and just confirm numbering and citation locations.

## Stage 2 — Frame the figure: what is it arguing, where is the data?

For the figure you're working on, write one sentence: *"This figure shows that ___."*
That sentence is the figure's job. Everything else serves it.

Then **locate the raw data**:
- Ask for / find the data file(s) (CSV, Excel, TSV, JSON, a database, `.mat`, etc.).
- Identify exactly which columns/fields/sheets feed this figure.
- Confirm units, the meaning of each variable, the grouping variable, and what counts as
  one observation (one cell? one animal? one patient? one replicate?). Getting n and the
  unit of analysis right is the most common source of wrong figures.
- If data is missing or ambiguous, ask. Do not invent or impute silently.

Load and inspect the data first (shape, dtypes, ranges, missingness, group sizes) before
deciding anything. Print a short summary so both you and the user can see what's there.

## Stage 3 — Analyze the data, choose statistics, decide the chart

Pick the statistical treatment and the chart type **from the data's shape and the claim**,
in that order. Read `references/chart-selection.md` for the full decision guide and
`references/statistical-methods.md` for choosing/justifying tests and what to report.

Quick map (details in the references):
- **One quantitative variable, by group** → box / violin / strip / raincloud (show the
  points; avoid bare bar-of-means unless n is large and the distribution is well-behaved).
- **Two quantitative variables** → scatter (+ fit / CI), maybe with marginal
  distributions.
- **Over time / ordered x** → line with error band; spaghetti + mean for repeated
  measures.
- **Counts / proportions** → grouped/stacked bar, or mosaic; consider showing n.
- **Many variables / samples** → heatmap, clustered heatmap, PCA/UMAP scatter.
- **Effect sizes across studies/subgroups** → forest plot.
- **Time-to-event** → Kaplan–Meier with risk table.
- **Distribution shape** → histogram / ECDF / density.

Before plotting, decide and tell the user: the chart type, the statistical test (if any)
and why it fits the design (paired vs unpaired, parametric assumptions, multiple-comparison
correction), what error representation you'll use (SD vs SEM vs CI — and say which in the
caption), and how significance will be shown. Run the actual statistics in code; never
assert a p-value you didn't compute.

For **tables**: decide the columns, the rounding/precision, what summary stats per cell
(mean ± SD, median [IQR], n (%)), and any test column. Tables follow the same data-first
rule.

## Stage 4 — Check standards, configure the environment

Figures must meet the **target journal's** requirements. Journal formatting is a
**configurable preset**, not hard-coded — let the user pick.

1. Ask the user for the target journal (or the venue type: e.g. a Nature-family journal,
   a Cell-press journal, IEEE, Elsevier, PLOS, a thesis, a generic high-quality default).
2. Read `references/journal-specs.md` to understand what to look up (column widths in mm,
   max dimensions, min font size, required file format & resolution, RGB/CMYK, line
   weights, panel-label style). If the exact journal isn't in `assets/presets.json` and
   you're unsure of its current rules, fetch the journal's "guide for authors" / "artwork
   guidelines" and confirm the numbers with the user rather than guessing.
3. Apply the preset via the bundled helper so every figure in the paper is consistent:
   `scripts/figstyle.py` reads `assets/presets.json` and configures matplotlib (size,
   dpi, fonts, line widths, export format). Add or edit a preset in `assets/presets.json`
   to capture a journal not already covered — that's the intended extension point.

Environment: ensure Python deps are available (see `requirements.txt` at repo root —
matplotlib, numpy, pandas, seaborn, scipy, statsmodels; plus lifelines, plotnine, plotly
as needed). Install only what a given figure needs. For fonts, prefer the journal's
required family (often Arial/Helvetica); if unavailable, pick the closest sans-serif and
note the substitution.

## Stage 5 — Plot: write and run the code

Write a clean, self-contained Python script per figure (or a small project with shared
style). The script should: load the raw data, do the analysis/stats, build the plot
applying the journal preset, and save the output. Read `references/plotting-stacks.md`
for publication-quality idioms across matplotlib, seaborn, plotnine, and plotly — pick
the stack that fits the figure (matplotlib/seaborn for most static print figures;
plotnine if the user thinks in grammar-of-graphics / ggplot; plotly for interactive or
HTML supplements).

**Compile and run the code** to produce the actual image — don't just write a script and
assume it works. Fix errors. Re-run until it renders.

## Stage 6 — Self-check: read the rendered image, close the loop

This is the step people skip and regret. **Open the rendered image and actually look at
it** (read the PNG/PDF you just made). Verify the loop is closed and sensible:

- Does the figure show what stage-2's sentence claimed? If not, the figure, the data, or
  the claim is wrong — investigate before exporting.
- Are axes labeled with units? Is the legend complete and correct? Are group labels right?
- Do the numbers match the data (sanity-check a couple of values against the source)?
- Is n shown or stated? Are error bars defined? Are significance markers correct and
  placed on the right comparisons?
- Is anything misleading (truncated axis, hidden zero, overplotting, wrong color for
  colorblind readers)? Use colorblind-safe palettes by default.
- Does it fit the journal's size at the required font size without tiny unreadable text?

If something's off, loop back to the relevant stage and fix it. Tell the user what you
checked and what you changed. Only a figure that passes self-check moves on.

## Stage 7 — Export in order, then write the report

Once all figures pass self-check, **export them in numbered order** (Fig 1, Fig 2, …,
Table 1, …) at the journal's required format/resolution. Use `scripts/figstyle.py`'s
save helper so naming and resolution are consistent (e.g. `Fig1.pdf` + `Fig1.png` preview,
`Table1.csv`/`Table1.docx`). Export vector (PDF/SVG/EPS) for line art when the journal
allows, high-dpi raster (TIFF/PNG, ≥300 dpi, ≥600 for line/photo combos) otherwise.

Then generate **one figure report** in the user's chosen language (English / Chinese /
bilingual — see *Communication & language*). For every figure and table it must contain:
- the figure number and file name,
- the **caption**,
- the **annotations** (what each panel/marker/error bar/significance symbol means,
  statistical test used, n, error definition),
- the **in-text citation location** — the section and sentence where it should be cited,
- a reproducibility note (data source file + the script that generated it).

Deliver the report as a **Word document** (`.docx`) by default — researchers want to open,
read, and paste from it. Use `scripts/report_docx.py` (`build_report(..., lang=...)`), which
embeds each figure image, renders tables inline as three-line tables, and lays out the
captions/annotations/citations in the chosen language. Fall back to the Markdown template
`assets/report_template.md` if the user prefers plain text. This report is the hand-off
artifact: a co-author should be able to drop each figure into the manuscript at the named
location with the caption ready to paste.

---

## Reference files (read when the stage calls for them)

- `references/chart-selection.md` — data shape × claim → chart type, with anti-patterns.
- `references/statistical-methods.md` — choosing tests, assumptions, corrections, error
  bars, what to report.
- `references/journal-specs.md` — what journal requirements to look up and how presets work.
- `references/plotting-stacks.md` — publication-quality idioms for matplotlib, seaborn,
  plotnine, plotly.

## Bundled tools

- `scripts/figstyle.py` — apply a journal preset to matplotlib and save figures with
  consistent naming/resolution. Run `python scripts/figstyle.py --list` to see presets.
- `scripts/docx_tables.py` — `three_line_table(df, path, ...)` writes a DataFrame as an
  academic three-line (三线表) Word table; `add_three_line_table(doc, df, ...)` adds one to
  an existing document.
- `scripts/report_docx.py` — `build_report(path, title, meta, items)` assembles the stage-7
  figure report as a Word document with embedded figures and inline tables.
- `assets/presets.json` — editable journal presets (generic default + examples). Add the
  target journal here.
- `assets/report_template.md` — Markdown fallback for the figure report.
