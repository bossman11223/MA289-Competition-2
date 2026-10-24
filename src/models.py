"""Model pipelines for the comparison and the SVM tuning grid.

Every pipeline is: grayscale pixels -> StandardScaler -> PCA -> classifier.
Input to each pipeline is the output of `src.data.to_grayscale`.
"""
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from src.features import pca, scaler

SEED = 0


def make_pipeline(clf, n_components=50):
    return Pipeline([
        ("scale", scaler()),
        ("pca", pca(n_components)),
        ("clf", clf),
    ])


def baseline_models(n_components=50):
    """The course comparison set: LDA, LogReg, KNN, Decision Tree, plus default SVMs."""
    return {
        "LDA": make_pipeline(LinearDiscriminantAnalysis(), n_components),
        "LogReg": make_pipeline(LogisticRegression(max_iter=5000), n_components),
        "KNN": make_pipeline(KNeighborsClassifier(n_neighbors=5), n_components),
        "DecisionTree": make_pipeline(DecisionTreeClassifier(random_state=SEED), n_components),
        "SVM-linear": make_pipeline(SVC(kernel="linear", probability=True, random_state=SEED), n_components),
        "SVM-rbf": make_pipeline(SVC(kernel="rbf", probability=True, random_state=SEED), n_components),
    }


def svm_param_grid():
    """Grid for GridSearchCV over the SVM pipeline (keys use the 'step__param' form)."""
    return [
        {
            "pca__n_components": [20, 50, 100],
            "clf__kernel": ["linear"],
            "clf__C": [0.01, 0.1, 1, 10],
        },
        {
            "pca__n_components": [20, 50, 100],
            "clf__kernel": ["rbf"],
            "clf__C": [0.1, 1, 10, 100],
            "clf__gamma": ["scale", 0.001, 0.01, 0.1],
        },
        {
            "pca__n_components": [20, 50, 100],
            "clf__kernel": ["poly"],
            "clf__degree": [2, 3],
            "clf__C": [0.1, 1, 10],
        },
    ]


def svm_pipeline(n_components=50):
    return make_pipeline(SVC(probability=True, random_state=SEED), n_components)
