# Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System

**Final Project Report**

---

| | |
|---|---|
| **Department** | Computer Engineering & MCA |
| **Year / Semester** | Third Year — Fifth Semester (CE) · Final Year — Third Semester (MCA) |
| **Dataset** | Fully Synthetic — 205 Students, 4,100 Records |
| **Report Date** | August 2026 |
| **Project Status** | Phases 0–5 Complete |

---

> **⚠️ SYNTHETIC DATA NOTICE**
>
> This project uses a synthetic student attendance dataset created for academic demonstration.
> It does not contain real student names, roll numbers, email IDs, or actual attendance
> records of identifiable students. All records are computer-generated using statistical
> modeling. No real student information was collected, stored, or processed at any stage.

---

## Terminology Notice

Early draft documentation (PROJECT_PLAN.md) used the terms **"Safe"** and **"At Risk"**.
All data files, scripts, validation reports, model outputs, and this report use the following
consistent terminology:

| Term | Equivalent in Early Drafts | Definition |
|------|---------------------------|------------|
| **Regular** | Safe | Attendance_Percentage ≥ 75% |
| **Defaulter** | At Risk | Attendance_Percentage < 75% |

This mapping is documented once here and used consistently throughout this report.

---

## Table of Contents

1. Abstract
2. Introduction
3. Problem Statement
4. Objectives
5. Scope
6. Synthetic Dataset Description
7. Privacy and Ethical Approach
8. Dataset Columns
9. Data Preprocessing
10. Exploratory Data Analysis
11. Regression Methodology
12. Classification Methodology
13. Algorithms Used
14. Evaluation Metrics
15. Actual Regression Results
16. Actual Classification Results
17. Best Model Selection
18. Sample Prediction
19. Findings
20. Practical Applications
21. Limitations
22. Future Scope
23. Conclusion
24. References
25. Appendix

---

## 1. Abstract

This project presents a complete end-to-end data science pipeline for student attendance
analysis and prediction using a fully synthetic, privacy-preserving dataset. The dataset
comprises 4,100 records representing 205 anonymous students (STU0001–STU0205) across two
departments — Computer Engineering and MCA — over five subjects and four attendance periods
per subject. All student identifiers are synthetic; no real student data is involved at any
stage.

The project implements two machine learning tasks: (1) **Regression** — predicting a
student's continuous attendance percentage, and (2) **Classification** — predicting whether a
student is **Regular** (Attendance_Percentage ≥ 75%) or a **Defaulter** (Attendance_Percentage
< 75%).

After systematic model comparison, **GradientBoostingRegressor** achieved the best regression
performance (RMSE: 11.3952, R²: 0.6874) and **GradientBoostingClassifier** achieved the best
classification performance (F1-Score: 0.8606, ROC-AUC: 0.9189, Recall: 0.8587). The project
demonstrates responsible, ethical data science practices while delivering a working predictive
system suitable for academic portfolio and viva demonstration.

---

## 2. Introduction

Student attendance is widely recognized as a critical indicator of academic engagement and
performance outcomes. Educational institutions maintain attendance registers to enforce
minimum attendance requirements — typically set at 75% — below which students may be barred
from examinations or required to seek remedial intervention.

However, building data-driven attendance prediction models using actual student records raises
significant privacy and ethical concerns. Real attendance datasets contain personally
identifiable information (PII) such as student names, roll numbers, and institutional email
IDs. Handling such data requires explicit institutional consent, data governance compliance,
and careful anonymization — constraints that are difficult to fulfill in a student project
setting.

This project resolves that tension by working with a **fully synthetic dataset**. The
synthetic data was statistically modeled to mirror the realistic distributions and correlations
of a genuine classroom attendance dataset, without capturing any real student information.
Using this dataset, the project demonstrates that a complete, reproducible, and
publication-quality data science workflow can be executed ethically and responsibly.

The project covers data generation, validation, exploratory analysis, regression modeling,
classification modeling, and a final interpretive summary — making it a complete academic
data science project demonstrating modern ML practices.

---

## 3. Problem Statement

Student absenteeism is a persistent challenge in higher education. Students who fall below the
minimum required attendance threshold risk academic penalties, poor exam performance, and
increased dropout rates. Faculty and administration often identify attendance problems only
after significant deterioration has occurred, leaving limited time for corrective intervention.

The core problem is twofold:

1. **Prediction Problem (Regression):** Given a student's demographic profile, prior
   academic performance, and study habits, can we predict their likely attendance percentage
   for the current semester?

2. **Classification Problem (Early Warning):** Can we classify a student as **Regular**
   (Attendance ≥ 75%) or **Defaulter** (Attendance < 75%) early enough to trigger
   meaningful academic intervention?

A secondary challenge is doing this responsibly — without requiring access to real student PII
— by demonstrating that synthetic data can serve as a viable and ethically sound substitute
for model development and academic exploration.

---

## 4. Objectives

| # | Objective |
|---|-----------|
| 1 | Generate a fully synthetic, anonymous student attendance dataset that preserves realistic statistical properties |
| 2 | Validate the synthetic dataset against 25 data quality, integrity, and privacy checks |
| 3 | Perform comprehensive Exploratory Data Analysis (EDA) to uncover attendance patterns and feature correlations |
| 4 | Build and evaluate multiple **Regression models** to predict `Attendance_Percentage` (continuous) |
| 5 | Build and evaluate multiple **Classification models** to predict `Attendance_Status` (Regular / Defaulter) |
| 6 | Select the best model for each task using principled metric-based criteria |
| 7 | Save trained model pipelines for reusable deployment |
| 8 | Demonstrate responsible, ethical, and privacy-preserving data science practices throughout |

---

## 5. Scope

**In Scope:**
- Synthetic data generation, validation, and documentation
- Exploratory Data Analysis with 11 professional visualizations
- Regression modeling (4 algorithms, full pipeline with preprocessing)
- Classification modeling (4 algorithms, full pipeline with preprocessing)
- Model evaluation, comparison, and best-model selection
- Saved, deployable model pipelines
- Complete summary report and presentation

**Out of Scope:**
- Real student data of any kind
- Real-time deployment or integration with institutional LMS/ERP systems
- FERPA/institutional data governance compliance (not applicable to synthetic data)
- Causal inference or interventional studies
- Time-series attendance modeling (week-by-week trends)
- Multi-institution comparison

---

## 6. Synthetic Dataset Description

### 6.1 Generation Overview

The dataset was generated in two phases using NumPy random seeding for reproducibility:

- **Phase 1:** 60 students (STU0001–STU0060), Computer Engineering, Third Year,
  Fifth Semester — generated by `src/generate_dataset.py` (seed=42)
- **Phase 2 Extension:** 145 additional students (STU0061–STU0205), MCA, Final Year,
  Third Semester — added by `src/extend_dataset_to_205.py` (seed=42+200)

### 6.2 Final Dataset Parameters

| Parameter | Value |
|-----------|-------|
| File | `data/student_attendance_205_students.csv` |
| Total Rows | 4,100 |
| Total Columns | 21 |
| Unique Students | 205 (STU0001–STU0205) |
| Rows per Student | 20 (5 subjects × 4 attendance periods) |
| Unique Subjects | 5 |
| Departments | Computer Engineering (1,200 records), MCA (2,900 records) |
| Attendance Range | 0.00% – 100.00% |
| Mean Attendance | 68.67% |
| Median Attendance | 70.00% |
| Std Deviation | 20.21% |
| Regular Records | 1,834 (44.73%) |
| Defaulter Records | 2,266 (55.27%) |
| Missing Values | 0 |
| Duplicate Rows | 0 |

### 6.3 Generation Strategy

- Attendance values generated using a clipped normal distribution (mean ~75%, std ~15%)
- Subject-level mild correlation applied so students who attend one subject tend to attend others
- All values rounded and clipped to valid integer range [0, Total_Classes]
- Attendance_Percentage computed as (Classes_Attended / Total_Classes) × 100
- Attendance_Status assigned by rule: ≥75% → Regular; <75% → Defaulter
- Student IDs use the format STU0001–STU0205 — no real identifiers

### 6.4 Subjects

| Code | Subject Name |
|------|-------------|
| 1 | Computer Networks |
| 2 | Data Structures & Algorithms |
| 3 | Database Management Systems |
| 4 | Software Engineering |
| 5 | Theory of Computation |

### 6.5 Validation

The final dataset was validated by `src/validate_final_dataset.py`, which executed **25
independent checks** covering file existence, row/column counts, student ID integrity,
subject completeness, missing values, duplicates, attendance calculation accuracy,
status label correctness, numeric range validity, and absence of private data patterns.

**Result: 25/25 checks PASSED.**

Full report: `outputs/final_dataset_validation_report.txt`

---

## 7. Privacy and Ethical Approach

| Principle | Implementation |
|-----------|----------------|
| **Data Minimization** | Only statistical classroom parameters used; no personal data collected or stored |
| **Full Anonymization** | All students assigned synthetic IDs (STU0001–STU0205); no real names or roll numbers exist in any file |
| **No Re-identification Risk** | No mapping table between synthetic IDs and real students was ever created |
| **Synthetic Data Labeling** | Every output file, notebook, and report clearly labels data as SYNTHETIC |
| **Honest Framing** | All conclusions explicitly acknowledge the synthetic nature of the data |
| **Source Isolation** | The `private_original_data/` directory is physically present but never read, imported, or inspected by any project script |
| **No Discrimination** | The Defaulter label is used solely for academic analysis — never for real-world academic judgment |
| **Reproducibility** | Fixed random seeds (42) ensure anyone can reproduce the exact same dataset |

> **Important for Real-World Deployment:** Before applying any attendance prediction model
> to real student data, institutions must obtain informed consent, comply with applicable
> education data privacy regulations, and ensure human oversight before acting on
> model-generated flags.

---

## 8. Dataset Columns

| # | Column | Data Type | Description |
|---|--------|-----------|-------------|
| 1 | `Student_ID` | Categorical | Anonymous synthetic ID (STU0001–STU0205) |
| 2 | `Gender` | Categorical | Male / Female |
| 3 | `Age` | Numeric | Student age (integer) |
| 4 | `Department` | Categorical | Computer Engineering / MCA |
| 5 | `Year` | Categorical | Third Year / Final Year |
| 6 | `Semester` | Categorical | Fifth Semester / Third Semester |
| 7 | `Subject` | Categorical | One of the 5 subjects listed in Section 6.4 |
| 8 | `Attendance_Period` | Categorical | Period_1 / Period_2 / Period_3 / Period_4 |
| 9 | `Total_Classes` | Numeric | Total classes scheduled in that period (8–12) |
| 10 | `Classes_Attended` | Numeric | Classes the student actually attended (0–12) |
| 11 | `Previous_Attendance_Percentage` | Numeric | Student's prior semester attendance % |
| 12 | `Assignment_Score` | Numeric | Score on course assignments |
| 13 | `Internal_Marks` | Numeric | Internal/mid-term exam marks |
| 14 | `Study_Hours_Per_Week` | Numeric | Self-reported weekly study hours |
| 15 | `Medical_Leave_Days` | Numeric | Days of medical leave taken this semester |
| 16 | `Travel_Distance_KM` | Numeric | Distance between student's home and college |
| 17 | `Previous_Exam_Score` | Numeric | Score in the previous semester's final exam |
| 18 | `Late_Count` | Numeric | Number of late arrivals to class |
| 19 | `Online_Class_Attendance` | Numeric | Online/virtual session attendance percentage |
| 20 | `Attendance_Percentage` | Numeric | **Regression Target:** (Classes_Attended / Total_Classes) × 100 |
| 21 | `Attendance_Status` | Categorical | **Classification Target:** Regular (≥75%) / Defaulter (<75%) |

**Note:** `Classes_Attended` and `Total_Classes` (columns 9–10) are mathematically
related to `Attendance_Percentage` (column 20). These two columns were **excluded from
all model features** to prevent data leakage.

---

## 9. Data Preprocessing

Both the regression and classification pipelines use an identical preprocessing workflow
implemented as a `sklearn.pipeline.Pipeline` combined with a `ColumnTransformer`.

### 9.1 Feature Selection

**15 predictors used (no leakage features):**

*Categorical (5):* Gender, Department, Year, Semester, Subject

*Numeric (10):* Age, Previous_Attendance_Percentage, Assignment_Score, Internal_Marks,
Study_Hours_Per_Week, Medical_Leave_Days, Travel_Distance_KM, Previous_Exam_Score,
Late_Count, Online_Class_Attendance

**Excluded (data leakage):** Classes_Attended, Total_Classes, Attendance_Period, Student_ID

### 9.2 Preprocessing Steps

| Step | Categorical Features | Numeric Features |
|------|---------------------|-----------------|
| Imputation | `SimpleImputer(strategy='most_frequent')` | `SimpleImputer(strategy='median')` |
| Encoding / Scaling | `OneHotEncoder(handle_unknown='ignore')` | `StandardScaler()` |

### 9.3 Train-Test Split

| Parameter | Value |
|-----------|-------|
| Split ratio | 80% train / 20% test |
| Random state | 42 |
| Stratification | Applied for classification (preserves class ratios) |
| Training rows | ~3,280 |
| Test rows | ~820 |

---

## 10. Exploratory Data Analysis

EDA was performed in `notebooks/01_exploratory_data_analysis.ipynb` using
`src/exploratory_analysis.py`. Nine visualizations were generated and saved to
`outputs/charts/`.

### 10.1 Attendance Distribution

The overall attendance percentage follows a near-normal distribution with:
- Mean: **68.67%**, Median: **70.00%**, Std Dev: **20.21%**
- Distribution peaks between 70–80%
- A secondary concentration of zero-attendance records exists (students who missed entire periods)
- The 75% threshold divides the dataset into Regular (44.73%) and Defaulter (55.27%)

### 10.2 Regular vs. Defaulter Distribution

| Status | Count | Percentage |
|--------|-------|------------|
| Defaulter (Attendance < 75%) | 2,266 | 55.27% |
| Regular (Attendance ≥ 75%) | 1,834 | 44.73% |

The majority class is Defaulter. This slight imbalance was addressed in classification
by using stratified train-test split and prioritizing F1-score and Recall over raw accuracy.

### 10.3 Department-wise Analysis

| Department | Records | Mean Attendance | Median Attendance |
|------------|---------|----------------|------------------|
| Computer Engineering | 1,200 | 70.89% | 72.73% |
| MCA | 2,900 | 67.75% | 66.67% |

Computer Engineering students show slightly higher mean attendance. This is consistent
with the dataset generation parameters which used different base rates for the two cohorts.

### 10.4 Subject-wise Analysis

| Subject | Records | Mean Attendance | Median Attendance |
|---------|---------|----------------|------------------|
| Software Engineering | 820 | 69.12% | 70.00% |
| Computer Networks | 820 | 68.86% | 71.37% |
| Data Structures & Algorithms | 820 | 68.54% | 70.00% |
| Theory of Computation | 820 | 68.43% | 70.00% |
| Database Management Systems | 820 | 68.38% | 66.67% |

Subject-level variation is minimal (< 1%). Attendance behaviour is predominantly
student-level, not subject-driven.

### 10.5 Feature Correlation Analysis (Pearson)

| Feature | Correlation with Attendance_Percentage | Interpretation |
|---------|---------------------------------------|----------------|
| `Classes_Attended` | 0.90 | Mathematical relationship (excluded) |
| `Previous_Attendance_Percentage` | 0.72 | Strong Positive |
| `Internal_Marks` | 0.67 | Strong Positive |
| `Study_Hours_Per_Week` | 0.61 | Moderate-Strong Positive |
| `Previous_Exam_Score` | 0.59 | Moderate-Strong Positive |
| `Assignment_Score` | 0.37 | Moderate Positive |
| `Online_Class_Attendance` | −0.00 | No Correlation |
| `Travel_Distance_KM` | 0.04 | No Correlation |
| `Late_Count` | 0.01 | No Correlation |
| `Medical_Leave_Days` | −0.02 | No Correlation |
| `Age` | −0.07 | Negligible Negative |

**Key Insight:** Prior academic behavior (`Previous_Attendance_Percentage`,
`Internal_Marks`, `Previous_Exam_Score`) is the dominant predictor group.
Logistical and personal factors (travel distance, medical leave, late count)
show no meaningful correlation in this synthetic dataset.

### 10.6 Correlation vs. Causation

Statistical correlations observed in this dataset **do not imply causal relationships**.
A positive correlation of 0.67 between `Internal_Marks` and `Attendance_Percentage`
does not mean that higher attendance causes better marks — both could be driven by
underlying student motivation, diligence, or academic support systems. This is
especially important to note in a synthetic dataset where correlations are mathematically
encoded during generation, not observed from natural behavior.

### 10.7 Visualizations Generated

| File | Description |
|------|-------------|
| `attendance_distribution.png` | KDE histogram with 75% threshold line |
| `regular_defaulter_count.png` | Bar chart: Regular vs Defaulter counts |
| `subject_wise_attendance.png` | Boxplot per subject |
| `attendance_by_period.png` | Boxplot across Period_1 to Period_4 |
| `study_hours_vs_attendance.png` | Scatter: Study hours vs attendance |
| `internal_marks_vs_attendance.png` | Scatter: Internal marks vs attendance |
| `medical_leave_vs_attendance.png` | Boxplot: Medical leave vs attendance |
| `late_count_vs_attendance.png` | Scatter: Late count vs attendance |
| `correlation_heatmap.png` | Pearson correlation matrix heatmap |
| `regression_actual_vs_predicted.png` | Actual vs predicted (best regressor) |
| `best_classifier_confusion_matrix.png` | Confusion matrix (best classifier) |

---

## 11. Regression Methodology

### 11.1 Task Definition

- **Target variable:** `Attendance_Percentage` (continuous, range: 0–100)
- **Type:** Supervised Regression
- **Script:** `src/train_regression.py`
- **Notebook:** `notebooks/02_regression_model.ipynb`

### 11.2 Pipeline Architecture

```
Raw Data
    → ColumnTransformer
        ├── Numeric Branch: SimpleImputer(median) → StandardScaler
        └── Categorical Branch: SimpleImputer(most_frequent) → OneHotEncoder
    → Regressor Model
    → Predicted Attendance_Percentage
```

### 11.3 Models Trained

| Model | Key Hyperparameters |
|-------|---------------------|
| LinearRegression | Default |
| DecisionTreeRegressor | max_depth=8, random_state=42 |
| RandomForestRegressor | n_estimators=100, max_depth=12, random_state=42 |
| GradientBoostingRegressor | n_estimators=100, learning_rate=0.1, random_state=42 |

---

## 12. Classification Methodology

### 12.1 Task Definition

- **Target variable:** `Attendance_Status` (Regular=0, Defaulter=1)
- **Type:** Supervised Binary Classification
- **Script:** `src/train_classification.py`
- **Notebook:** `notebooks/03_classification_model.ipynb`

### 12.2 Target Encoding

| Label | Encoded Value |
|-------|--------------|
| Regular | 0 |
| Defaulter | 1 |

### 12.3 Pipeline Architecture

```
Raw Data
    → ColumnTransformer (same as Regression)
    → Classifier Model
    → Predicted Attendance_Status (Regular / Defaulter)
         + Predicted Probabilities (for ROC-AUC)
```

### 12.4 Models Trained

| Model | Key Hyperparameters |
|-------|---------------------|
| LogisticRegression | max_iter=1000, random_state=42 |
| DecisionTreeClassifier | max_depth=6, random_state=42 |
| RandomForestClassifier | n_estimators=100, max_depth=10, random_state=42 |
| GradientBoostingClassifier | n_estimators=100, learning_rate=0.1, random_state=42 |

---

## 13. Algorithms Used

### 13.1 Gradient Boosting (Both Best Models)

Gradient Boosting is an ensemble learning method that builds models sequentially.
Each new tree corrects the residual errors of all preceding trees:

```
F_m(x) = F_{m-1}(x) + η · h_m(x)
```

Where F_m(x) is the model at iteration m, η is the learning rate (0.1), and h_m(x)
is a decision tree fitted on the residuals of F_{m-1}(x).

**Why it performs well here:**
- Handles mixed categorical + numeric features effectively
- Captures non-linear relationships between attendance and predictors
- Sequential error correction reduces both bias and variance
- Less prone to overfitting than single deep trees

### 13.2 Random Forest

An ensemble of independently trained decision trees that vote (classification) or average
(regression) their predictions. Uses bootstrap sampling and random feature selection at
each split to reduce variance.

### 13.3 Decision Tree

A single recursive binary splitting tree. Interpretable but prone to overfitting on
complex datasets, hence typically outperformed by ensembles.

### 13.4 Linear / Logistic Regression

Linear Regression fits a hyperplane minimizing mean squared error.
Logistic Regression models class probability using the sigmoid function.
Both serve as interpretable baselines.

---

## 14. Evaluation Metrics

### 14.1 Regression Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **MAE** | mean(|y − ŷ|) | Average absolute error in attendance percentage points |
| **MSE** | mean((y − ŷ)²) | Mean squared error (penalizes large errors more) |
| **RMSE** | √MSE | Root MSE — same units as target (percentage points) |
| **R²** | 1 − SS_res/SS_tot | Proportion of variance explained (1.0 = perfect) |

**Primary selection criterion: Lowest RMSE + Highest R²**

### 14.2 Classification Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Accuracy** | (TP+TN)/(TP+TN+FP+FN) | Overall correct predictions |
| **Precision** | TP/(TP+FP) | Of predicted Defaulters, how many are actually Defaulters |
| **Recall** | TP/(TP+FN) | Of actual Defaulters, how many were correctly identified |
| **F1-Score** | 2·Prec·Rec/(Prec+Rec) | Harmonic mean of Precision and Recall |
| **ROC-AUC** | Area under ROC curve | Ability to discriminate Regular from Defaulter across all thresholds |

**Primary selection criterion: Highest F1-Score, then highest Recall**

Recall is prioritized in the secondary criterion because in an early-warning system,
a **False Negative** (failing to identify a Defaulter) is more costly than a
**False Positive** (incorrectly flagging a Regular student).

---

## 15. Actual Regression Results

*Source: `outputs/regression_model_results.csv` — values verified directly from file*

| Model | MAE | MSE | RMSE | R² |
|-------|-----|-----|------|----|
| LinearRegression | 9.3679 | 134.8109 | 11.6108 | 0.6755 |
| DecisionTreeRegressor | 10.2138 | 164.6423 | 12.8313 | 0.6037 |
| RandomForestRegressor | 9.1673 | 130.7760 | 11.4357 | 0.6852 |
| **GradientBoostingRegressor** | **9.1786** | **129.8510** | **11.3952** | **0.6874** |

**Full precision values (from CSV, unrounded):**

| Model | MAE (full) | MSE (full) | RMSE (full) | R² (full) |
|-------|------------|------------|-------------|-----------|
| LinearRegression | 9.367864124465022 | 134.8109039111988 | 11.610809787056146 | 0.6754938609166184 |
| DecisionTreeRegressor | 10.213813496653357 | 164.642279552681 | 12.831300773993298 | 0.6036861343002312 |
| RandomForestRegressor | 9.167304377304418 | 130.77602261653715 | 11.435734458990256 | 0.6852063078523121 |
| GradientBoostingRegressor | 9.178560849121798 | 129.8509839512371 | 11.395217591219446 | 0.6874329877207083 |

**Chart:** `outputs/charts/regression_actual_vs_predicted.png`

---

## 16. Actual Classification Results

*Source: `outputs/classification_model_results.csv` — values verified directly from file*

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| LogisticRegression | 0.8390 | 0.8512 | 0.8587 | 0.8549 | 0.9246 |
| DecisionTreeClassifier | 0.8268 | 0.8659 | 0.8124 | 0.8383 | 0.8841 |
| RandomForestClassifier | 0.8451 | 0.8655 | 0.8521 | 0.8587 | 0.9276 |
| **GradientBoostingClassifier** | **0.8463** | **0.8625** | **0.8587** | **0.8606** | 0.9189 |

**Full precision values (from CSV, unrounded):**

| Model | Accuracy (full) | Precision (full) | Recall (full) | F1-Score (full) | ROC-AUC (full) |
|-------|-----------------|-----------------|---------------|-----------------|----------------|
| LogisticRegression | 0.8390243902439024 | 0.8512035010940919 | 0.8587196467991169 | 0.8549450549450549 | 0.9245778972758059 |
| DecisionTreeClassifier | 0.8268292682926829 | 0.8658823529411764 | 0.8123620309050773 | 0.8382687927107062 | 0.8840819002592465 |
| RandomForestClassifier | 0.8451219512195122 | 0.8654708520179372 | 0.8520971302428256 | 0.8587319243604005 | 0.9276214879910496 |
| GradientBoostingClassifier | 0.8463414634146341 | 0.8625277161862528 | 0.8587196467991169 | 0.8606194690265486 | 0.9188937209400244 |

**Chart:** `outputs/charts/best_classifier_confusion_matrix.png`

---

## 17. Best Model Selection

### 17.1 Best Regression Model — GradientBoostingRegressor

**Selection Criterion:** Lowest RMSE (and correspondingly highest R²)

| Model | RMSE | R² | Rank |
|-------|------|----|------|
| GradientBoostingRegressor | **11.3952** | **0.6874** | 1 ✅ |
| RandomForestRegressor | 11.4357 | 0.6852 | 2 |
| LinearRegression | 11.6108 | 0.6755 | 3 |
| DecisionTreeRegressor | 12.8313 | 0.6037 | 4 |

**Rationale:**
- Achieved lowest RMSE (11.3952) and highest R² (0.6874) simultaneously
- GradientBoosting's sequential error-correction particularly benefits mixed feature datasets
- Margin over RandomForest is small but consistent (RMSE 0.04 lower, R² 0.0022 higher)
- DecisionTree overfits — highest error; LinearRegression assumes linearity that doesn't fully hold

**Model saved:** `models/best_regression_model.joblib`

**Interpretation:** R² = 0.6874 means the model explains **68.74%** of variance in student
attendance percentage. The remaining unexplained variance reflects features with near-zero
correlation (travel distance, medical leave, late count) that were included for completeness
but contribute minimal predictive signal.

### 17.2 Best Classification Model — GradientBoostingClassifier

**Selection Criterion:** Highest F1-Score, then Recall (accuracy alone is insufficient
due to class imbalance and early-warning context)

| Model | F1-Score | Recall | Accuracy | ROC-AUC | Rank |
|-------|----------|--------|----------|---------|------|
| GradientBoostingClassifier | **0.8606** | **0.8587** | 0.8463 | 0.9189 | 1 ✅ |
| RandomForestClassifier | 0.8587 | 0.8521 | 0.8451 | 0.9276 | 2 |
| LogisticRegression | 0.8549 | 0.8587 | 0.8390 | 0.9246 | 3 |
| DecisionTreeClassifier | 0.8383 | 0.8124 | 0.8268 | 0.8841 | 4 |

**Rationale:**
- Highest F1-Score (0.8606) balances Precision and Recall optimally
- Equal Recall to LogisticRegression (0.8587) but higher F1 and Accuracy
- RandomForest has higher ROC-AUC (0.9276) but lower F1-Score — ROC-AUC is not the
  primary criterion for this early-warning use case
- DecisionTree shows worst Recall (0.8124) — unacceptable for an early-warning system

**Model saved:** `models/best_classification_model.joblib`

**Interpretation:**
- **Precision (86.25%):** When the model flags a student as Defaulter, it is correct 86.25% of the time
- **Recall (85.87%):** The model correctly identifies 85.87% of all actual Defaulters
- **F1-Score (0.8606):** Strong balance between identifying Defaulters and avoiding false alarms
- **ROC-AUC (0.9189):** Excellent discriminating power across all classification thresholds

---

## 18. Sample Prediction

The following demonstration uses the saved model pipelines to predict for a hypothetical
student. This student is not part of the training or test data.

**Sample Student Profile:**

| Feature | Value |
|---------|-------|
| Gender | Male |
| Department | Computer Engineering |
| Year | Third Year |
| Semester | Fifth Semester |
| Subject | Data Structures & Algorithms |
| Age | 20 |
| Previous_Attendance_Percentage | 68.5% |
| Assignment_Score | 62.0 |
| Internal_Marks | 15.0 |
| Study_Hours_Per_Week | 10.0 |
| Medical_Leave_Days | 2 |
| Travel_Distance_KM | 8.5 |
| Previous_Exam_Score | 58.0 |
| Late_Count | 1 |
| Online_Class_Attendance | 70.0% |

*Actual prediction output can be reproduced by running the code cell in*
`notebooks/05_summary_report.ipynb` *Section 11.*

**Loading the models:**
```python
import joblib
best_regressor   = joblib.load("models/best_regression_model.joblib")
best_classifier  = joblib.load("models/best_classification_model.joblib")

# Predict
predicted_pct    = best_regressor.predict(sample_student)[0]
predicted_status = "Defaulter" if best_classifier.predict(sample_student)[0] == 1 else "Regular"
predicted_proba  = best_classifier.predict_proba(sample_student)[0]
```

---

## 19. Findings

### 19.1 Dataset Findings
1. The 205-student dataset (4,100 records) is fully clean — 0 missing values, 0 duplicates,
   25/25 validation checks passed
2. **55.27%** of records fall below the 75% threshold (Defaulter) — the threshold is
   genuinely challenging
3. Mean attendance (**68.67%**) is below the 75% cutoff, indicating that the average
   student in this dataset is a Defaulter

### 19.2 EDA Findings
4. Subject-level attendance variation is minimal (< 1%) — attendance behaviour is primarily
   student-level, not subject-driven
5. Computer Engineering students show higher mean attendance (70.89%) than MCA (67.75%)
6. Prior academic behavior dominates as a predictor: `Previous_Attendance_Percentage`
   (r=0.72) and `Internal_Marks` (r=0.67) are the two strongest correlates
7. Logistical factors (`Travel_Distance_KM`, `Late_Count`, `Medical_Leave_Days`) show
   no meaningful correlation — these do not systematically drive attendance in this dataset

### 19.3 Modelling Findings
8. **GradientBoostingRegressor** is the best regressor with RMSE=11.3952 and R²=0.6874
9. **GradientBoostingClassifier** is the best classifier with F1=0.8606, Recall=0.8587
10. Linear models (LinearRegression, LogisticRegression) are competitive — they are
    interpretable baselines that perform near the level of more complex ensembles
11. DecisionTree models (both regressor and classifier) show the weakest performance,
    suggesting single-tree models overfit on this dataset

---

## 20. Practical Applications

If deployed on real (properly anonymized, consent-compliant) student data:

| Use Case | Description |
|----------|-------------|
| **Early Semester Warning** | Predict attendance trajectory after the first few weeks; trigger counseling before the attendance falls irreversibly below 75% |
| **Department-Level Analytics** | HOD can view department-wide attendance risk distribution; allocate faculty support accordingly |
| **Class Teacher Dashboard** | Teachers receive automated flags for students predicted as Defaulters in their specific subject |
| **Student Self-Assessment** | Students can input their own profile and receive a predicted attendance status — proactive self-monitoring |
| **Institutional Policy Design** | Analyze which feature groups (academic engagement vs. logistical factors) are most predictive; inform policy |

**Deployment Pipeline:**
```
Attendance Data → Preprocessing → Trained Pipeline → Prediction → Alert / Report
```

---

## 21. Limitations

| # | Limitation | Impact Level |
|---|------------|--------------|
| 1 | **Synthetic Data** — Results are statistically modeled, not empirically observed from real student behavior | High |
| 2 | **No Causal Analysis** — Correlations are identified, not causal mechanisms | Medium |
| 3 | **No Temporal Component** — Attendance is recorded as period-level totals, not as a week-by-week time series | Medium |
| 4 | **No External Factors** — Health status, family income, mental health, transportation access are not modeled | Medium |
| 5 | **Fixed Threshold** — The 75% threshold is used as a universal rule; real institutions may apply different criteria | Low |
| 6 | **Model Generalizability** — A model trained on synthetic data cannot be directly deployed on real student data without retraining | High |
| 7 | **Dataset Size** — 205 students is a moderate size; larger datasets would improve model stability | Low |
| 8 | **Leakage Exclusion Trade-off** — Excluding `Classes_Attended` and `Total_Classes` is necessary but reduces R² | Medium |

---

## 22. Future Scope

| Direction | Description |
|-----------|-------------|
| **Time-Series Modeling** | Use LSTM, Transformer, or Prophet on week-by-week attendance sequences to detect deterioration early in the semester |
| **Real Data Integration** | Retrain the complete pipeline on real, properly anonymized, consent-based student attendance data for institutional deployment |
| **Explainability (SHAP)** | Apply SHAP values to explain individual predictions — why a specific student was flagged as Defaulter |
| **Multi-Class Classification** | Expand to 3-class model: Regular / At-Risk / Critical-Defaulter for more granular early-warning |
| **Web Dashboard** | Build a Streamlit or Flask-based dashboard for real-time prediction and visualization |
| **Differential Privacy** | Apply differential privacy mechanisms to formal mathematical guarantees during synthetic generation |
| **Cross-Cohort Benchmarking** | Extend the dataset to additional departments, years, and institution types |
| **Active Learning** | Identify the most uncertain predictions and design targeted data collection to improve model accuracy |

---

## 23. Conclusion

This project demonstrates a complete, reproducible, and ethically responsible data science
workflow for student attendance analysis and prediction. Working entirely with a synthetic
dataset eliminates privacy risks while preserving the ability to explore realistic attendance
patterns and build functional predictive models.

**Key accomplishments:**

- Generated and validated a clean, realistic 205-student synthetic attendance dataset
  (4,100 records, 25/25 validation checks passed)
- Conducted thorough EDA revealing that prior academic behavior is the dominant predictor
  of attendance, with logistical factors showing negligible correlation
- Trained and evaluated 8 machine learning models (4 regression + 4 classification)
  using rigorous preprocessing pipelines and principled evaluation criteria
- Selected **GradientBoostingRegressor** as the best regression model (RMSE: 11.3952,
  R²: 0.6874) and **GradientBoostingClassifier** as the best classification model
  (F1-Score: 0.8606, ROC-AUC: 0.9189)
- Saved deployable model pipelines and created comprehensive documentation

The project establishes that **Gradient Boosting ensemble methods** consistently
outperform simpler models on mixed-feature attendance datasets. The classification model's
Recall of **85.87%** makes it suitable for an early-warning system where correctly
identifying Defaulters is the highest priority.

> **Privacy Assurance:** This project used zero real student data at any stage.
> All records are computer-generated. The `private_original_data/` directory was
> isolated and never accessed. This project is safe for academic submission,
> public portfolio sharing, and viva demonstration.

---

## 24. References

1. Breiman, L. (2001). *Random Forests*. Machine Learning, 45(1), 5–32.
2. Friedman, J. H. (2001). *Greedy Function Approximation: A Gradient Boosting Machine*.
   Annals of Statistics, 29(5), 1189–1232.
3. Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*.
   Journal of Machine Learning Research, 12, 2825–2830.
4. McKinney, W. (2010). *Data Structures for Statistical Computing in Python*.
   Proceedings of the 9th Python in Science Conference, 51–56.
5. Waskom, M. (2021). *Seaborn: Statistical Data Visualization*.
   Journal of Open Source Software, 6(60), 3021.
6. Harris, C. R. et al. (2020). *Array Programming with NumPy*.
   Nature, 585, 357–362.
7. European Commission. (2018). *General Data Protection Regulation (GDPR)*.
   Official Journal of the European Union, L 119/1.
8. Dwork, C. (2006). *Differential Privacy*. International Colloquium on Automata,
   Languages and Programming, 1–12.
9. Tinto, V. (1975). *Dropout from Higher Education: A Theoretical Synthesis of Recent
   Research*. Review of Educational Research, 45(1), 89–125.
10. scikit-learn Documentation. (2024). *Pipeline, ColumnTransformer, GradientBoosting*.
    Retrieved from https://scikit-learn.org/stable/

---

## 25. Appendix

### A. File Structure

```
Data_Science_attendence_project/
├── data/
│   ├── student_attendance_205_students.csv      [Main dataset — 4,100 rows × 21 cols]
│   ├── student_attendance_205_students.xlsx
│   ├── student_attendance.csv                   [Original 60-student dataset]
│   ├── DATASET_DICTIONARY.md
│   └── SYNTHETIC_DATA_NOTICE.md
├── models/
│   ├── best_regression_model.joblib             [GradientBoostingRegressor pipeline]
│   └── best_classification_model.joblib         [GradientBoostingClassifier pipeline]
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_regression_model.ipynb
│   ├── 03_classification_model.ipynb
│   └── 05_summary_report.ipynb
├── outputs/
│   ├── charts/                                  [11 PNG visualization files]
│   ├── regression_model_results.csv
│   ├── classification_model_results.csv
│   ├── final_model_comparison.csv
│   ├── final_project_summary.md
│   ├── final_findings.txt
│   ├── eda_summary.md
│   ├── final_dataset_validation_report.txt
│   └── dataset_validation_report.txt
├── report/
│   ├── project_report.md                        [This file]
│   └── project_report.pdf                       [PDF version — see conversion note]
├── presentation/
│   ├── presentation_content.md
│   ├── project_presentation.pptx
│   └── viva_questions.md
├── src/
│   ├── generate_dataset.py
│   ├── extend_dataset_to_205.py
│   ├── validate_dataset.py
│   ├── validate_final_dataset.py
│   ├── exploratory_analysis.py
│   ├── train_regression.py
│   ├── train_classification.py
│   ├── generate_eda_notebook.py
│   ├── generate_regression_notebook.py
│   ├── generate_classification_notebook.py
│   └── generate_summary_notebook.py
├── private_original_data/                       [ISOLATED — never accessed by scripts]
├── PROJECT_PLAN.md
└── PROJECT_STATUS.md
```

### B. Random Seeds Used

| Script | Seed | Purpose |
|--------|------|---------|
| `generate_dataset.py` | 42 | 60-student base dataset |
| `extend_dataset_to_205.py` | 42 + 200 = 242 | MCA extension dataset |
| All model training | 42 | Train-test split and model initialization |

### C. Python Environment

| Package | Version (from PROJECT_STATUS.md) |
|---------|----------------------------------|
| Python | 3.13.7 |
| pandas | 2.3.3 |
| numpy | 2.3.3 |
| scikit-learn | Installed (version per pip freeze) |
| matplotlib | Installed |
| seaborn | Installed |
| joblib | Installed |
| openpyxl | 3.1.5 |

### D. Metrics Verification

All metric values in this report were verified directly against their source CSV files:
- Regression metrics: `outputs/regression_model_results.csv`
- Classification metrics: `outputs/classification_model_results.csv`

No values were estimated, rounded incorrectly, or fabricated. Full-precision values
are provided in Sections 15 and 16.
