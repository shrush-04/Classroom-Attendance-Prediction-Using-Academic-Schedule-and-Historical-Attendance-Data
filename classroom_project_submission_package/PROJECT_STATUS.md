# PROJECT STATUS

**Last Updated:** 2026-08-30  
**Overall Status:** ✅ Pipeline Complete — Scientific Validity Review Applied

---

## Scientific Validity Statement

> **The available dataset contained only 18 valid lecture observations. The regression experiment
> produced a small improvement over the historical-average baseline, but the test set contained
> only four observations, so the result is exploratory and cannot establish reliable
> generalization. The classification model did not outperform the dummy baseline and should not
> be used for operational decisions. More physically verified lecture records are required before
> deploying a reliable predictive system.**

---

## Completed Milestones

| # | Milestone | Status |
|:--|:--|:--|
| 1 | Source data inspection & provenance analysis | ✅ |
| 2 | Class strength confirmed: **80 students** | ✅ |
| 3 | Canonical raw dataset built (`data/raw/raw_lecture_attendance.csv`, 18 rows) | ✅ |
| 4 | Stray record excluded & logged (`outputs/excluded_records_log.csv`) | ✅ |
| 5 | Data alignment report (`outputs/data_alignment_report.md`) | ✅ |
| 6 | Validation script patched (Faculty_ID regex, PII false-positive, Holiday NaN) | ✅ |
| 7 | All 16 validation checks passed (`outputs/data_quality_report.md`) | ✅ |
| 8 | Data cleaned → `data/processed/cleaned_lecture_attendance.csv` | ✅ |
| 9 | Feature engineering → `data/processed/feature_engineered_attendance.csv` (29 features) | ✅ |
| 10 | EDA charts + summary (`outputs/charts/`, `outputs/eda_summary.md`) | ✅ |
| 11 | Model training with Dummy baselines + chronological split (14 train / 4 test) | ✅ |
| 12 | Experiment results (`outputs/experiment_results/`) | ✅ |
| 13 | Models serialized with `is_valid` metadata | ✅ |
| 14 | Streamlit app updated with fallback warnings and validity checks | ✅ |
| 15 | Streamlit server verified running at `http://localhost:8501` | ✅ |
| 16 | **Scientific validity review applied to all output documents** | ✅ |
| 17 | Final audit report (`FINAL_CLASSROOM_PROJECT_AUDIT.md`) | ✅ |
| 18 | Generated college report (`report/project_report.pdf` - 31 pages) | ✅ |
| 19 | Generated presentation slides (`presentation/project_presentation.pptx` - 13 slides) | ✅ |

---

## Actual Model Performance (from Pipeline Run)

### Dataset
| Property | Value |
|:--|:--|
| Total lectures | 18 |
| Training rows | 14 |
| Test rows | 4 |
| Mean attendance | 38.75% |
| Mean students present | 31.0 / 80 |
| High band (>75%) observed | **Never — 0 out of 18** |

### Regression (Target: Students_Present)
| | Value |
|:--|:--|
| Dummy Baseline MAE | 14.5000 |
| Random Forest MAE | 14.0192 |
| Random Forest RMSE | 15.1268 |
| Random Forest R² | 0.1174 |
| Random Forest MAPE | 43.05% |
| `is_valid` | `True` — **Exploratory only, not production-ready** |

### Classification (Target: Attendance_Band)
| | Value |
|:--|:--|
| Dummy Baseline Accuracy | 0.5000 |
| Best Trained Accuracy | 0.5000 (ties dummy) |
| Weighted F1 | 0.3333 |
| High class in training | 0 — never observed |
| `is_valid` | `False` — **Invalid for operational use** |

---

## Practical Fallback (Current Default)

| Output | Value | Source |
|:--|:--|:--|
| Predicted attendance | **38.75%** | Historical mean of all 18 lectures |
| Predicted students present | **~31 out of 80** | Historical mean |
| Attendance band | **Not predicted** (classifier invalid) | — |

---

## Commands

### Re-Run the Pipeline
```powershell
cd d:\Data_Science_attendence_project
python classroom-attendance-schedule-project/src/run_pipeline.py
```

### Launch the Dashboard
```powershell
cd d:\Data_Science_attendence_project
python -m streamlit run classroom-attendance-schedule-project/app/streamlit_app.py
```

---

## Permanent Data Rules
- ❌ Do not generate fake/synthetic attendance rows
- ❌ Do not display student names, roll numbers, or emails
- ❌ Do not include `private_original_data/` in any output
- ❌ Do not invent metrics or claim model reliability beyond what experiments confirm
- ✅ Class strength: **80 students** (confirmed)
- ✅ All source files remain read-only inputs
- ✅ Historical mean baseline (38.75%) is the operational fallback
