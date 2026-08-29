# Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System

This repository contains a complete, end-to-end data science and machine learning project focused on predicting student attendance and identifying students at academic risk ("Defaulters").

> **⚠️ PRIVACY & SYNTHETIC DATA NOTICE**
> 
> All student records in this project are **100% synthetic and computer-generated**.
> No real student names, roll numbers, email IDs, or actual academic files are used or stored.
> The dataset does not represent, map to, or expose any real student or classroom records.
> This repository is safe for public distribution and academic submission.

---

## 📌 Terminology Mapping

The classification models and data files consistently use the following target categories:
*   **Regular:** Equivalent to "Safe" (Attendance Percentage $\ge 75\%$)
*   **Defaulter:** Equivalent to "At Risk" (Attendance Percentage $< 75\%$)

---

## 📂 Project Structure

```
├── data/
│   ├── student_attendance_205_students.csv      [Main dataset — 4,100 rows × 21 cols]
│   ├── student_attendance_205_students.xlsx
│   ├── DATASET_DICTIONARY.md                    [Column definitions and ranges]
│   └── SYNTHETIC_DATA_NOTICE.md                 [Detailed privacy policies]
├── models/
│   ├── best_regression_model.joblib             [GradientBoostingRegressor pipeline]
│   └── best_classification_model.joblib         [GradientBoostingClassifier pipeline]
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb       [EDA visualizations & correlations]
│   ├── 02_regression_model.ipynb                [Regression model comparisons]
│   ├── 03_classification_model.ipynb            [Classification model comparisons]
│   └── 05_summary_report.ipynb                  [Final executed project summary]
├── outputs/
│   ├── charts/                                  [11 PNG visualization plots]
│   ├── final_project_summary.md                 [Markdown summary with metrics]
│   ├── final_model_comparison.csv               [Sourced model results comparison]
│   └── final_findings.txt                       [Detailed plain-text findings]
├── report/
│   └── project_report.pdf                       [Full academic project report PDF]
├── presentation/
│   ├── project_presentation.pptx                [14-slide corporate dark presentation]
│   ├── presentation_content.md                  [Presentation script and notes]
│   └── viva_questions.md                        [45 Viva questions and answers]
├── src/                                         [Core standalone Python utility scripts]
│   ├── generate_dataset.py
│   ├── extend_dataset_to_205.py
│   ├── validate_final_dataset.py
│   ├── exploratory_analysis.py
│   ├── train_regression.py
│   ├── train_classification.py
│   ├── generate_summary_notebook.py
│   ├── generate_pptx.py
│   └── generate_pdf_report.py
├── README.md                                    [This file]
└── requirements.txt                             [Python dependencies list]
```

---

## 🚀 Installation & Setup

1. Clone or download this project workspace.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Run the Jupyter Notebook environment to explore the notebooks:
   ```bash
   jupyter notebook
   ```

---

## 📊 Summary of Final Model Performance

All values are verified and sourced directly from outputs/charts and result CSVs.

*   **Best Regression Model:** `GradientBoostingRegressor` (RMSE: **11.3952**, $R^2$: **0.6874**)
*   **Best Classification Model:** `GradientBoostingClassifier` (F1-score: **0.8606**, Recall: **0.8587**, ROC-AUC: **0.9189**)

*Note: Preprocessing (Imputation, One-Hot Encoding, scaling) is fully contained inside the saved `.joblib` pipelines, allowing plug-and-play predictions on new student records.*

---
*Generated: August 2026*  
*Project: Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System*
