# Academic Project Report

**Project Title:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data  
**Department:** Computer Applications (MCA)  
**Academic Year:** Final Year  
**Semester:** Third Semester  

---

## 1. Executive Summary
This project outlines a modern, privacy-preserving machine learning system designed to predict lecture-level classroom attendance. Student attendance is a primary indicator of academic health, but student-level databases present security vulnerabilities. By abstracting the analysis to the lecture slot level, this system utilizes timetable schedules, exam schedules, and historical lag variables to forecast student counts and attendance bands. When models are executed on physically verified log data, they provide administrative decision support to optimize course timetables.

## 2. Problem Statement & Objectives
### 2.1 Problem Statement
Traditional attendance analysis systems focus on individual student records. While useful for student auditing, these files present compliance risks (e.g. exposure of names, emails, and rolls). Furthermore, schedulers have no proactive tools to determine when and why class slots will see high default rates. There is a clear need for a prediction system that operates purely on aggregate, schedule-based parameters to forecast attendance without storing individual student identifiers.

### 2.2 Objectives
- Build a dataset architecture using only aggregate, lecture-level statistics.
- Construct administrative protocols to extract and compile attendance data securely.
- Code a complete pipeline to validate, clean, engineer lag features, and train models.
- Apply chronological test splits to accurately simulate real-world schedule forecasts.
- Design an interactive user dashboard for schedulers to input slot data and analyze risks.

## 3. Data Collection Methodology
### 3.1 Data Sources
The raw data is compiled by department representatives using only aggregate session metrics. The sources include:
- **Master Timetable:** Supplies slot numbers, classrooms, subject codes, and section details.
- **Faculty Registers:** Physical registries checked in-class to sum the number of present students.
- **Academic Calendar:** Used to flag upcoming holidays and week offsets.
- **Continuous Evaluation Schedule:** Identifies midterm testing weeks.

### 3.2 Privacy by Design Safeguards
- **Zero Student PII:** Student names, roll numbers, and emails are completely excluded.
- **Instructor Anonymization:** Faculty names are replaced with codes (e.g. `F001`, `F002`).
- **No Mapping Tables:** No internal database maps individual identifiers to records.

## 4. Preprocessing & Feature Engineering
### 4.1 Data Cleaning & Standardizing
Data validation checks enforce schemas and capacity rules (`Students_Present` <= `Total_Enrolled_Students`). Cleaning standardizes text case, formats dates, and audits missing records. Optional empty fields are logged as `Not_Collected` rather than fabricated.

### 4.2 Leakage-Free Feature Generation
To prevent model leakage, features are derived chronologically:
- **Lag Features:** Previous attendance rate and gap hours are shifted.
- **Rolling Features:** Moving averages exclude the current target class.
- **Historical Averages:** Expanding subject means use only preceding sessions.

## 5. Exploratory Data Analysis (EDA)
`[TO BE COMPLETED AFTER ORIGINAL DATA COLLECTION AND MODEL EXECUTION]`

## 6. Model Training & Experiments
The pipeline evaluates multiple models:
- **Regression (Target: Students_Present):** Linear Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor.
- **Classification (Target: Attendance_Band):** Logistic Regression, Decision Tree Classifier, Random Forest Classifier, Support Vector Machine, k-Nearest Neighbors.

### 6.1 Evaluation Partitioning
Model evaluation uses a chronological split where the first 80% of lectures are used for training and the last 20% are used for testing. Random splits are avoided to preserve temporal validity.

### 6.2 Model Performance Metrics
`[TO BE COMPLETED AFTER ORIGINAL DATA COLLECTION AND MODEL EXECUTION]`

## 7. Streamlit Dashboard
An interactive dashboard is implemented in `app/streamlit_app.py`. It renders historical trends and provides a form for planners to run predictions for future slots, returning expected headcounts, fill percentages, and low-attendance risk flags.

## 8. Limitations & Future Scope
### 8.1 Limitations
- Environmental factors (e.g. weather, traffic) are optional and hard to verify.
- The lag calculations are sensitive to schedule changes or missing classes.
- Models require at least a few weeks of baseline data before predictions stabilize.

### 8.2 Future Scope
- Integration with campus scheduling software.
- Incorporating campus-wide event logs (symposiums, placement drives).
- Extending the model to support multi-department class cohorts.

## 9. Conclusion
This project demonstrates that robust predictive modeling can coexist with strict privacy safeguards. By focusing on lecture-level characteristics rather than individual profiles, the system offers actionable scheduling recommendations to administrative departments while maintaining zero re-identification risks.
