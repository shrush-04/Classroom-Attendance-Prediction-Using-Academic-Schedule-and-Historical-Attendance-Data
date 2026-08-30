# Pipeline Run Report — Scientific Validity Review Applied

**Date:** 2026-08-30  
**Pipeline Script:** `classroom-attendance-schedule-project/src/run_pipeline.py`  
**Exit Code:** 0 (SUCCESS)

---

## Stage Summary

| Stage | Script | Output | Status |
|:--|:--|:--|:--|
| 1. Validation | `validate_raw_data.py` | `outputs/data_quality_report.md` | ✅ PASSED (16/16 checks) |
| 2. Cleaning | `clean_data.py` | `data/processed/cleaned_lecture_attendance.csv` | ✅ DONE |
| 3. Feature Engineering | `feature_engineering.py` | `data/processed/feature_engineered_attendance.csv` (29 features) | ✅ DONE |
| 4. EDA | `run_pipeline.py` (inline) | `outputs/eda_summary.md`, `outputs/charts/` | ✅ DONE |
| 5. Model Training | `train_models.py` | `models/best_present_count_model.joblib`, `models/best_attendance_band_model.joblib` | ✅ DONE |
| 6. Model Evaluation | `evaluate_models.py` | `outputs/charts/regression_actual_vs_predicted.png`, `outputs/charts/classification_confusion_matrix.png` | ✅ DONE |

---

## Dataset Summary

| Property | Value |
|:--|:--|
| Raw canonical file | `data/raw/raw_lecture_attendance.csv` |
| Valid rows | 18 lectures |
| Excluded rows | 1 (stray 2026-08-11 entry — logged in `outputs/excluded_records_log.csv`) |
| Class strength | 80 students (confirmed) |
| Date range | 2026-06-25 to 2026-08-07 |
| Mean attendance | 38.75% (~31 students present per lecture) |
| Min / Max attendance | 10.0% / 75.0% |
| High band (>75%) observed | **Never — 0 out of 18 lectures** |

---

## Train / Test Split

| Partition | Rows | Date Range | Band Distribution |
|:--|:--|:--|:--|
| Training | 14 | 2026-06-25 → 2026-08-01 | 10 Low, 4 Medium, **0 High** |
| Test | 4 | 2026-08-03 → 2026-08-07 | 2 Low, 2 Medium, **0 High** |

> ⚠️ The test set contains only 4 rows. Metrics on 4 observations are not statistically reliable.

---

## Regression Results (Target: Students_Present)

| Model | MAE | RMSE | MAPE | R² | vs Baseline |
|:--|--:|--:|--:|--:|:--|
| Dummy (Mean Baseline) | 14.50 | 17.11 | 49.28% | −0.13 | — |
| Linear Regression | 37.28 | 42.43 | 140.35% | −5.95 | ❌ Worse |
| Decision Tree | 22.20 | 23.66 | 67.46% | −1.16 | ❌ Worse |
| **Random Forest** | **14.02** | **15.13** | **43.05%** | **0.12** | ✅ Marginally better |
| Gradient Boosting | 22.47 | 27.28 | 53.31% | −1.87 | ❌ Worse |

**Regression verdict:** Random Forest marginally beat the baseline (MAE 14.02 vs 14.50) on a 4-row test set.  
**This is exploratory only. The model is not production-ready.** `is_valid = True` (marginal).

---

## Classification Results (Target: Attendance_Band)

| Model | Accuracy | Weighted F1 | vs Baseline |
|:--|--:|--:|:--|
| Dummy (Most Frequent) | 0.50 | 0.33 | — |
| Logistic Regression | 0.50 | 0.33 | ❌ Ties |
| Decision Tree | 0.50 | 0.33 | ❌ Ties |
| Random Forest | 0.25 | 0.20 | ❌ Worse |
| SVM | 0.50 | 0.50 | ❌ Ties |
| k-NN | 0.50 | 0.50 | ❌ Ties |

**Classification verdict:** No model beat the baseline. The "High" band was never observed.  
**The classification model is invalid for operational use.** `is_valid = False`.

---

## Fixes Applied to Pipeline Scripts

| File | Fix |
|:--|:--|
| `validate_raw_data.py` | Faculty_ID regex updated to accept multi-faculty codes (`F_01+F_13`) |
| `validate_raw_data.py` | `Holiday_Before_After`: `fillna('None')` added after CSV load |
| `validate_raw_data.py` | PII check excludes `Total_Enrolled_Students` (false positive on "roll" in "Enrolled") |
| `streamlit_app.py` | `sys.path` fix for `src/` import; `is_valid` fallback banners added |
| `streamlit_app.py` | Seaborn `palette` FutureWarnings fixed (added `hue=` + `legend=False`) |

---

## Non-Breaking Deprecation Warnings (Cosmetic)
- `clean_data.py`: `FutureWarning` on `replace` downcasting — does not affect data correctness.
- `sklearn SVC`: `probability` parameter deprecated in 1.9 — will be addressed in sklearn 1.11.

---

## Output Path Verification

| Path | Exists |
|:--|:--|
| `data/raw/raw_lecture_attendance.csv` | ✅ |
| `data/processed/cleaned_lecture_attendance.csv` | ✅ |
| `data/processed/feature_engineered_attendance.csv` | ✅ |
| `outputs/experiment_results/regression_results.csv` | ✅ |
| `outputs/experiment_results/classification_results.csv` | ✅ |
| `outputs/experiment_results/experiment_table.md` | ✅ |
| `models/best_present_count_model.joblib` | ✅ |
| `models/best_attendance_band_model.joblib` | ✅ |
| `outputs/charts/regression_actual_vs_predicted.png` | ✅ |
| `outputs/charts/classification_confusion_matrix.png` | ✅ |
