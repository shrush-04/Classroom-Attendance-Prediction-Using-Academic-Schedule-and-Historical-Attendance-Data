# FINAL CLASSROOM PROJECT AUDIT — Scientific Validity Review

**Project:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data  
**Date:** 2026-08-30  
**Scope:** MCA Final Year, Semester III — Mobile Application Development (Theory & Practical)

---

## ✅ Safety Protocol Compliance

| Rule | Status |
|:--|:--|
| No synthetic/generated attendance rows | ✅ All 18 rows come from real physical register headcounts |
| No student PII (names, roll numbers, emails) | ✅ Dataset is purely lecture-level aggregates |
| No private faculty mapping in outputs | ✅ Only anonymous IDs used (F_01, F_02) |
| No `private_original_data/` in outputs | ✅ Complied |
| Source files preserved as read-only inputs | ✅ Originals untouched |
| All outputs saved to official project paths | ✅ Complied |
| No invented metrics or fabricated rows | ✅ All values from actual pipeline run |

---

## 📁 Output Path Verification

| Path | Rows / Status |
|:--|:--|
| `data/raw/raw_lecture_attendance.csv` | 18 rows ✅ |
| `data/processed/cleaned_lecture_attendance.csv` | 18 rows ✅ |
| `data/processed/feature_engineered_attendance.csv` | 18 rows, 29 features ✅ |
| `outputs/excluded_records_log.csv` | 1 excluded row ✅ |
| `outputs/data_quality_report.md` | 16/16 checks passed ✅ |
| `outputs/data_alignment_report.md` | Present ✅ |
| `outputs/eda_summary.md` | Present ✅ |
| `outputs/experiment_results/regression_results.csv` | 5 models ✅ |
| `outputs/experiment_results/classification_results.csv` | 6 models ✅ |
| `outputs/experiment_results/experiment_table.md` | Full validity review ✅ |
| `outputs/pipeline_run_report.md` | Present ✅ |
| `outputs/charts/regression_actual_vs_predicted.png` | Present ✅ |
| `outputs/charts/classification_confusion_matrix.png` | Present ✅ |
| `models/best_present_count_model.joblib` | `is_valid=True` (exploratory) ✅ |
| `models/best_attendance_band_model.joblib` | `is_valid=False` ✅ |
| `report/project_report.pdf` | Verified (31 pages) ✅ |
| `presentation/project_presentation.pptx` | Verified (13 slides) ✅ |

---

## 🔬 Scientific Validity Status

> **The available dataset contained only 18 valid lecture observations. The regression experiment
> produced a small improvement over the historical-average baseline, but the test set contained
> only four observations, so the result is exploratory and cannot establish reliable
> generalization. The classification model did not outperform the dummy baseline and should not
> be used for operational decisions. More physically verified lecture records are required before
> deploying a reliable predictive system.**

### Dataset Facts (Confirmed from Actual Data)

| Fact | Value |
|:--|:--|
| Total valid lectures | 18 |
| Training observations | 14 (2026-06-25 → 2026-08-01) |
| Test observations | 4 (2026-08-03 → 2026-08-07) |
| Minimum attendance | 10.0% |
| Maximum attendance | 75.0% |
| Mean attendance | **38.75%** |
| Mean students present | **31.0 out of 80** |
| Low band (<50%) count | 12 (67% of data) |
| Medium band (50–75%) count | 6 (33% of data) |
| **High band (>75%) count** | **0 — NEVER OBSERVED** |

---

## 🤖 Model Validity Assessment

### Regression — `is_valid = True` (Exploratory)

| | Value |
|:--|:--|
| Dummy Baseline MAE | 14.5000 |
| Random Forest MAE | **14.0192** |
| Improvement | 0.48 students (on 4 test rows) |
| RMSE | 15.1268 |
| R² | 0.1174 (~12% variance explained) |
| MAPE | 43.05% average relative error |
| Verdict | **EXPLORATORY ONLY — not production-ready** |

> Random Forest marginally beat the mean baseline on a 4-row test set. This margin (0.48 MAE) is within noise range for such a small test. The result cannot establish generalization.

### Classification — `is_valid = False`

| | Value |
|:--|:--|
| Dummy Baseline Accuracy | 0.5000 |
| Best Trained Accuracy | 0.5000 (Logistic Regression — ties) |
| High class in training data | **0 — never observed** |
| Verdict | **INVALID for operational use** |

> No classifier outperformed the naive baseline. The "High" band (>75% attendance) was never present in the 18 collected lectures. Automated attendance-band decisions must not be generated from this model.

---

## 🖥️ Dashboard Validity

| Feature | Status |
|:--|:--|
| Streamlit server starts on port 8501 | ✅ Verified |
| `is_valid` flags read from joblib on startup | ✅ |
| Fallback warning shown when classifier is invalid | ✅ |
| Regression shown with "Exploratory / Limited Data" label | ✅ |
| Band prediction disabled when classifier `is_valid=False` | ✅ |
| Historical average (38.75%) shown as default baseline | ✅ |
| No confident High/Medium/Low band from invalid classifier | ✅ |
| Syntax validation (`py_compile`) | ✅ No errors |

---

## ⚠️ Confirmed Limitations

1. **n=18 total observations** — statistically insufficient for generalizable supervised learning.
2. **4-row test set** — no metric on 4 rows can be statistically significant.
3. **High class (>75%) never observed** — 3-class schema structurally unvalidatable with current data.
4. **Max attendance = 75%** — data never exceeds Medium/High boundary.
5. **MAPE = 43%** — best regression model deviates by 43% on average.
6. **R² = 0.12** — model explains only ~12% of test-set variance.
7. **4 of 5 regressors worse than baseline** — most ML models overfit on 14 training rows.
8. **All classifiers at or below baseline** — no learned decision boundary generalizes.

---

## 📋 Recommended Next Step

Physically verify and log additional lecture attendance records from subsequent months.  
Each new batch of records should be added to `data/raw/raw_lecture_attendance.csv` and the pipeline re-executed:

```powershell
python classroom-attendance-schedule-project/src/run_pipeline.py
```

The `is_valid` flags in the serialized model packages will automatically upgrade from `False` to `True` when a trained model first outperforms the dummy baseline on a meaningfully sized test set.
