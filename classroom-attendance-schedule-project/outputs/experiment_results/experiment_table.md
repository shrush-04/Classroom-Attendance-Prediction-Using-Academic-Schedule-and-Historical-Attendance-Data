# Model Training Experiment Results — Scientific Validity Review

> ⚠️ **Scientific Validity Notice:** The dataset contains only **18 valid lecture observations**. The
> chronological 80/20 split yields 14 training rows and **4 test rows**. Metrics computed on a
> 4-row test set are statistically unreliable and cannot establish generalization. All results
> below are **exploratory only** and must not be cited as evidence of production-ready performance.

---

- **Total Valid Lectures:** 18
- **Chronological Train Split:** 14 rows (2026-06-25 → 2026-08-01)
- **Chronological Test Split:** 4 rows (2026-08-03 → 2026-08-07)
- **Historical Mean Attendance Percentage:** 38.75%
- **Historical Mean Students Present:** 31.0 out of 80 enrolled

---

## 1. Class Distribution (Attendance Band)

| Band | Definition | All Data (n=18) | Train (n=14) | Test (n=4) |
|:--|:--|--:|--:|--:|
| Low | < 50% | 12 | 10 | 2 |
| Medium | 50% – 75% | 6 | 4 | 2 |
| **High** | **> 75%** | **0** | **0** | **0** |

> 🔴 **The "High" attendance band (>75%) was never observed in any of the 18 recorded lectures.**
> The maximum recorded attendance was exactly 75.0%. Therefore, no model can learn to predict
> the "High" class, and any High prediction from this system would be fabricated.

---

## 2. Regression Models (Target: Students_Present)

| Model | MAE | RMSE | MAPE (%) | R² |
|:--|--:|--:|--:|--:|
| Dummy Regressor (Mean Baseline) | 14.5000 | 17.1092 | 49.28 | −0.1291 |
| Linear Regression | 37.2796 | 42.4341 | 140.35 | −5.9456 |
| Decision Tree Regressor | 22.2000 | 23.6587 | 67.46 | −1.1591 |
| **Random Forest Regressor** | **14.0192** | **15.1268** | **43.05** | **0.1174** |
| Gradient Boosting Regressor | 22.4673 | 27.2761 | 53.31 | −1.8698 |

### Regression Interpretation

- The **Random Forest Regressor** is the only model to marginally beat the dummy baseline
  (MAE 14.02 vs 14.50 — a reduction of 0.48 students on a 4-row test set).
- **This marginal improvement cannot establish reliable generalization.** With only 4 test
  observations, the difference is within random noise.
- The R² of 0.1174 indicates the model explains only ~12% of variance in the test set.
- The MAPE of 43.05% means predictions are off by 43% on average — operationally imprecise.
- All other regression models perform **worse** than the naive mean-predictor baseline.
- **Verdict: Exploratory result only. The regression model is not production-ready.**

---

## 3. Classification Models (Target: Attendance_Band — Low/Medium only)

| Model | Accuracy | Weighted Precision | Weighted Recall | Weighted F1 |
|:--|--:|--:|--:|--:|
| Dummy Classifier (Most Frequent) | 0.5000 | 0.2500 | 0.5000 | 0.3333 |
| Logistic Regression | 0.5000 | 0.2500 | 0.5000 | 0.3333 |
| Decision Tree Classifier | 0.5000 | 0.2500 | 0.5000 | 0.3333 |
| Random Forest Classifier | 0.2500 | 0.1667 | 0.2500 | 0.2000 |
| Support Vector Machine | 0.5000 | 0.5000 | 0.5000 | 0.5000 |
| k-Nearest Neighbors | 0.5000 | 0.5000 | 0.5000 | 0.5000 |

### Classification Interpretation

- **No classification model outperformed the dummy baseline.** The best trained models
  (Logistic Regression, Decision Tree) exactly match the dummy at 0.50 accuracy.
- **The "High" attendance class was never observed** in any of the 18 lectures (max was 75.0%).
  The classifier was trained and tested on a 2-class problem (Low / Medium) only.
- On a 4-row test set with 2 Low and 2 Medium observations, a model that predicts "Low" for
  every row achieves 50% accuracy by definition — this is what the dummy does.
- **Verdict: The classification model is invalid for operational use.** Attendance-band
  decisions must not be automated from this classifier.

---

## 4. Baseline Comparison Summary

| | Regression | Classification |
|:--|:--|:--|
| Baseline | Dummy Regressor (predicts training mean) | Dummy Classifier (predicts most frequent class: Low) |
| Baseline MAE / Accuracy | 14.5000 | 0.5000 |
| Best Trained Model | Random Forest | Logistic Regression |
| Best Model MAE / Accuracy | 14.0192 | 0.5000 |
| Improvement | 0.48 MAE reduction on 4-row test | No improvement — exact tie |
| Beats Baseline? | Marginally (not statistically significant) | No |
| is_valid | `True` (marginal, exploratory) | `False` |
| Recommended fallback | Historical mean: 38.75% / 31 students present | Historical most-frequent class: Low |

---

## 5. Scientific Validity Assessment

> **The available dataset contained only 18 valid lecture observations. The regression experiment
> produced a small improvement over the historical-average baseline, but the test set contained
> only four observations, so the result is exploratory and cannot establish reliable
> generalization. The classification model did not outperform the dummy baseline and should not
> be used for operational decisions. More physically verified lecture records are required before
> deploying a reliable predictive system.**

### Specific Limitations Confirmed by Data

1. **n=18 total observations** — statistically insufficient for generalizable supervised learning.
2. **4-row test set** — no metric computed on 4 rows can be statistically meaningful.
3. **High class never observed** — the 3-band classification schema cannot be fully validated.
4. **Max attendance = 75%** — the upper boundary of data barely touches the Medium/High threshold.
5. **MAPE = 43%** — even the best regression model has a 43% average relative error.
6. **R² = 0.117** — the model explains only ~12% of the variance in held-out data.
7. **All other regressors worse than baseline** — 4 of 5 models degrade relative to the naive mean.
8. **All classifiers at or below baseline** — no learned pattern generalizes to unseen data.

### Recommended Next Step

Physically verify and log additional lecture attendance records. Every new semester month
that is logged and added to `data/raw/raw_lecture_attendance.csv` improves model reliability.
Re-run `python src/run_pipeline.py` after each batch of new records is added.
