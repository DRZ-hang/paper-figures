<div align="center">

[English](README.md) · **中文**

# 📊 paper-figures

### 用一个 AI 技能,把论文原始数据变成可直接投稿的统计图与表格。

[![Claude Skill](https://img.shields.io/badge/Claude-Skill-8A2BE2)](https://claude.com/claude-code)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Output](https://img.shields.io/badge/输出-英文%20%2F%20双语%20%2F%20中文-red.svg)](#-输出语言)
[![Reproducible](https://img.shields.io/badge/结果-100%25%20可复现-success.svg)](#-可复现)

</div>

---

**paper-figures** 是一个 [Claude](https://claude.com/claude-code) 技能:给它论文稿件和**原始
数据**,它就产出期刊可接受的图表——**所有结果都由 Python 代码生成、可重跑,绝不手绘、绝不
编造**。它会通读文章、找出需要配图的地方、按数据形态与论证目标选定统计方法与图型、套用目标
期刊的格式、绘制、**打开渲染出的图自检**、按编号导出,并交付一份 Word 报告(**全英 / 全中 /
中英双语任选**),其中包含每张图表的图注、标注与正文引用位置。

---

## ✨ 亮点

- 🔬 **数据优先、诚实** — 图只揭示数据中**本就为真**的事实;不截断坐标轴、不隐藏样本量 *n*、不编造 p 值。
- 📈 **自动选对图型** — 内置"数据形态 × 论证目标 → 图型 + 统计检验"的决策库。
- 🎓 **符合期刊规范** — 可配置预设(Nature / Science / Cell / IEEE / Elsevier / PLOS + 通用默认):栏宽、字体、dpi、矢量导出、色盲安全配色。
- 📐 **学术三线表(Word)** — 审稿人期待的标准表格格式。
- 🌏 **输出语言任你选** — 图注与报告可选全英、全中或中英双语。
- 🧰 **主流绘图栈全覆盖** — matplotlib · seaborn · plotnine · plotly,外加 lifelines 与 scikit-learn 做生存/机器学习。
- ♻️ **100% 可复现** — 固定随机种子、保留脚本、记录版本。

---

## 🖼 实际演示

[`examples/`](examples/) 中有两个基于**真实、开放许可论文**的完整端到端案例:输入原始数据,
输出下方的图与 Word 报告。下面每张图都由技能从所引论文的原始数据生成。

### 🐧 案例 1 — 图型多样性(南极企鹅)
**9 类图型 9 张图 + 3 张三线表** ·
[查看 ↗](examples/penguins-sexual-dimorphism/) ·
[📄 报告](examples/penguins-sexual-dimorphism/Figure_Report.docx)

| 散点 + 回归 | 云雨图 | PCA 双标图 |
|:---:|:---:|:---:|
| ![](examples/penguins-sexual-dimorphism/figures/Fig3.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig4.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig8.png) |
| **相关热图** | **直方图 + ECDF** | **森林图** |
| ![](examples/penguins-sexual-dimorphism/figures/Fig7.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig5.png) | ![](examples/penguins-sexual-dimorphism/figures/Fig9.png) |

### 🫀 案例 2 — 统计深度(心衰生存分析)
**Kaplan–Meier · Cox 回归 · 交叉验证 ROC + 2 张三线表** ·
[查看 ↗](examples/heart-failure-survival/) · 报告:
[英文](examples/heart-failure-survival/Figure_Report_EN.docx) ·
[双语](examples/heart-failure-survival/Figure_Report.docx) ·
[中文](examples/heart-failure-survival/Figure_Report_ZH.docx)

| Kaplan–Meier + 风险表 | Cox 风险比 | 交叉验证 ROC |
|:---:|:---:|:---:|
| ![](examples/heart-failure-survival/figures/Fig2.png) | ![](examples/heart-failure-survival/figures/Fig4.png) | ![](examples/heart-failure-survival/figures/Fig6.png) |

---

## 🎯 七阶段工作流

这是一套有纪律的工作流,而非一次性提示——就是一位严谨分析者会走的路径。

| | 阶段 | 做什么 |
|---|---|---|
| 1️⃣ | **通读文章** | 理解研究;列出所有适合配图/配表的地方。 |
| 2️⃣ | **图的立意** | 一句话:*"这张图要表明 ___。"* 然后定位精确的原始数据。 |
| 3️⃣ | **剖析与选型** | 按数据形态与论证目标选定统计方法与图型。 |
| 4️⃣ | **查规范** | 套用目标期刊预设(尺寸、字体、dpi、格式)。 |
| 5️⃣ | **绘制** | 编写并**运行** Python,得到真实图像。 |
| 6️⃣ | **自检** | **打开渲染图核对**闭环是否合理——标签、单位、*n*、显著性。 |
| 7️⃣ | **导出 + 报告** | 编号资产 + 你所选语言的 Word 报告(图注、标注、引用位置)。 |

---

## 💪 与众不同之处

| | 普通"帮我画个图" | **paper-figures** |
|---|---|---|
| 数据来源 | 截图 / 编造数字 | **你的原始数据,经可运行代码** |
| 图型选择 | 默认随便 | **匹配数据形态 + 论证目标** |
| 统计 | 常被略过或出错 | **设计恰当的检验,计算并报告** |
| 诚实性 | 截轴、藏 n | **强制:柱状图零基线、注明 n 与误差** |
| 期刊适配 | 手动反复调 | **一套预设,统一应用** |
| 自检 | 无 | **导出前先读自己渲染的图** |
| 交付物 | 一张 PNG | **编号矢量 + 位图 + Word 报告** |
| 可复现 | 否 | **固定种子 + 保留脚本** |

---

## 🌐 输出语言

告诉 Claude 你想要图注、标注和报告用哪种语言,或让它从稿件中自行判断:

- **全英** — 国际期刊 / 英文稿件
- **全中** — 中文学位论文或期刊
- **中英双语** — 图注双语(起稿阶段或双语团队很实用)

可对比心衰案例的同一份报告:
[英文版](examples/heart-failure-survival/Figure_Report_EN.docx)、
[双语版](examples/heart-failure-survival/Figure_Report.docx)、
[中文版](examples/heart-failure-survival/Figure_Report_ZH.docx)。

---

## 🚀 安装

**1. 获取技能** — 克隆本仓库,把 `paper-figures/` 文件夹放到 Claude 能发现技能的目录:

```bash
git clone https://github.com/DRZ-hang/paper-figures.git
# 用户级(所有项目可用):
cp -r paper-figures/paper-figures ~/.claude/skills/
# Windows PowerShell:
# Copy-Item -Recurse paper-figures\paper-figures $env:USERPROFILE\.claude\skills\
```

**2. 安装 Python 依赖:**

```bash
pip install -r paper-figures/requirements.txt
```

之后当你请求 Claude 为论文绘制图表时,技能会自动触发。

> 运行 `python paper-figures/scripts/figstyle.py --list` 可查看内置期刊预设。

---

## 📝 用法

直接把任务描述给 Claude,并提供稿件和数据:

> - *"这是我的稿件和 `results.xlsx`,帮我画结果部分的图,按 Nature 规范,图注用英文。"*
> - *"为这篇论文的实验数据画一张分组比较图,目标期刊是 IEEE 双栏,图注用中文。"*
> - *"把 `cohort.csv` 做成 Kaplan–Meier 图和一张基线特征三线表,出中英双语报告。"*

Claude 会通读文章、提出图表方案、选定统计与图型、套用期刊预设、用 Python 绘制、读图自检、
按编号导出,并给出你所选语言的 Word 报告。

---

## 📦 仓库结构

```
paper-figures/                     ← 技能本体(安装这个文件夹)
├── SKILL.md                       ← Claude 遵循的工作流
├── requirements.txt
├── references/                    ← 按需加载的决策指南
│   ├── chart-selection.md         ·  数据形态 × 论证目标 → 图型
│   ├── statistical-methods.md     ·  统计方法的选择与报告
│   ├── journal-specs.md           ·  期刊规范 + 预设系统
│   └── plotting-stacks.md         ·  matplotlib / seaborn / plotnine / plotly 写法
├── scripts/
│   ├── figstyle.py                ·  套用期刊预设 + 导出图
│   ├── docx_tables.py             ·  三线表 Word 表格
│   └── report_docx.py             ·  生成报告(lang = en / zh / bilingual)
└── assets/
    ├── presets.json               ·  可编辑的期刊预设
    └── report_template.md         ·  Markdown 报告备用模板

examples/                          ← 两个完整案例(数据 + 脚本 + 图 + 报告)
├── penguins-sexual-dimorphism/    ·  9 类图型,3 张表
└── heart-failure-survival/        ·  生存 / Cox / ROC,2 张表,3 种语言报告
```

---

## 🔬 可复现

仓库中所有图表均由 `examples/*/scripts/` 中的脚本运行生成,无任何手工改动;随机种子固定,
重跑即可精确重现;所有统计量已用原始数据独立复核。

```bash
cd examples/penguins-sexual-dimorphism/scripts
for f in make_*.py; do python "$f"; done   # 重新生成全部图、表与报告

# 为心衰案例选择报告语言:
cd ../../heart-failure-survival/scripts
PAPERFIG_LANG=zh python make_report.py      # 或 en / bilingual
```

---

## 📄 许可与数据署名

本项目**代码**以 [MIT 许可](LICENSE)发布。

两个案例完全基于**他人已发表、开放许可的数据**构建,数据著作权归下列原作者所有,转用请保留署名。

### 🐧 案例 1 — 南极企鹅
> **论文(CC BY 4.0):** Gorman KB, Williams TD, Fraser WR (2014). *Ecological Sexual Dimorphism
> and Environmental Variability within a Community of Antarctic Penguins (Genus Pygoscelis).*
> **PLOS ONE** 9(3): e90081. https://doi.org/10.1371/journal.pone.0090081
>
> **数据(CC0):** 由 Kristen Gorman 博士与帕尔默站南极长期生态研究项目(PAL-LTER)采集;
> 经 `palmerpenguins` R 包分发 —— Horst AM, Hill AP, Gorman KB (2020)。
> https://allisonhorst.github.io/palmerpenguins/ · doi:10.5281/zenodo.3960218

### 🫀 案例 2 — 心衰生存分析
> **论文(CC BY 4.0):** Chicco D, Jurman G (2020). *Machine learning can predict survival of
> patients with heart failure from serum creatinine and ejection fraction alone.* **BMC Medical
> Informatics and Decision Making** 20: 16. https://doi.org/10.1186/s12911-020-1023-5
>
> **原始数据采集:** Ahmad T, Munir A, Bhatti SH, Aftab M, Raza MA (2017). *Survival analysis of
> heart failure patients: A case study.* **PLOS ONE** 12(7): e0181001.
> https://doi.org/10.1371/journal.pone.0181001
>
> **数据集(CC BY 4.0):** UCI 机器学习库,*Heart failure clinical records*(数据集 519)。
> https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records

各案例的详细说明与许可:[企鹅](examples/penguins-sexual-dimorphism/README.md#source--attribution--来源与署名)
· [心衰](examples/heart-failure-survival/README.md#source--attribution--来源与署名)。

<div align="center">

**由 [Claude Code](https://claude.com/claude-code) 构建。** 如果它帮到了你的研究,欢迎点亮 ⭐。

</div>
