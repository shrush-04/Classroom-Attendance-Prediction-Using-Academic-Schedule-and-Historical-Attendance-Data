# Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data

This project implements a lecture-level attendance prediction system designed to help department planners and schedulers predict future class session attendance without violating student privacy. The system utilizes academic schedules, Continuous Internal Evaluation (CIE) calendars, timetables, and aggregate historical class logs.

## Project Folder Structure

```text
classroom-attendance-schedule-project/
├── data/
│   ├── raw/                  # Place raw_lecture_attendance.csv here
│   ├── processed/            # Cleaned and feature engineered CSV datasets
│   └── templates/            # Data dictionaries and blank CSV/Excel templates
├── notebooks/                # Step-by-step Jupyter Notebooks for analysis
├── src/                      # Data processing, feature engineering, and ML scripts
├── models/                   # Serialized ML pipeline joblib files
├── outputs/
│   ├── charts/               # Generated EDA and model performance charts
│   ├── experiment_results/   # CSV lists of metrics for compared algorithms
│   ├── final_demo_instructions.md # Guide to running dashboard demos ✅
│   └── final_viva_summary.md # Viva presentation Q&A sheet ✅
├── app/                      # Streamlit application dashboard code
├── report/
│   ├── project_report.md     # Markdown project report
│   └── project_report.pdf    # Compiled professional PDF report ✅
├── presentation/
│   ├── presentation_content.md # Presentation script
│   └── project_presentation.pptx # Compiled slide deck (13 slides) ✅
└── docs/                     # Administrative checklists and collection protocol docs
```

## Installation & Setup

1. **Verify Python Installation:**
   Requires Python 3.8+ (tested on Python 3.13.7).

2. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```
   *Required packages: pandas, numpy, scikit-learn, joblib, matplotlib, seaborn, openpyxl, streamlit, jinja2.*

## How to Add Raw Data
1. Locate the blank templates inside `data/templates/`.
2. Extract lecture-level attendance counts (Total Strength and Present count) from the class registers.
3. Place your data rows in `data/raw/raw_lecture_attendance.csv` following the headers and rules defined in `data/templates/data_dictionary.md`.
4. *Do not record student names, roll numbers, or emails.*

## Executing the Data & Modeling Pipeline

You can run the entire pipeline end-to-end using the main orchestrator script:
```bash
python classroom-attendance-schedule-project/src/run_pipeline.py
```

### Or run steps individually:

1. **Validate Data:**
   ```bash
   python classroom-attendance-schedule-project/src/validate_raw_data.py classroom-attendance-schedule-project/data/raw/raw_lecture_attendance.csv
   ```
2. **Clean Data:**
   ```bash
   python classroom-attendance-schedule-project/src/clean_data.py classroom-attendance-schedule-project/data/raw/raw_lecture_attendance.csv
   ```
3. **Feature Engineering:**
   ```bash
   python classroom-attendance-schedule-project/src/feature_engineering.py classroom-attendance-schedule-project/data/processed/cleaned_lecture_attendance.csv
   ```
4. **Train Models:**
   ```bash
   python classroom-attendance-schedule-project/src/train_models.py classroom-attendance-schedule-project/data/processed/feature_engineered_attendance.csv
   ```
5. **Evaluate Models:**
   ```bash
   python classroom-attendance-schedule-project/src/evaluate_models.py classroom-attendance-schedule-project/data/processed/feature_engineered_attendance.csv
   ```

## Running the Streamlit App

Launch the interactive dark-themed dashboard:
```bash
streamlit run classroom-attendance-schedule-project/app/streamlit_app.py
```

## Privacy Rules (Privacy by Design)
- Never log individual student identifiers (names, roll numbers, emails, biometrics, photos).
- Faculty names must be anonymized (encoded as `F001`, `F002`).
- Do not create student-level ID mapping tables.
- Keep data aggregation at the lecture level.

## System Limitations
- Cannot capture spontaneous external shifts (e.g. transport strikes) not scheduled in academic logs.
- Predictions for the first week of semesters default to historical averages due to lag limitations.
- Requires physically verified class registers for baseline training.


## Dataset Placeholders (Continuous Evaluation Features)
- Internal_Test_Week and Assignment_Due columns are added in ttendance_stage1_final.csv as placeholders for future academic calendar integration. They are left blank/NaN intentionally because the official internal CIE (Continuous Internal Evaluation) exam schedule was not publicly available at the time of dataset construction. These represent planned future data collections rather than erroneous missing data.
