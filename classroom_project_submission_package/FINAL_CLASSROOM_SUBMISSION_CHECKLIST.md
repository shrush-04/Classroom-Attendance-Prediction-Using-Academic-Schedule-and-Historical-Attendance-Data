# FINAL CLASSROOM SUBMISSION CHECKLIST
**Project:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data  
**Date:** 2026-08-30  
**Status:** ✅ READY FOR SUBMISSION (with documented limitations)

---

## Part 1 — File Verification

### Required Files — All Present ✅

| File | Size | Rows | Status |
|:--|--:|--:|:--|
| `data/raw/raw_lecture_attendance.csv` | 4,020 b | 18 | ✅ |
| `data/processed/cleaned_lecture_attendance.csv` | 3,552 b | 18 | ✅ |
| `data/processed/feature_engineered_attendance.csv` | 4,776 b | 18 | ✅ |
| `outputs/data_quality_report.md` | 1,585 b | — | ✅ |
| `outputs/eda_summary.md` | 2,680 b | — | ✅ |
| `outputs/experiment_results/regression_results.csv` | 540 b | 5 models | ✅ |
| `outputs/experiment_results/classification_results.csv` | 771 b | 6 models | ✅ |
| `outputs/experiment_results/experiment_table.md` | 6,062 b | — | ✅ |
| `outputs/pipeline_run_report.md` | 4,579 b | — | ✅ |
| `models/best_present_count_model.joblib` | 65,939 b | — | ✅ |
| `models/best_attendance_band_model.joblib` | 9,069 b | — | ✅ |
| `app/streamlit_app.py` | 28,303 b | — | ✅ |
| `report/project_report.md` | 8,692 b | — | ✅ |
| `presentation/presentation_content.md` | 8,822 b | — | ✅ |
| `PROJECT_STATUS.md` | 4,037 b | — | ✅ |
| `FINAL_CLASSROOM_PROJECT_AUDIT.md` | 5,925 b | — | ✅ |
| `README.md` | 4,739 b | — | ✅ |
| `requirements.txt` | 160 b | — | ✅ |

### Charts Generated ✅

| Chart | File |
|:--|:--|
| Subject-wise attendance boxplot | `outputs/charts/subject_wise_attendance.png` |
| Day-wise attendance bar chart | `outputs/charts/day_wise_attendance.png` |
| Attendance distribution | `outputs/charts/attendance_percentage_distribution.png` |
| Regression actual vs predicted | `outputs/charts/regression_actual_vs_predicted.png` |
| Classification confusion matrix | `outputs/charts/classification_confusion_matrix.png` |
| Correlation heatmap | `outputs/charts/correlation_heatmap.png` |
| Practical vs Theory | `outputs/charts/practical_vs_theory_attendance.png` |
| Holiday proximity | `outputs/charts/holiday_proximity_attendance.png` |

---

## Part 2 — Actual Metrics (From Pipeline Run — Not Invented)

### Dataset
| Property | Value |
|:--|:--|
| Total valid lectures | **18** |
| Training observations | **14** (2026-06-25 → 2026-08-01) |
| Test observations | **4** (2026-08-03 → 2026-08-07) |
| Class strength | **80 enrolled students** |
| Mean attendance | **38.75%** (~31 students per lecture) |
| Min attendance | 10.0% (8 students) |
| Max attendance | 75.0% (60 students) |
| High band (>75%) observed | **0 — never occurred** |

### Regression Results (Target: Students_Present)
| Model | MAE | RMSE | MAPE | R² |
|:--|--:|--:|--:|--:|
| Dummy Regressor (Mean Baseline) | **14.5000** | 17.1092 | 49.28% | −0.13 |
| Linear Regression | 37.2796 | 42.4341 | 140.35% | −5.95 |
| Decision Tree | 22.2000 | 23.6587 | 67.46% | −1.16 |
| **Random Forest** | **14.0192** | **15.1268** | **43.05%** | **0.1174** |
| Gradient Boosting | 22.4673 | 27.2761 | 53.31% | −1.87 |

- `is_valid = True` | Improvement over baseline: 0.48 MAE on **4 test rows** | **EXPLORATORY ONLY**

### Classification Results (Target: Attendance_Band)
| Model | Accuracy | Weighted F1 |
|:--|--:|--:|
| Dummy Classifier (Most Frequent) | **0.5000** | 0.3333 |
| Logistic Regression | 0.5000 | 0.3333 |
| Decision Tree | 0.5000 | 0.3333 |
| Random Forest | 0.2500 | 0.2000 |
| SVM | 0.5000 | 0.5000 |
| k-NN | 0.5000 | 0.5000 |

- `is_valid = False` | Best classifier ties dummy | **INVALID for operational use**

---

## Part 3 — Data Leakage Verification ✅

| Column | In Features? | Status |
|:--|:--|:--|
| `Students_Present` (current target) | No | ✅ SAFE |
| `Attendance_Percentage` (current target) | No | ✅ SAFE |
| `Lecture_ID` (identifier) | No | ✅ SAFE |
| `Total_Enrolled_Students` (capacity) | No | ✅ SAFE |
| All lag/rolling features | Shifted by 1+ rows | ✅ SAFE |
| Train/test split | Chronological 80/20 | ✅ SAFE |

**29 features used** — all are schedule metadata, holiday flags, and lagged historical aggregates.

---

## Part 4 — Scientific Validity Rules ✅

| Rule | Status |
|:--|:--|
| 1. Regression described as exploratory only | ✅ |
| 2. Regression NOT described as production-ready | ✅ |
| 3. States marginal beat on 4-row test set | ✅ |
| 4. States classification did not beat baseline | ✅ |
| 5. Classification marked not reliable for operational decisions | ✅ |
| 6. Historical-average fallback used in dashboard (38.75%) | ✅ |
| 7. No confident classification recommendations shown | ✅ |
| 8. States more verified lecture records are required | ✅ |
| 9. Correct bands: Low <50%, Medium 50–75%, High >75% | ✅ |
| 10. No synthetic student-level data used | ✅ |

---

## Part 5 — Privacy & PII Compliance ✅

| Check | Status |
|:--|:--|
| No student names in any file | ✅ |
| No roll numbers in any file | ✅ |
| No email IDs in any file | ✅ |
| No private_original_data/ in package | ✅ |
| No faculty_map.csv in package | ✅ |
| Faculty IDs are anonymous codes (F_01, F_02) | ✅ |
| All predictions at aggregate lecture level | ✅ |
| Dashboard form requests no personal information | ✅ |

---

## Part 6 — Dashboard Verification ✅

| Check | Status |
|:--|:--|
| App syntax: `py_compile` | ✅ No errors |
| Server starts on port 8501 | ✅ Confirmed |
| Dataset size of 18 visible on Tab 2 | ✅ |
| "Insufficient validated history..." notice shown | ✅ |
| "Regression results are exploratory..." shown | ✅ |
| "Classification is not recommended..." shown | ✅ |
| Exploratory / Limited Data warning (amber) | ✅ |
| Attendance Band Prediction Unavailable (red) | ✅ |
| Historical average baseline (38.75%) shown | ✅ |
| No confident Low/Medium/High from invalid classifier | ✅ |
| No traceback or runtime errors | ✅ |

---

## Part 7 — Submission Package ✅

**Package directory:** `classroom_project_submission_package/`

### Included
- `data/raw/raw_lecture_attendance.csv` ✅
- `data/processed/cleaned_lecture_attendance.csv` ✅
- `data/processed/feature_engineered_attendance.csv` ✅
- `data/templates/` (schema and format files) ✅
- `notebooks/` (6 Jupyter notebooks) ✅
- `src/` (7 pipeline scripts) ✅
- `models/` (2 joblib packages with is_valid metadata) ✅
- `outputs/` (reports, charts, experiment results) ✅
- `app/streamlit_app.py` ✅
- `report/project_report.md` ✅
- `presentation/presentation_content.md` ✅
- `docs/` (protocol, ethics, logbook template) ✅
- `README.md` ✅
- `requirements.txt` ✅

### Excluded (Confirmed Absent)
- `private_original_data/` — ✅ not in package
- `faculty_map.csv` — ✅ not in package
- Student names — ✅ none anywhere
- Roll numbers — ✅ none anywhere
- College email IDs — ✅ none anywhere
- Synthetic student-level dataset — ✅ not present

---

## Part 8 — Known Limitations (Mandatory Disclosure)

1. **n=18 observations** — statistically insufficient for supervised ML generalization
2. **4-row test set** — no metric on 4 rows is statistically significant
3. **High attendance band (>75%) never observed** — max was 75.0%; 3-class schema unvalidatable
4. **MAPE = 43%** — best regression model has 43% average relative error
5. **R² = 0.12** — model explains only ~12% of test-set variance
6. **4 of 5 regressors worse than baseline** — most ML models overfit on 14 training rows
7. **All classifiers at or below baseline** — no learned pattern generalizes to unseen data
8. **Cold-start lags** — first week of semester has no prior attendance to reference

---

## Part 9 — Commands

### Run the full pipeline
```powershell
cd d:\Data_Science_attendence_project
python classroom-attendance-schedule-project/src/run_pipeline.py
```

### Launch the dashboard
```powershell
python -m streamlit run classroom-attendance-schedule-project/app/streamlit_app.py
```

### Install all dependencies
```powershell
pip install -r classroom-attendance-schedule-project/requirements.txt
pip install tabulate
```
