# Final Submission Checklist

This checklist audits the readiness of all files in the **Classroom Attendance Prediction** project.

---

## 1. Project Folder Structure

```text
classroom-attendance-schedule-project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── templates/
├── notebooks/
├── src/
├── models/
├── outputs/
│   ├── charts/
│   └── experiment_results/
├── app/
├── report/
├── presentation/
└── docs/
```

---

## 2. Checklist of Created Files

| File Path | Purpose | Status |
| :--- | :--- | :--- |
| **DATA Collection & Templates** | | |
| [raw_lecture_attendance_template.xlsx](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/data/templates/raw_lecture_attendance_template.xlsx) | Blank Excel template | 🟢 **Ready** |
| [raw_lecture_attendance_template.csv](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/data/templates/raw_lecture_attendance_template.csv) | Blank CSV template | 🟢 **Ready** |
| [data_dictionary.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/data/templates/data_dictionary.md) | Fields definition sheet | 🟢 **Ready** |
| [example_row_format.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/data/templates/example_row_format.md) | Sample row layout | 🟢 **Ready** |
| [data_collection_protocol.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/docs/data_collection_protocol.md) | Data aggregation steps | 🟢 **Ready** |
| [handwritten_logbook_template.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/docs/handwritten_logbook_template.md) | Physical log paper template | 🟢 **Ready** |
| [privacy_and_ethics.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/docs/privacy_and_ethics.md) | Privacy commitment guidelines | 🟢 **Ready** |
| [source_record_checklist.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/docs/source_record_checklist.md) | Quality checklist | 🟢 **Ready** |
| **Python Pipelines (`src/`)** | | |
| [validate_raw_data.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/validate_raw_data.py) | 16 validations check code | 🟢 **Ready** |
| [clean_data.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/clean_data.py) | Cleaner and null-logger code | 🟢 **Ready** |
| [feature_engineering.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/feature_engineering.py) | Lag and rolling features code | 🟢 **Ready** |
| [train_models.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/train_models.py) | Pipelines training code | 🟢 **Ready** |
| [evaluate_models.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/evaluate_models.py) | Multi-model evaluation code | 🟢 **Ready** |
| [predict_future_lecture.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/predict_future_lecture.py) | Session prediction code | 🟢 **Ready** |
| [run_pipeline.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/src/run_pipeline.py) | Master pipeline runner code | 🟢 **Ready** |
| **Jupyter Notebooks** | | |
| [01_data_validation.ipynb](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/notebooks/01_data_validation.ipynb) | Interactive raw validation | 🟢 **Ready** |
| [02_data_cleaning_and_feature_engineering.ipynb](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/notebooks/02_data_cleaning_and_feature_engineering.ipynb) | Preprocessing notebook | 🟢 **Ready** |
| [03_exploratory_data_analysis.ipynb](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/notebooks/03_exploratory_data_analysis.ipynb) | Data statistics plotting | 🟢 **Ready** |
| [04_model_training_and_evaluation.ipynb](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/notebooks/04_model_training_and_evaluation.ipynb) | Model training notebook | 🟢 **Ready** |
| [05_future_lecture_prediction.ipynb](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/notebooks/05_future_lecture_prediction.ipynb) | Predicted slots notebook | 🟢 **Ready** |
| **Streamlit UI** | | |
| [streamlit_app.py](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/app/streamlit_app.py) | Dark-themed application dashboard | 🟢 **Ready** |
| [README.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/app/README.md) | Execution run commands | 🟢 **Ready** |
| **Reports & Milestones** | | |
| [README.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/README.md) | Setup and pipelines guide | 🟢 **Ready** |
| [PROJECT_PLAN.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/PROJECT_PLAN.md) | Scope and WBS | 🟢 **Ready** |
| [PROJECT_STATUS.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/PROJECT_STATUS.md) | Milestones and task checklist | 🟢 **Ready** |
| [requirements.txt](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/requirements.txt) | Dependencies list | 🟢 **Ready** |
| [project_report.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/report/project_report.md) | Main project report text | 🟢 **Ready** |
| [presentation_content.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/presentation/presentation_content.md) | Slide details outline | 🟢 **Ready** |
| [viva_questions.md](file:///d:/Data_Science_attendence_project/classroom-attendance-schedule-project/presentation/viva_questions.md) | 45 Viva questions and answers | 🟢 **Ready** |

---

## 3. Files Requiring Original Attendance Data

The following directories/files will remain empty or contain default messages until the user provides verified attendance records:
- **`data/raw/raw_lecture_attendance.csv` (or `.xlsx`)**: Requires user to enter verified numbers.
- **`models/best_present_count_model.joblib`**: Generated after pipeline training.
- **`models/best_attendance_band_model.joblib`**: Generated after pipeline training.
- **`outputs/charts/`**: Charts populated after pipeline runs.
- **`outputs/experiment_results/regression_results.csv`**: Saved after pipeline training.
- **`outputs/experiment_results/classification_results.csv`**: Saved after pipeline training.
- **`outputs/experiment_results/experiment_table.md`**: Saved after pipeline training.

---

## 4. The Single Remaining Manual Requirement

> [!IMPORTANT]
> The project cannot be claimed as fully complete until this final manual step is performed:
> **Copying physically verified classroom lecture attendance counts (Timetable slot, Total Enrolled batch strength, Students Present count) into `classroom-attendance-schedule-project/data/raw/raw_lecture_attendance.csv` and running `python classroom-attendance-schedule-project/src/run_pipeline.py`.**
