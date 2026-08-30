# Academic Project Report

**Project Title:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data  
**Department:** Computer Applications (MCA)  
**Academic Year:** Final Year  
**Semester:** Third Semester  

---

## 1. Executive Summary
This project outlines a privacy-preserving machine learning pipeline designed to predict lecture-level classroom attendance. By abstracting analysis to the lecture-slot level, the system uses timetable schedules, exam calendars, and historical lag variables to forecast student counts and attendance categories. All predictions are generated from aggregate headcounts — no student names, roll numbers, or email addresses are stored or processed at any point.

> **Scientific Status Note:** The current dataset contains 18 validated lecture observations. All modelling results are exploratory. The system falls back to the historical average baseline for any operational output until a larger verified dataset is collected.

---

## 2. Problem Statement & Objectives

### 2.1 Problem Statement
Traditional attendance systems focus on individual student records, which present compliance risks (exposure of names, emails, rolls). Schedulers also have no proactive tools to determine when class slots will see high absenteeism. There is a need for a prediction system that operates purely on aggregate, schedule-based parameters without storing individual student identifiers.

### 2.2 Objectives
- Build a dataset architecture using only aggregate, lecture-level statistics.
- Construct administrative protocols to extract and compile attendance data securely.
- Code a complete pipeline to validate, clean, engineer lag features, and train models.
- Apply chronological test splits to accurately simulate real-world forecasting conditions.
- Design an interactive dashboard for schedulers, with honest model validity indicators.

---

## 3. Data Collection Methodology

### 3.1 Data Sources
The raw data is compiled by department representatives using only aggregate session metrics:
- **Master Timetable:** Slot numbers, classrooms, subject codes, and section details.
- **Faculty Registers:** Physical registers checked in-class to sum the number of present students.
- **Academic Calendar:** Used to flag public holidays and proximity windows.
- **Continuous Evaluation Schedule:** Identifies internal test weeks.

### 3.2 Privacy by Design Safeguards
- **Zero Student PII:** Student names, roll numbers, and emails are completely excluded.
- **Instructor Anonymization:** Faculty names are replaced with codes (e.g. `F_01`, `F_02`).
- **No Mapping Tables:** No internal database maps individual identifiers to records.

---

## 4. Preprocessing & Feature Engineering

### 4.1 Data Cleaning & Standardizing
Validation enforces 16 rules including schema checks, capacity constraints (`Students_Present ≤ Total_Enrolled_Students`), date/time format verification, and PII absence checks. Cleaning standardizes text case, formats dates, and logs optional missing values as `Not_Collected`.

### 4.2 Leakage-Free Feature Generation
Features are derived strictly chronologically to prevent target leakage:
- **Lag Features:** Previous attendance rate and gap hours are shifted by one row.
- **Rolling Features:** Moving averages of the previous 3 lectures exclude the current row.
- **Historical Averages:** Expanding subject means use only preceding sessions.

---

## 5. Exploratory Data Analysis (EDA)

The pipeline was executed on 18 validated lectures from the period 2026-06-25 to 2026-08-07.

| Statistic | Value |
|:--|:--|
| Total valid lectures | 18 |
| Minimum attendance | 10.0% (8 students) |
| Maximum attendance | 75.0% (60 students) |
| Mean attendance | 38.75% (31 students) |
| Subjects | Mobile Application Development (Theory), MAD Practical |
| Class strength | 80 enrolled |

**Attendance Band Distribution (all 18 lectures):**

| Band | Threshold | Count |
|:--|:--|:--|
| Low | < 50% | 12 |
| Medium | 50% – 75% | 6 |
| High | > 75% | **0** |

> ⚠️ The "High" attendance band was **never observed** in the collected data. The maximum recorded attendance was exactly 75.0%, which falls at the boundary of Medium. Any system claiming to predict "High" attendance would be extrapolating beyond the observed data range.

---

## 6. Model Training & Experiments

### 6.1 Evaluation Partitioning
A strict **chronological split** was applied: the first 80% of lectures (n=14, 2026-06-25 to 2026-08-01) form the training set and the last 20% (n=4, 2026-08-03 to 2026-08-07) form the test set.

> ⚠️ **Critical Limitation:** With only 4 test observations, all computed metrics are inherently unreliable. No metric on a 4-row test set constitutes statistically significant evidence of generalization.

### 6.2 Regression Results (Target: Students_Present)

Dummy baseline: **MAE = 14.50** (predicting the training mean of 31 students for every lecture).

| Model | MAE | RMSE | MAPE | R² |
|:--|--:|--:|--:|--:|
| Dummy Regressor (Mean Baseline) | 14.50 | 17.11 | 49.28% | −0.13 |
| Linear Regression | 37.28 | 42.43 | 140.35% | −5.95 |
| Decision Tree | 22.20 | 23.66 | 67.46% | −1.16 |
| **Random Forest** | **14.02** | **15.13** | **43.05%** | **0.12** |
| Gradient Boosting | 22.47 | 27.28 | 53.31% | −1.87 |

**Interpretation:** Random Forest marginally beat the dummy baseline by 0.48 MAE on a test set of only 4 rows. This result is **exploratory only** and is insufficient to establish reliable generalization. The R² of 0.12 indicates the model explains approximately 12% of variance in held-out data. The MAPE of 43% means predictions deviate by an average of 43% from true values. Four of five trained regression models perform worse than the naive mean-predictor.

### 6.3 Classification Results (Target: Attendance_Band)

Dummy baseline: **Accuracy = 0.50** (predicts "Low" — most frequent class — for every test row).

| Model | Accuracy | Weighted F1 |
|:--|--:|--:|
| Dummy Classifier | 0.50 | 0.33 |
| Logistic Regression | 0.50 | 0.33 |
| Decision Tree | 0.50 | 0.33 |
| Random Forest | **0.25** | 0.20 |
| SVM | 0.50 | 0.50 |
| k-NN | 0.50 | 0.50 |

**Interpretation:** No classification model outperformed the dummy baseline. Logistic Regression, the best trained classifier, exactly ties the baseline at 0.50 accuracy. The "High" attendance band was never observed in training or test data, making 3-class classification structurally impossible with the current data. The classification model is **invalid for operational attendance-band decisions**.

---

## 7. Streamlit Dashboard
An interactive dashboard is implemented in `app/streamlit_app.py`. It renders historical trends and provides a form for planners to enter future lecture slot details. The dashboard reads `is_valid` flags from serialized model packages and:
- Displays the **historical average baseline** (38.75%) as the primary output when the classifier is not valid.
- Shows any ML regression estimate with an explicit **"Exploratory / Limited Data"** warning label.
- Disables automated Low/Medium/High band decisions from the invalid classifier.

---

## 8. Limitations

1. **Insufficient data:** 18 lecture observations are statistically inadequate for supervised machine learning generalization.
2. **4-row test set:** No metric computed on 4 rows carries statistical significance.
3. **High class unobserved:** The "High" band (>75%) was never recorded. The 3-class schema cannot be validated with current data.
4. **Maximum attendance = 75%:** The data never exceeds the Medium/High boundary, indicating the semester was atypical or attendance was systematically low.
5. **Lag sensitivity:** Rolling and lag features become unreliable when class sessions are skipped or timetabled irregularly.
6. **First-week cold start:** Lag features default to the historical mean during the first week of a new semester.

---

## 9. Conclusion

The lecture-level attendance prediction pipeline was successfully implemented from raw attendance records through validation, cleaning, feature engineering, exploratory analysis, modeling, evaluation, and dashboard deployment. However, only 18 valid lecture observations were available. The Random Forest regression model marginally outperformed the historical-average baseline, but the test set contained only four observations, so the result is exploratory and cannot establish reliable generalization. The classification model did not outperform the dummy baseline and is not recommended for operational use. Additional physically verified lecture records are required before reliable deployment.

The system infrastructure — validation pipeline, feature engineering, model training, and dashboard — is fully implemented and ready to scale automatically as more lecture records are collected and added to `data/raw/raw_lecture_attendance.csv`.

