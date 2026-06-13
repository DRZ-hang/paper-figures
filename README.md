<div align="center">

# 📊 paper-figures

### Turn your paper's raw data into publication-ready figures & tables — with one AI skill.
### 让 AI 把论文原始数据,变成可直接投稿的统计图与三线表。

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-8A2BE2)](https://claude.com/claude-code)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bilingual](https://img.shields.io/badge/docs-中文%20%2F%20English-red.svg)](#)
[![Reproducible](https://img.shields.io/badge/results-100%25%20reproducible-success.svg)](#-reproducibility--可复现)

</div>

---

**paper-figures** is a [Claude](https://claude.com/claude-code) skill that takes a manuscript
and its **raw data** and produces the figures and tables a journal will accept — every result
generated and re-runnable from Python, never hand-drawn, never fabricated. It reads the paper,
finds where visuals are needed, picks the right statistics and chart for the data, applies the
target journal's formatting, renders, **checks its own output by looking at the rendered image**,
exports numbered assets, and hands you a **bilingual (中文/English) Word report** with every
caption, annotation, and in-text citation location.

> 一句话:给它论文和原始数据,它就按"通读 → 找配图点 → 选统计与图型 → 套期刊规范 → 绘制
> → 读图自检 → 编号导出 → 生成双语 Word 报告"的完整流程,产出可投稿的图表。**结果全部由
> Python 代码生成、可复现,绝不手绘或编造。**

---

## ✨ Highlights / 亮点

- 🔬 **Data-first & honest** — the figure only ever reveals what's *already true* in the data. No truncated axes, no hidden *n*, no fabricated p-values. 数据优先、诚实:不截轴、不藏样本量、不编造显著性。
- 📈 **The right chart, chosen for you** — a built-in decision guide maps your data's *shape* + your *claim* to the correct chart and statistical test. 内置"数据形态 × 论证目标 → 图型 + 检验"决策库。
- 🎓 **Journal-ready formatting** — configurable presets (Nature / Science / Cell / IEEE / Elsevier / PLOS + a generic default); column widths, fonts, dpi, vector export, colorblind-safe palettes. 期刊预设可配置可扩展。
- 📐 **Academic three-line tables (三线表)** in Word, the standard format reviewers expect. 输出标准学术三线表(Word)。
- 🌏 **Bilingual deliverable** — captions, annotations and citation locations in both Chinese and English. 中英双语交付。
- 🧰 **Full plotting stack** — matplotlib · seaborn · plotnine · plotly, plus lifelines & scikit-learn for survival/ML. 主流绘图与统计库全覆盖。
- ♻️ **100% reproducible** — fixed seeds, saved scripts, recorded versions. 固定种子、保留脚本、可一键重建。

---

## 🖼 See it in action / 演示

Two complete, end-to-end runs on **real, openly-licensed published papers** live in
[`examples/`](examples/) — raw data in, the figures and a Word report below out. Every image
here was produced by the skill from the cited paper's own data.

> 两个基于**真实开放许可论文**的完整案例见 [`examples/`](examples/),下方所有图均由技能从原始数据生成。

### 🐧 Example 1 — Chart *variety* (Antarctic penguins) / 图型多样性
**9 figures across 9 chart families + 3 three-line tables** ·
[explore ↗](examples/penguins-sexual-dimorphism/) ·
[📄 Word report](examples/penguins-sexual-dimorphism/Figure_Report.docx)

| Scatter + regression | Raincloud | PCA biplot |
|:---:|:---:|:---:|
| ![](examples/penguins-sexual-dimorphism/figures/Fig3.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig4.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig8.png) |
| **Correlation heatmap** | **Histogram + ECDF** | **Forest plot** |
| ![](examples/penguins-sexual-dimorphism/figures/Fig7.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig5.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig9.png) |

### 🫀 Example 2 — Statistical *depth* (heart-failure survival) / 统计深度
**Kaplan–Meier · Cox regression · cross-validated ROC + 2 three-line tables** ·
[explore ↗](examples/heart-failure-survival/) ·
[📄 Word report](examples/heart-failure-survival/Figure_Report.docx)

| Kaplan–Meier + risk table | Cox hazard ratios | Cross-validated ROC |
|:---:|:---:|:---:|
| ![](examples/heart-failure-survival/figures/Fig2.png) | ![](examples/heart-failure-survival/figures/Fig4.png) | ![](examples/heart-failure-survival/figures/Fig6.png) |

---

## 🎯 The 7-stage workflow / 七阶段工作流

The skill is a disciplined workflow, not a one-shot prompt — the same path a careful analyst takes.

| | Stage | What happens / 做什么 |
|---|---|---|
| 1️⃣ | **Read the paper** 通读文章 | Understand the study; list every place a figure/table would strengthen it. |
| 2️⃣ | **Frame the figure** 立意 | One sentence: *"This figure shows that ___."* Then locate the exact raw data. |
| 3️⃣ | **Analyze & decide** 选型 | Pick the statistic + chart from the data's shape and the claim. |
| 4️⃣ | **Check standards** 查规范 | Apply the target journal's preset (size, fonts, dpi, format). |
| 5️⃣ | **Plot** 绘制 | Write & *run* Python to render the real figure. |
| 6️⃣ | **Self-check** 自检 | **Open the rendered image and verify** the loop closes — labels, units, *n*, significance. |
| 7️⃣ | **Export & report** 导出+报告 | Numbered assets + a bilingual Word report (captions, annotations, citation locations). |

---

## 💪 Why it's different / 优势

| | Typical "make me a chart" | **paper-figures** |
|---|---|---|
| Source | screenshots / made-up numbers | **your raw data, via runnable code** |
| Chart choice | whatever's default | **matched to data shape + claim** |
| Statistics | often skipped or wrong | **design-appropriate tests, computed, reported** |
| Honesty | truncated axes, hidden n | **enforced: zero-baseline bars, stated n & error** |
| Journal fit | manual fiddling | **one preset, applied consistently** |
| Self-review | none | **reads its own rendered image before exporting** |
| Deliverable | a PNG | **numbered vector + raster + a bilingual Word report** |
| Reproducible | no | **fixed seeds + saved scripts** |

---

## 🚀 Install & deploy / 安装部署

**1. Get the skill** — clone this repo and drop the `paper-figures/` folder where Claude finds skills:

```bash
git clone https://github.com/<your-username>/paper-figures.git
# user-level (all projects):
cp -r paper-figures/paper-figures ~/.claude/skills/
# Windows PowerShell:
# Copy-Item -Recurse paper-figures\paper-figures $env:USERPROFILE\.claude\skills\
```

**2. Install the Python dependencies:**

```bash
pip install -r paper-figures/requirements.txt
```

That's it — the skill triggers automatically when you ask Claude to make figures or tables for
a paper. 安装后,当你请求 Claude 为论文绘制图表时即自动触发。

> Run `python paper-figures/scripts/figstyle.py --list` to see the bundled journal presets.

---

## 📝 Usage / 用法

Just describe the task to Claude with your manuscript and data at hand:

> - *"Here's my manuscript and `results.xlsx` — make the figures for the Results section, formatted for Nature."*
> - *"为这篇论文的实验数据画一张分组比较图,目标期刊是 IEEE 双栏。"*
> - *"Turn `cohort.csv` into a Kaplan–Meier figure and a baseline characteristics table (三线表)."*
> - *"我有一份 CSV,帮我决定该用什么统计图并画出来,生成中英双语报告。"*

Claude reads the paper, proposes a figure/table plan, picks the statistics and chart type,
applies the journal preset, renders with Python, self-checks the image, exports the numbered
assets, and gives you the bilingual Word report.

---

## 📦 What's in the box / 仓库结构

```
paper-figures/                     ← the skill (install this folder)
├── SKILL.md                       ← the workflow Claude follows
├── requirements.txt
├── references/                    ← decision guides loaded on demand
│   ├── chart-selection.md         ·  data shape × claim → chart type
│   ├── statistical-methods.md     ·  choosing & reporting statistics
│   ├── journal-specs.md           ·  journal requirements + preset system
│   └── plotting-stacks.md         ·  matplotlib / seaborn / plotnine / plotly idioms
├── scripts/
│   ├── figstyle.py                ·  apply journal preset + export figures
│   ├── docx_tables.py             ·  three-line (三线表) Word tables
│   └── report_docx.py             ·  assemble the bilingual Word report
└── assets/
    ├── presets.json               ·  editable journal presets
    └── report_template.md         ·  Markdown report fallback

examples/                          ← two full worked examples (data + scripts + figures + reports)
├── penguins-sexual-dimorphism/    ·  9 chart families, 3 tables
└── heart-failure-survival/        ·  survival / Cox / ROC, 2 tables
```

---

## 🔬 Reproducibility / 可复现

Every figure and table in this repo was generated by running the scripts in
`examples/*/scripts/` — no manual editing. Random seeds are fixed, so re-running reproduces the
exact output. The statistics have been independently re-derived from the raw data and verified.

> 仓库中所有图表均由 `examples/*/scripts/` 脚本运行生成,无手工改动;随机种子固定,可精确重现;
> 所有统计量已用原始数据独立复核。

```bash
cd examples/penguins-sexual-dimorphism/scripts
for f in make_*.py; do python "$f"; done   # regenerates every figure, table & the Word report
```

---

## 📄 License & data attribution / 许可与数据署名

This project's **code** is released under the [MIT License](LICENSE).

The two worked examples reuse real published datasets under open licenses — please keep the
attribution if you reuse them:

- 🐧 **Penguins** — Gorman, Williams & Fraser (2014), *PLOS ONE* 9(3):e90081 (CC BY 4.0); data via the `palmerpenguins` package (CC0). [Details](examples/penguins-sexual-dimorphism/README.md#source--attribution--来源与署名)
- 🫀 **Heart failure** — Chicco & Jurman (2020), *BMC Med Inform Decis Mak* 20:16 (CC BY 4.0); UCI dataset 519 (CC BY 4.0). [Details](examples/heart-failure-survival/README.md#source--attribution--来源与署名)

<div align="center">

**Built with [Claude Code](https://claude.com/claude-code).** If this helps your research, please ⭐ the repo.
如果它帮到了你的研究,欢迎点亮 ⭐。

</div>
