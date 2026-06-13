"""Figure 6 — Does serum creatinine + ejection fraction predict death as well as
the full feature set? (cross-validated ROC).

Stage 2 claim (the paper's headline): "Two features — serum creatinine and ejection
fraction — predict mortality almost as well as all clinical features."
Stage 3: binary classification performance -> ROC curves with AUC. To avoid an
optimistic in-sample estimate we use 5-fold cross-validated predicted probabilities.
Follow-up `time` is deliberately EXCLUDED as a predictor (it is post-baseline and
would leak the outcome). Data: heart_failure_*.csv. Uses scikit-learn.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import roc_curve, roc_auc_score

from _common import load_clean, FIGDIR, CONTINUOUS, BINARY
from figstyle import apply_preset, save_figure, get_preset

ps = apply_preset("generic", column="single", aspect=0.92)
colors = get_preset("generic")["palette_colors"]
df = load_clean()
y = df["death_event"].values
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

all_feats = [c for c, *_ in CONTINUOUS] + [c for c, _ in BINARY]  # excludes `time`
two_feats = ["serum_creatinine", "ejection_fraction"]
models = [
    ("All clinical features", all_feats, colors[5]),
    ("Creatinine + ejection fraction", two_feats, colors[6]),
]

fig, ax = plt.subplots()
for name, feats, c in models:
    X = df[feats].values
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    proba = cross_val_predict(clf, X, y, cv=cv, method="predict_proba")[:, 1]
    fpr, tpr, _ = roc_curve(y, proba)
    auc = roc_auc_score(y, proba)
    ax.plot(fpr, tpr, color=c, lw=1.3, label=f"{name} (AUC = {auc:.2f})")

ax.plot([0, 1], [0, 1], color="grey", lw=0.6, ls="--")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.legend(frameon=False, loc="lower right", fontsize=ps["tick_label_pt"])
ax.set_title("Predicting in-study death (5-fold CV)", fontsize=ps["title_pt"])

save_figure(fig, number="6", preset="generic", outdir=str(FIGDIR), kind="line")
print("Fig6 done — cross-validated ROC")
