"""Cross-validated ROC AUC, ROC plots, the comparison table, and submission writing."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import RocCurveDisplay
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_val_score

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
FIG_DIR = RESULTS_DIR / "figures"
SUB_DIR = ROOT / "submissions"


def cv_splitter(n_splits=5, seed=0):
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)


def compare_models(models, X, y, cv=None):
    """Return a DataFrame of mean/std CV ROC AUC for each model, best first."""
    cv = cv or cv_splitter()
    rows = []
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=cv, scoring="roc_auc")
        rows.append({"model": name, "cv_auc_mean": scores.mean(), "cv_auc_std": scores.std()})
    return pd.DataFrame(rows).sort_values("cv_auc_mean", ascending=False).reset_index(drop=True)


def plot_cv_roc(models, X, y, cv=None, filename="roc_comparison.png"):
    """Overlay out-of-fold ROC curves for each model and save to results/figures."""
    cv = cv or cv_splitter()
    fig, ax = plt.subplots(figsize=(6, 6))
    for name, model in models.items():
        proba = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
        RocCurveDisplay.from_predictions(y, proba, name=name, ax=ax)
    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_title("Out-of-fold ROC curves")
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")
    return fig


def write_submission(ids, proba, filename):
    """Write the Kaggle file: header + ID, Probability, in test-set order."""
    SUB_DIR.mkdir(parents=True, exist_ok=True)
    path = SUB_DIR / filename
    pd.DataFrame({"ID": ids, "Probability": proba}).to_csv(path, index=False)
    return path
