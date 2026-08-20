# Project Status — Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System

> All student data in this project is 100% synthetic.
> No real student records, names, roll numbers, or identifiers are used at any point.

**Department:** Computer Engineering (original) + MCA (extended)
**Last Updated:** 2026-08-20

---

## Phase 0: Project Setup

| # | Task | Status |
|---|------|--------|
| 0.1 | Create project folder structure | Completed |
| 0.2 | Write PROJECT_PLAN.md | Completed |
| 0.3 | Write PROJECT_STATUS.md | Completed |
| 0.4 | Install required Python libraries | Completed (Python 3.13.7, pandas 2.3.3, numpy 2.3.3, openpyxl 3.1.5) |
| 0.5 | Verify Jupyter Notebook launches correctly | Not Started |

---

## Phase 1: Synthetic Data Generation

| # | Task | Status |
|---|------|--------|
| 1.1 | Write src/generate_dataset.py (60 students, STU0001-STU0060) | Completed |
| 1.2 | Write src/validate_dataset.py (16 checks, all PASS) | Completed |
| 1.3 | Generate data/student_attendance.csv (1200 rows, 20 columns) | Completed |
| 1.4 | Generate data/student_attendance.xlsx | Completed |
| 1.5 | Write data/DATASET_DICTIONARY.md | Completed |
| 1.6 | Write data/SYNTHETIC_DATA_NOTICE.md | Completed |
| 1.7 | Run validation on 60-student dataset — 16 checks, all PASS | Completed |
| 1.8 | Save outputs/dataset_validation_report.txt | Completed |
| 1.9 | Write src/extend_dataset_to_205.py | Completed |
| 1.10 | Extend dataset to 205 students (STU0061-STU0205, +2900 rows) | Completed |
| 1.11 | Generate data/student_attendance_205_students.csv (4100 rows, 21 columns) | Completed |
| 1.12 | Generate data/student_attendance_205_students.xlsx | Completed |
| 1.13 | Run validation on 205-student dataset — 17 checks, all PASS | Completed |
| 1.14 | Save outputs/dataset_validation_report_205_students.txt | Completed |
| 1.15 | Update data/SYNTHETIC_DATA_NOTICE.md | Completed |
| 1.16 | [MANUAL] Review CSV to verify data looks realistic and no real info is present | Not Started |

---

## Phase 2: Exploratory Data Analysis (EDA)

| # | Task | Status |
|---|------|--------|
| 2.1 | Write src/eda_utils.py (reusable plotting helpers) | Not Started |
| 2.2 | Write notebooks/02_eda.ipynb | Not Started |
| 2.3 | Plot attendance distribution histogram (KDE) | Not Started |
| 2.4 | Plot subject-wise boxplots | Not Started |
| 2.5 | Plot correlation heatmap | Not Started |
| 2.6 | Plot risk label distribution (pie/count plot) | Not Started |
| 2.7 | Outlier analysis | Not Started |
| 2.8 | Violin/scatter plots segmented by Attendance_Status | Not Started |
| 2.9 | Save all charts to outputs/charts/ | Not Started |

---

## Phase 3: Regression Modelling

| # | Task | Status |
|---|------|--------|
| 3.1 | Write src/model_utils.py (train/evaluate helpers) | Not Started |
| 3.2 | Write notebooks/03_regression.ipynb | Not Started |
| 3.3 | Train Linear Regression (baseline) | Not Started |
| 3.4 | Train Ridge / Lasso Regression | Not Started |
| 3.5 | Train Random Forest Regressor | Not Started |
| 3.6 | Evaluate models (MAE, RMSE, R-squared) | Not Started |
| 3.7 | Plot regression results chart | Not Started |
| 3.8 | [MANUAL] Select best regression model | Not Started |
| 3.9 | Save best model to models/regression_model.pkl | Not Started |

---

## Phase 4: Classification Modelling

| # | Task | Status |
|---|------|--------|
| 4.1 | Write notebooks/04_classification.ipynb | Not Started |
| 4.2 | Train Logistic Regression (baseline) | Not Started |
| 4.3 | Train Decision Tree Classifier | Not Started |
| 4.4 | Train Random Forest Classifier | Not Started |
| 4.5 | Evaluate models (Accuracy, Precision, Recall, F1, AUC) | Not Started |
| 4.6 | Plot Confusion Matrix | Not Started |
| 4.7 | Plot ROC Curve | Not Started |
| 4.8 | [MANUAL] Select best classification model | Not Started |
| 4.9 | Save best model to models/classification_model.pkl | Not Started |

---

## Phase 5: Summary and Report

| # | Task | Status |
|---|------|--------|
| 5.1 | Write notebooks/05_summary_report.ipynb | Not Started |
| 5.2 | [MANUAL] Write project_report.pdf | Not Started |
| 5.3 | [MANUAL] Create project_presentation.pptx | Not Started |

---

## Phase 6: Final Privacy and Submission Checks

| # | Task | Status |
|---|------|--------|
| 6.1 | [MANUAL] Verify no real student data in data/ or outputs/ | Not Started |
| 6.2 | [MANUAL] Confirm private_original_data/ excluded from submission zip | Not Started |
| 6.3 | [MANUAL] Verify all SYNTHETIC labels present in files and notebooks | Not Started |
| 6.4 | [MANUAL] Final review of PROJECT_PLAN.md and PROJECT_STATUS.md | Not Started |

---

## Dataset Registry

| File | Students | Rows | Columns | Seed | Status |
|------|----------|------|---------|------|--------|
| student_attendance.csv | 60 (STU0001-STU0060) | 1,200 | 20 | 42 | Completed |
| student_attendance.xlsx | 60 | 1,200 | 20 | 42 | Completed |
| student_attendance_205_students.csv | 205 (STU0001-STU0205) | 4,100 | 21 | 42+200 | Completed |
| student_attendance_205_students.xlsx | 205 | 4,100 | 21 | 42+200 | Completed |

---
*Last updated: 2026-08-20*
*Project: Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System*
