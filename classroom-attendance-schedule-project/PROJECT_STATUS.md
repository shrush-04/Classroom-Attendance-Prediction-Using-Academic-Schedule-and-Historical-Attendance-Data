# Project Status

**Project Title:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data  
**Class Scope:** MCA Final Year (Sem III)  
**Last Updated:** 2026-08-30  

---

## Development Milestones Summary

| Phase | Milestone | Status | Description |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Setup & Administration Templates** | 🟢 **Completed** | Excel/CSV templates, protocols, checklists, and log designs created. |
| **Phase 2** | **Python Core Pipelines** | 🟢 **Completed** | Scripts for validation, cleaning, feature engineering, training, and predicting written. |
| **Phase 3** | **Jupyter Notebooks** | 🟢 **Completed** | Interlock notebooks (01 to 05) generated for user interactiveness. |
| **Phase 4** | **Streamlit App UI** | 🟢 **Completed** | Dark-themed application dashboard completed. |
| **Phase 5** | **Documentation & Presentation** | 🟢 **Completed** | Finalizing thesis project reports, viva prep Q&As, and checklists. |
| **Phase 6** | **Real-world Verification** | 🔴 **Pending Data** | Waiting for physically verified student registers to be copied to raw data. |

---

## Detailed Task Logs

### Phase 1: Setup & Administration Templates
- [x] Create project subfolders (`data/raw`, `data/processed`, etc.)
- [x] Generate blank `raw_lecture_attendance_template.csv`
- [x] Generate blank `raw_lecture_attendance_template.xlsx`
- [x] Write `data_dictionary.md` and `example_row_format.md`
- [x] Write privacy policies and source checklists in `docs/`

### Phase 2: Core Python Pipelines
- [x] Implement validation checks (schema checks, chronological checks, and PII filters) in `validate_raw_data.py`
- [x] Implement standardization and missing log audit in `clean_data.py`
- [x] Implement shifted lag features and rolling averages in `feature_engineering.py`
- [x] Implement pipeline transformers and model training loops in `train_models.py`
- [x] Implement performance metrics calculations in `evaluate_models.py`
- [x] Implement prediction solver in `predict_future_lecture.py`
- [x] Implement pipeline orchestrator in `run_pipeline.py`

### Phase 3: Jupyter Notebooks
- [x] Build notebook 01 for raw data validation
- [x] Build notebook 02 for preprocessing & features
- [x] Build notebook 03 for EDA and visual plotting
- [x] Build notebook 04 for training models
- [x] Build notebook 05 for predicting future classes

### Phase 4: Streamlit App
- [x] Implement dashboard styling (custom CSS cards)
- [x] Add dynamic resource checks (warn if data/models are absent)
- [x] Create historical trend visualizations
- [x] Build interactive predictive forms
- [x] Document limitations, disclaimers, and collection protocols

### Phase 5: Documentation & Reports
- [x] Create master project `README.md`
- [x] Write academic `PROJECT_PLAN.md`
- [x] Write academic `project_report.md`
- [x] Write `presentation_content.md`
- [x] Compile 45 detailed `viva_questions.md`
- [x] Write `FINAL_CHECKLIST.md`

### Phase 6: Model Execution
- [ ] Paste original attendance data into `data/raw/raw_lecture_attendance.csv`
- [ ] Run `python src/run_pipeline.py` to train model pipelines
- [ ] Open Streamlit app and verify predictive accuracy
