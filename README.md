# MA289 Competition 2 — Spoken Digit Classification (6 vs 7)

Binary classification of spoken digits **6** (label `0`) vs **7** (label `1`) from the Spoken MNIST audio dataset, using classical ML with an **SVM** as the final model.

- **Predict:** probability that each test recording is a 7
- **Metric:** ROC AUC (higher is better)
- **Submission:** CSV with header and exactly two columns, `ID,Probability`, in the same row order as `test.csv`
- **Due:** 2359 16 OCT 2026

## Data

| File | Rows | Columns |
|---|---|---|
| `train.csv` | 400 (200 sixes / 200 sevens) | `ID`, `x0`–`x16383`, `Label` |
| `test.csv` | 200 | `ID`, `x0`–`x16383` |

The 16,384 features are a **64×64 spectrogram image flattened as RGBA**. R, G, and B are identical and alpha is always 255, so the real signal is 4,096 grayscale pixels (values 0–251). `src.data.to_grayscale` does this reduction. The `.wav` files in `data/raw/` are example recordings for listening only.

## Approach

1. **EDA:** view spectrograms, class-mean images, and PCA explained variance.
2. **Baselines:** grayscale → `StandardScaler` → `PCA(50)` → classifier, for LDA, Logistic Regression, KNN, Decision Tree, linear SVM, and RBF SVM. Each is scored with 5-fold stratified CV ROC AUC.
3. **SVM tuning:** `GridSearchCV` over kernel (linear/rbf/poly), `C`, `gamma`/`degree`, and the number of PCA components.
4. **Final:** refit the best SVM on all training data, then predict test probabilities.

Scaling and PCA are inside the pipeline, so they are fit only on training folds and never on validation or test data.

## Project structure

```
├── README.md
├── requirements.txt
├── kaggle_prompt.txt          # competition description
├── data/
│   ├── raw/                   # Kaggle files (gitignored)
│   └── processed/             # gitignored
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_baselines.ipynb
│   ├── 03_svm_tuning.ipynb
│   └── 04_final_submission.ipynb
├── src/
│   ├── data.py                # loading, RGBA → grayscale, reshape to images
│   ├── features.py            # scaler, PCA, Downsample (average pooling)
│   ├── models.py              # baseline pipelines + SVM param grid
│   └── evaluate.py            # CV AUC table, ROC plots, submission writer
├── results/
│   ├── figures/
│   └── model_comparison.csv
└── submissions/
```

## Setup

```bash
pip install -r requirements.txt
# put train.csv and test.csv in data/raw/
jupyter notebook notebooks/
```

Run the notebooks in order. Notebook 02 writes `results/model_comparison.csv` and notebook 04 writes `submissions/submission_v1.csv`.

## Results

| Model | CV ROC AUC | Kaggle AUC |
|---|---|---|
| SVM (linear, defaults) | 1.000 ± 0.000 | |
| Logistic Regression | 0.999 ± 0.001 | |
| SVM (rbf, defaults) | 0.999 ± 0.002 | |
| LDA | 0.998 ± 0.003 | |
| KNN (k=5) | 0.991 ± 0.007 | |
| Decision Tree | 0.845 ± 0.042 | |

*(Baseline run: grayscale + scale + PCA 50, 5-fold stratified CV.)*
