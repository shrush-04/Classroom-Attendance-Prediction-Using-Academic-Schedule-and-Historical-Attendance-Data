# Final Project Summary
## Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System

> **All student records in this project are 100% synthetic and computer-generated.**
> No real student names, roll numbers, email IDs, or personally identifiable information are used at any stage.

**Department:** Computer Engineering & MCA (Extended Dataset)  
**Semester:** Fifth Semester (CE) | Third Semester (MCA)  
**Generated:** 2026-08-29

---

## Terminology Mapping

| Term Used in This Project | Equivalent Term (Seen in PROJECT_PLAN.md) | Definition |
|--------------------------|-------------------------------------------|------------|
| **Regular** | Safe | Attendance_Percentage >= 75% |
| **Defaulter** | At Risk | Attendance_Percentage < 75% |

> Note: PROJECT_PLAN.md drafted terms "Safe" and "At Risk". All data files, scripts, validation reports, and model outputs consistently use **Regular** and **Defaulter**.

---

## Dataset Summary

| Property | Value |
|----------|-------|
| File | `data/student_attendance_205_students.csv` |
| Total Rows | 4,100 |
| Total Columns | 21 |
| Unique Students | 205 (STU0001 – STU0205) |
| Unique Subjects | 5 |
| Missing Values | 0 |
| Duplicate Rows | 0 |
| Regular Records | 1,834 (44.73%) |
| Defaulter Records | 2,266 (55.27%) |
| Validation Status | PASSED — 25/25 checks passed |

### Subjects
1. Computer Networks
2. Data Structures & Algorithms
3. Database Management Systems
4. Software Engineering
5. Theory of Computation

### Attendance Statistics
| Statistic | Value |
|-----------|-------|
| Mean | 68.67% |
| Median | 70.00% |
| Std Dev | (see EDA charts) |
| Min | 0.00% |
| Max | 100.00% |

---

## EDA Key Findings

1. **55.27%** of records are Defaulter (Attendance < 75%)
2. Subject-level variation is minimal (< 1% across all 5 subjects)
3. Computer Engineering mean attendance (70.89%) > MCA mean attendance (67.75%)
4. Third Year (Fifth Semester) mean attendance (70.89%) > Final Year (Third Semester) (67.75%)

### Top Feature Correlations with Attendance_Percentage

| Feature | Pearson Correlation |
|---------|---------------------|
| Classes_Attended | 0.90 (mathematical relation — excluded from model) |
| Previous_Attendance_Percentage | 0.72 |
| Internal_Marks | 0.67 |
| Study_Hours_Per_Week | 0.61 |
| Previous_Exam_Score | 0.59 |
| Assignment_Score | 0.37 |
| Travel_Distance_KM | 0.04 |
| Late_Count | 0.01 |
| Medical_Leave_Days | -0.02 |
| Age | -0.07 |

---

## Regression Model Results (Actual — from outputs/regression_model_results.csv)

> Target: Predict `Attendance_Percentage` (continuous)
> Features: 15 predictors (Classes_Attended and Total_Classes excluded to prevent leakage)
> Split: 80/20 train-test, random_state=42

| Model | MAE | MSE | RMSE | R² |
|-------|-----|-----|------|----|
| LinearRegression | 9.3679 | 134.8109 | 11.6108 | 0.6755 |
| DecisionTreeRegressor | 10.2138 | 164.6423 | 12.8313 | 0.6037 |
| RandomForestRegressor | 9.1673 | 130.7760 | 11.4357 | 0.6852 |
| **GradientBoostingRegressor** | **9.1786** | **129.8510** | **11.3952** | **0.6874** |

**Best Regression Model: GradientBoostingRegressor**
- Selection criterion: Lowest RMSE
- RMSE: 11.3952 | R²: 0.6874
- Saved to: `models/best_regression_model.joblib`

---

## Classification Model Results (Actual — from outputs/classification_model_results.csv)

> Target: Predict `Attendance_Status` (Regular / Defaulter)
> Features: Same 15 predictors; Regular=0, Defaulter=1
> Split: 80/20 stratified, random_state=42

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| LogisticRegression | 0.8390 | 0.8512 | 0.8587 | 0.8549 | 0.9246 |
| DecisionTreeClassifier | 0.8268 | 0.8659 | 0.8124 | 0.8383 | 0.8841 |
| RandomForestClassifier | 0.8451 | 0.8655 | 0.8521 | 0.8587 | 0.9276 |
| **GradientBoostingClassifier** | **0.8463** | **0.8625** | **0.8587** | **0.8606** | 0.9189 |

**Best Classification Model: GradientBoostingClassifier**
- Selection criterion: Highest F1-score, then Recall (early-warning system priority)
- Accuracy: 84.63% | F1-Score: 0.8606 | ROC-AUC: 0.9189
- Saved to: `models/best_classification_model.joblib`

---

## Charts Generated (outputs/charts/)

| File | Description |
|------|-------------|
| `attendance_distribution.png` | KDE histogram of overall attendance with 75% threshold line |
| `regular_defaulter_count.png` | Bar chart: Regular (1,834) vs Defaulter (2,266) counts |
| `subject_wise_attendance.png` | Boxplot: attendance distribution across all 5 subjects |
| `attendance_by_period.png` | Boxplot: attendance across Period_1 to Period_4 |
| `study_hours_vs_attendance.png` | Scatter: Study_Hours_Per_Week vs Attendance_Percentage |
| `internal_marks_vs_attendance.png` | Scatter: Internal_Marks vs Attendance_Percentage |
| `medical_leave_vs_attendance.png` | Boxplot: Medical_Leave_Days vs Attendance_Percentage |
| `late_count_vs_attendance.png` | Scatter: Late_Count vs Attendance_Percentage (no correlation) |
| `correlation_heatmap.png` | Pearson correlation heatmap (all numeric features) |
| `regression_actual_vs_predicted.png` | Actual vs Predicted scatter for best regression model |
| `best_classifier_confusion_matrix.png` | Confusion matrix for best classification model |

---

## Ethical Considerations

- Zero real student data used at any stage
- Anonymous IDs (STU0001–STU0205) with no mapping to real students
- Every output clearly labeled SYNTHETIC
- `private_original_data/` folder never accessed by any project script
- Defaulter label used for academic analysis only — not for real-world judgment

## Limitations

1. Synthetic data — results may not reflect real-world dynamics
2. No causal analysis — correlations only
3. No temporal component — attendance recorded as period totals, not time series
4. No external factors modeled (health, socioeconomic status, etc.)
5. Model trained on synthetic data cannot be deployed directly on real data

## Project Status

| Phase | Status |
|-------|--------|
| Phase 0 — Setup | Complete |
| Phase 1 — Data Generation | Complete |
| Phase 2 — EDA | Complete |
| Phase 3 — Regression | Complete |
| Phase 4 — Classification | Complete |
| Phase 5 — Summary Report | Complete |
| Phase 6 — Final Checks | Pending (Manual) |

---
*Last updated: 2026-08-29*  
*Source: actual project output files — no values were invented*
