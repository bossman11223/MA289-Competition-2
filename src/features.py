"""Feature transforms used inside model pipelines.

Everything here is a scikit-learn transformer so it is fit only on the
training fold during cross-validation and never sees validation/test data.
"""
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from src.data import IMG_SIDE


class Downsample(BaseEstimator, TransformerMixin):
    """Average-pool 64x64 images into blocks (e.g. factor=4 -> 16x16 = 256 features)."""

    def __init__(self, factor=2):
        self.factor = factor

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        f = self.factor
        side = IMG_SIDE // f
        imgs = X.reshape(-1, side, f, side, f)
        return imgs.mean(axis=(2, 4)).reshape(len(X), -1)


def scaler():
    return StandardScaler()


def pca(n_components=50):
    return PCA(n_components=n_components, random_state=0)
