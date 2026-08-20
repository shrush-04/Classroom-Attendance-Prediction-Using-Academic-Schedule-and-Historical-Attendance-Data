# Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System
### Project Plan — College Data Science Project

> ⚠️ **Privacy Notice:** All student records used in this project are **fully synthetic** and computer-generated.
> No real student names, roll numbers, email IDs, or personal identifiers are used at any stage.
> The dataset does not represent, map to, or expose any real classroom data.

---

## 1. Problem Statement

Student attendance is a key indicator of academic engagement and performance. However, working directly
with real student data raises significant privacy concerns — exposure of personal identifiers, risk of
re-identification, and ethical issues with handling private academic records.

This project addresses that by constructing a **privacy-preserving synthetic dataset** that statistically
mirrors a real Third Year Computer Engineering class (Semester 5, 60 students, 5 subjects), without
touching any real student identity. Using this synthetic data, we apply **Exploratory Data Analysis (EDA)**,
**Regression**, and **Classification** models to analyze and predict attendance patterns.

---

## 2. Project Objectives

| # | Objective |
|---|-----------|
| 1 | Generate a synthetic, anonymous attendance dataset that preserves realistic statistical properties. |
| 2 | Perform thorough Exploratory Data Analysis (EDA) to uncover attendance trends and distributions. |
| 3 | Build a **Regression model** to predict a student's total attendance percentage. |
| 4 | Build a **Classification model** to predict whether a student is **At Risk** (attendance < 75%) or **Safe** (>= 75%). |
| 5 | Visualize findings with professional charts and graphs. |
| 6 | Demonstrate responsible, ethical data science practices. |

---

## 3. Dataset Design

### 3.1 Class Parameters (Non-Identifying Classroom Facts)

| Parameter | Value |
|-----------|-------|
| Department | Computer Engineering |
| Year | Third Year |
| Semester | Fifth Semester |
| Number of Students | 60 |
| Number of Subjects | 5 |
| Total Classes per Subject | 40 |
| Attendance Range | 50% to 98% |
| Approximate Mean Attendance | ~78% |

### 3.2 Subjects (Synthetic Labels)

| Subject Code | Subject Name |
|-------------|--------------|
| SUB01 | Data Structures & Algorithms |
| SUB02 | Database Management Systems |
| SUB03 | Computer Networks |
| SUB04 | Theory of Computation |
| SUB05 | Software Engineering |

### 3.3 Student Identifier Format

- All students are assigned anonymous IDs: **STU0001, STU0002, ... STU0060**
- No real names, roll numbers, or any personally identifiable information (PII) are used.
- No mapping table linking synthetic IDs to real students will ever be created.

### 3.4 Synthetic Features to Generate

| Feature | Description |
|---------|-------------|
| student_id | Anonymous ID (STU0001-STU0060) |
| sub01_attended ... sub05_attended | Classes attended per subject (integer, 0-40) |
| sub01_pct ... sub05_pct | Attendance percentage per subject |
| total_attended | Sum of classes attended across all subjects |
| total_possible | Total possible classes = 5 x 40 = 200 |
| overall_pct | (total_attended / total_possible) x 100 |
| risk_label | "At Risk" if overall_pct < 75, else "Safe" |

### 3.5 Generation Strategy

- Use numpy.random seeded for reproducibility.
- Model attendance using a clipped normal distribution (mean ~78%, std ~10%).
- Apply mild subject-level correlation so students who attend one subject also tend to attend others.
- All values rounded and clipped to valid integer range [0, 40].

---

## 4. Regression Objective

**Goal:** Predict a student's overall_pct (overall attendance percentage).

- **Input features:** sub01_attended, sub02_attended, sub03_attended, sub04_attended, sub05_attended
- **Target variable:** overall_pct
- **Models to try:** Linear Regression (baseline), Ridge/Lasso Regression, Random Forest Regressor
- **Evaluation metrics:** MAE, RMSE, R-squared

---

## 5. Classification Objective

**Goal:** Predict whether a student is "At Risk" or "Safe".

- **Input features:** Same 5 per-subject attendance counts
- **Target variable:** risk_label (binary: At Risk / Safe)
- **Models to try:** Logistic Regression (baseline), Decision Tree, Random Forest Classifier
- **Evaluation metrics:** Accuracy, Precision, Recall, F1-Score, Confusion Matrix, ROC-AUC

---

## 6. EDA Workflow

1. Dataset Overview — shape, dtypes, null check, descriptive statistics
2. Attendance Distribution — histogram of overall_pct with KDE
3. Subject-wise Analysis — boxplots and bar charts per subject
4. Correlation Heatmap — relationship between per-subject attendance values
5. Risk Label Distribution — pie chart / count plot (At Risk vs. Safe split)
6. Outlier Analysis — identifying very low or very high attendance students
7. Attendance vs. Risk — scatter plots or violin plots segmented by risk label
8. Cumulative Attendance — sorted bar chart showing student-level totals

---

## 7. Required Python Libraries

| Library | Purpose |
|---------|---------|
| numpy | Synthetic data generation, numerical operations |
| pandas | Data manipulation and analysis |
| matplotlib | Base plotting |
| seaborn | Statistical visualizations |
| scikit-learn | ML models, metrics, train-test split |
| scipy | Statistical tests (optional) |
| joblib | Model serialization (saving trained models) |
| jupyter | Interactive notebook environment |
| openpyxl | Export data to Excel format |

Installation command:
  pip install numpy pandas matplotlib seaborn scikit-learn scipy joblib jupyter openpyxl

---

## 8. Privacy Approach

| Principle | Implementation |
|-----------|---------------|
| Data Minimization | Only statistical classroom parameters are used — no personal data collected or stored. |
| Anonymization | All records use synthetic IDs (STU0001-STU0060). No real identifiers exist in any file. |
| No Re-identification Risk | No mapping table between synthetic IDs and real students is ever created. |
| Synthetic Data Labeling | Every output file, notebook, and report clearly labels the data as SYNTHETIC. |
| Honest Framing | Project states generated records are statistical simulations, not real records. |
| Source Isolation | The private original data file is never read, imported, or inspected by any project script. |

---

## 9. Expected Files

data/
  synthetic_attendance.csv          - Main synthetic dataset (60 rows x 13+ columns)
  synthetic_attendance.xlsx         - Excel version for review
  data_description.txt              - Column descriptions and metadata

notebooks/
  01_data_generation.ipynb          - Step 1: Synthetic data creation
  02_eda.ipynb                      - Step 2: Exploratory Data Analysis
  03_regression.ipynb               - Step 3: Regression modelling
  04_classification.ipynb           - Step 4: Classification modelling
  05_summary_report.ipynb           - Step 5: Summary and conclusions

src/
  generate_data.py                  - Standalone script: data generation
  eda_utils.py                      - Reusable EDA helper functions
  model_utils.py                    - Reusable model training/evaluation helpers

models/
  regression_model.pkl              - Saved best regression model
  classification_model.pkl          - Saved best classification model

outputs/charts/
  attendance_distribution.png
  subject_boxplots.png
  correlation_heatmap.png
  risk_label_distribution.png
  regression_results.png
  classification_confusion_matrix.png
  roc_curve.png

report/
  project_report.pdf                - Final written report

presentation/
  project_presentation.pptx        - Slide deck for viva/demo

---

## 10. Project Limitations

1. Synthetic Data — Results may not perfectly reflect real-world attendance dynamics.
2. No Causal Analysis — The project identifies patterns, not causes of poor attendance.
3. Small Dataset — With only 60 students, model generalizability is limited.
4. No Temporal Component — Attendance is recorded as a total count, not week-by-week.
5. Balanced Class Assumption — The synthetic 75% threshold may not match the institution's real criterion.
6. No External Factors — Variables like health, distance, family issues are not modeled.

---

## 11. Ethical Considerations

- No Real Student Harm: Since no real student data is used, there is zero risk of privacy breach or academic profiling.
- Transparent Labeling: All outputs clearly state data is synthetic.
- No Discrimination: The risk label is used for academic analysis only, not for any real-world judgment.
- Reproducibility: The random seed ensures anyone can reproduce the exact same synthetic dataset.
- Responsible Reporting: Project conclusions are carefully worded to avoid overgeneralizing synthetic findings.
- Respect for Institutional Data: The real classroom file is treated as private and is never accessed by project code.

---

## 12. Manual Tasks You Must Perform

| # | Task | When |
|---|------|------|
| 1 | Install required Python libraries (pip install ...) | Before running any notebook |
| 2 | Launch Jupyter Notebook (jupyter notebook) | When working on notebooks |
| 3 | Review generated synthetic_attendance.csv to confirm it looks realistic | After Step 1 |
| 4 | Choose the best model based on evaluation metrics | After Steps 3 and 4 |
| 5 | Write the project_report.pdf narrative in Word/LaTeX | After all notebooks complete |
| 6 | Create the project_presentation.pptx slide deck | Before submission/viva |
| 7 | Double-check that no real student data appears anywhere in data/ or outputs/ | Before final submission |
| 8 | Confirm that private_original_data/ folder is excluded from any shared zip or upload | Before submitting to college |

---

Document generated: 2026-08-20
Project: Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System
Department: Computer Engineering | Year: Third | Semester: Fifth
