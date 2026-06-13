# Figure & Table Report / 图表报告

> Fill one block per figure and table, in numbered order. Captions and annotations are
> bilingual (中文 + English). The "Citation location" tells the author exactly where to
> cite each item in the manuscript. Delete these instruction lines in the final report.
>
> 每个图/表填写一个区块,按编号顺序排列。图注与标注中英双语。"引用位置"指明在正文中
> 何处引用。完成后删除本说明行。

---

## Manuscript / 稿件
- **Title / 标题:**
- **Target journal / 目标期刊:**
- **Preset used / 使用的预设:** (e.g. `nature`, single column)
- **Date / 日期:**

## Asset index / 图表清单
| # | Type 类型 | File 文件 | One-line claim 一句话结论 |
|---|---|---|---|
| Fig 1 | figure | Fig1.pdf | |
| Fig 2 | figure | Fig2.pdf | |
| Table 1 | table | Table1.docx | |

---

## Figure 1 / 图 1 — <short title / 简短标题>

**File / 文件:** `Fig1.pdf` (+ `Fig1.png` preview) — <format>, <dpi>, <width> mm

**Claim / 论证:** This figure shows that … / 本图表明……

### Caption / 图注
**EN:** Figure 1. <Full caption: what is plotted, groups, what each element means.>
Data are <mean ± SEM / median [IQR]>; n = <n, unit of analysis>. <Test> was used;
*p < 0.05, **p < 0.01, ***p < 0.001; ns, not significant.

**中文:** 图 1。<完整图注:绘制了什么、分组、各元素含义。>数据为<均值 ± 标准误 /
中位数 [四分位距]>;n = <样本量,分析单位>。采用<统计检验>;*p < 0.05,**p < 0.01,
***p < 0.001;ns 表示无显著性差异。

### Annotations / 标注说明
- **Panels / 分图:** A = …, B = … / A = ……,B = ……
- **Axes / 坐标轴:** x = … (units), y = … (units)
- **Error bars / 误差棒:** <SD | SEM | 95% CI> — define explicitly / 明确定义
- **n / 样本量:** <n per group, what one observation is>
- **Statistics / 统计:** <test, paired/unpaired, correction, effect size + CI>
- **Significance markers / 显著性标记:** <which comparisons, convention>
- **Color / 颜色:** <palette; colorblind-safe? grayscale-safe?>
- **Scale choices / 标度:** <log axis? broken axis? — note if it affects interpretation>

### Citation location / 引用位置
- **Section / 章节:** Results → <subsection> / 结果 → <小节>
- **Sentence / 句子:** "…the effect was significant **(Fig. 1A)**." Insert after this
  sentence. / 在该句后引用。

### Reproducibility / 可复现性
- **Data source / 数据来源:** `<path/to/data.csv>` (sheet/columns: …)
- **Script / 脚本:** `<path/to/make_fig1.py>` (seed = …)
- **Key libraries / 主要依赖:** matplotlib x.y, seaborn x.y, scipy x.y

---

## Table 1 / 表 1 — <short title / 简短标题>

**File / 文件:** `Table1.docx` / `Table1.csv`

### Caption / 表注
**EN:** Table 1. <What the table summarizes; per-cell statistic; n; test footnotes.>
**中文:** 表 1。<表格汇总内容;每格统计量;样本量;检验脚注。>

### Annotations / 标注说明
- **Columns / 列:** <column = meaning, units, statistic shown>
- **Summary statistic / 汇总统计:** <mean ± SD | median [IQR] | n (%)>
- **Tests / 检验:** <test per row/column; correction>
- **Abbreviations / 缩写:** <define every abbreviation>

### Citation location / 引用位置
- **Section / 章节:** <e.g. Results, baseline characteristics / 结果,基线特征>
- **Sentence / 句子:** "Baseline characteristics are summarized in **Table 1**." 

### Reproducibility / 可复现性
- **Data source / 数据来源:** `<path/to/data.csv>`
- **Script / 脚本:** `<path/to/make_table1.py>`

---

<!-- Duplicate the Figure/Table blocks above for every additional asset, in order. -->
<!-- 为每个后续图表复制上述区块,按顺序排列。 -->
