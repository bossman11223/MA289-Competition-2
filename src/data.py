"""Loading the Kaggle CSVs and turning them into usable arrays.

Each row stores a 64x64 spectrogram image flattened as RGBA (16,384 columns).
R, G, and B are identical and alpha is always 255, so only every 4th column
carries information. `to_grayscale` keeps just those 4,096 pixels.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
IMG_SIDE = 64


def load_train(path=RAW_DIR / "train.csv"):
    """Return (ids, X, y) where X is the raw 16,384-column RGBA array."""
    df = pd.read_csv(path)
    ids = df["ID"].to_numpy()
    y = df["Label"].to_numpy()
    X = df.drop(columns=["ID", "Label"]).to_numpy(dtype=np.float32)
    return ids, X, y


def load_test(path=RAW_DIR / "test.csv"):
    """Return (ids, X) for the test set, in the original row order."""
    df = pd.read_csv(path)
    ids = df["ID"].to_numpy()
    X = df.drop(columns=["ID"]).to_numpy(dtype=np.float32)
    return ids, X


def to_grayscale(X):
    """Keep only the R channel: (n, 16384) -> (n, 4096)."""
    return X[:, 0::4]


def to_images(X_gray):
    """Reshape grayscale rows into (n, 64, 64) images for plotting."""
    return X_gray.reshape(-1, IMG_SIDE, IMG_SIDE)
