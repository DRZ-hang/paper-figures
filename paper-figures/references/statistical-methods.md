# Statistical Methods — choosing, justifying, reporting

The figure's statistics must match the **study design**, not the chart you'd like to draw.
Compute every statistic in code (scipy / statsmodels / pingouin / lifelines); never write a
p-value or CI you didn't calculate. This file helps you pick the right test, check its
assumptions, correct for multiplicity, and report it honestly in the caption.

## Table of contents
1. First, classify the design
2. Comparing groups (the common case)
3. Associations & regression
4. Categorical data
5. Survival / time-to-event
6. Assumptions — check, don't assume
7. Multiple comparisons
8. Error bars: SD vs SEM vs CI
9. Effect sizes & what to report
10. p-value hygiene

---

## 1. First, classify the design
Answer these before choosing a test:
- **Outcome type:** continuous, count, proportion, ordinal, time-to-event?
- **Number of groups/conditions:** 1, 2, or >2?
- **Paired or independent?** Repeated measures on the same unit → paired/within-subject.
- **Unit of analysis / n:** what is one independent observation? Pseudoreplication (treating
  technical replicates as independent) inflates n and is a top reviewer complaint.
- **Covariates** to adjust for?

## 2. Comparing groups (continuous outcome)
- **2 groups, independent, ~normal:** Welch's t-test (don't assume equal variance).
  Non-normal/small n/ordinal → Mann–Whitney U.
- **2 groups, paired:** paired t-test; non-normal → Wilcoxon signed-rank.
- **>2 groups, independent:** one-way ANOVA (+ post-hoc Tukey) if assumptions hold; else
  Kruskal–Wallis (+ Dunn with correction).
- **>2 conditions, repeated measures:** repeated-measures ANOVA / mixed model; non-normal →
  Friedman.
- **Two factors:** two-way ANOVA / linear model with interaction.
- **Nested/clustered data (cells within animals, repeated patients):** use a linear
  **mixed-effects model** (statsmodels `mixedlm`), not a plain test — this is the correct
  fix for pseudoreplication.

## 3. Associations & regression
- Linear association, continuous, ~normal → **Pearson r**; monotonic/non-normal/ordinal →
  **Spearman ρ**. Report r/ρ, CI, p, and n.
- Predicting a continuous outcome → linear regression; report coefficients, CI, R².
- Always plot the data behind a correlation (Anscombe's quartet: same r, wildly different
  data). Don't report r without the scatter.

## 4. Categorical data
- 2×2 or R×C counts → χ² test; small expected counts (<5) → Fisher's exact.
- Paired proportions → McNemar.
- Report counts and proportions, the test, and an effect measure (odds/risk ratio with CI).

## 5. Survival / time-to-event
- Kaplan–Meier estimate + **log-rank** test for group differences.
- Adjusted analysis → Cox proportional-hazards; report HR with CI and check the
  proportional-hazards assumption. Use `lifelines`.

## 6. Assumptions — check, don't assume
- **Normality:** look at the distribution (histogram/QQ) more than Shapiro p-values; small
  n makes normality tests useless, large n makes them over-sensitive.
- **Equal variance:** Levene's test / just use Welch by default.
- **Independence:** the design tells you, not a test. Clustered data → mixed model.
- If assumptions fail, switch to a non-parametric test or a model that fits, and say so.

## 7. Multiple comparisons
If you run many tests (multiple pairwise comparisons, many outcomes, omics), **correct**:
- Few planned comparisons → Bonferroni/Holm.
- Many tests, discovery setting → Benjamini–Hochberg FDR (report q-values).
State the correction in the caption. Marking 15 uncorrected pairwise stars is misleading.

## 8. Error bars: SD vs SEM vs CI
Pick deliberately and **always define it in the caption** — this is the single most common
caption omission.
- **SD** describes the spread of the data (how variable individuals are).
- **SEM** describes the precision of the mean estimate (≈ SD/√n) — it shrinks with n and is
  *not* a description of data spread; don't use it to imply small variability.
- **95% CI** is usually the most interpretable for inference.
Whatever you choose, write "error bars = mean ± SEM (n = …)" etc.

## 9. Effect sizes & what to report
p-values alone are not enough. Report an **effect size** with CI: Cohen's d / Hedges' g
(group means), r/ρ (correlation), odds/risk ratio, hazard ratio, η²/partial-η² (ANOVA).
A figure caption should let the reader judge *how big* the effect is, not just whether
p<0.05.

## 10. p-value hygiene
- Report exact p (e.g. p = 0.013), not "p < 0.05", until very small (then "p < 0.001").
- Significance markers convention (state it): ns, * p<0.05, ** p<0.01, *** p<0.001.
- Don't imply causation from an association.
- State the test, the n, the tails, and any correction for every reported statistic.
- Pre-specified vs exploratory: label exploratory comparisons as such.
