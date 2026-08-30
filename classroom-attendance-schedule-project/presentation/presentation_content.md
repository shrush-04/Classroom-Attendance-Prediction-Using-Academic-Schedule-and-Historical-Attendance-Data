# Project Presentation Content

This document outlines the slide-by-slide layout, key bullet points, and speaker notes for the final project presentation.

---

### Slide 1: Project Title Slide
- **Title:** Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data
- **Subtitle:** A Privacy-Preserving Predictive System for Lecture-Level Analysis
- **Context:** MCA Final Year | Semester III Project
- **Speaker Notes:** "Good morning members of the jury. Today I am presenting my project on predicting classroom attendance. Unlike conventional systems that track individual students, our system implements Privacy by Design to predict lecture-level statistics using timetable and calendar schedules."

---

### Slide 2: Problem Statement
- **Core Challenge:** Low classroom attendance impacts academic outcomes, but profiling individual students raises surveillance and privacy concerns.
- **Data Risk:** Storing student names, emails, and rolls in predictive databases exposes PII to breaches.
- **The Solution:** Aggregating data at the *lecture* level. Schedulers do not need to know *who* skips, only *when* and *why* attendance will drop.
- **Speaker Notes:** "The main issue is finding a balance between academic planning and data ethics. Schedulers need aggregate statistics, not private student-level details. This project bridges that gap."

---

### Slide 3: Project Objectives
- Create a template architecture for aggregate lecture log collection.
- Code a complete pipelines for validation, cleaning, and lag engineering.
- Implement chronological splitting to eliminate predictive data leakage.
- Compare multiple regression and classification algorithms.
- Deploy an interactive dark-themed dashboard for department scheduler use.
- **Speaker Notes:** "Our objective is to deliver a complete ETL and ML pipeline that runs safely, validates rules automatically, and outputs predictions on a scheduler dashboard."

---

### Slide 4: Data Collection Methodology
- **Administrative Registers:** Timetables, lab logs, exam tables, and official registers.
- **Zero Student PII:** Student names, roll numbers, emails, or biometrics are never imported.
- **Faculty Encoding:** Faculty names are mapped to codes like `F001`, `F002` to protect instructor privacy.
- **Granularity:** Each row represents a single scheduled class session.
- **Speaker Notes:** "Our data collection is aggregate. We only count the total number of present students per lecture slot. Faculty names are also encoded to ensure privacy."

---

### Slide 5: Schema and Templates
- **Required Columns:** Lecture_ID, Date, Day_of_Week, Lecture_Number, Start/End Time, Subject, Faculty_ID, Total_Enrolled, Students_Present, Attendance_Percentage, Practical_Theory, Test_Week, Assignment_Due, Holiday_Before_After.
- **Optional Columns:** Weather, Special_Event.
- **Logbook Template:** Handwritten log design created for administrative representatives.
- **Speaker Notes:** "We created standardized Excel and CSV templates to ensure that the raw data structure is uniform and complies with the data dictionary."

---

### Slide 6: Preprocessing & Feature Engineering
- **Validation:** 16 rules enforcing formats, chronological order, capacities, and filtering PII.
- **Feature Engineering (No Leakage):**
  - Time indicators (Morning/Afternoon, Day of Semester, Week of Year).
  - Shifted previous lecture attendance percentage (Lag 1).
  - Shifted rolling average of previous 3 lectures.
  - Expanding subject historical average.
- **Speaker Notes:** "Data leakage is a major risk in time-series forecasting. We strictly sort all data chronologically and apply shift operations on target-derived features so that future data is never leaked."

---

### Slide 7: Exploratory Data Analysis (EDA)
- `[TO BE COMPLETED AFTER ORIGINAL DATA COLLECTION AND MODEL EXECUTION]`
- **Speaker Notes:** "Once original data is added and the pipeline runs, this slide will display the distributions, subject-wise attendance boxplots, and feature correlations."

---

### Slide 8: Machine Learning Pipelines
- **Features Input:** Scheduled details, lag averages, holiday buffers, test flags.
- **Regression Models (Target: Students_Present):**
  - Linear Regression (Baseline), Decision Tree, Random Forest, Gradient Boosting.
- **Classification Models (Target: Attendance_Band):**
  - Logistic Regression (Baseline), Decision Tree, Random Forest, SVM, k-NN.
- **Pipelines:** Implemented via Scikit-Learn `Pipeline` and `ColumnTransformer`.
- **Speaker Notes:** "We construct preprocessing pipelines that impute and scale numbers, and one-hot encode categoricals, feeding them directly into our ML algorithms."

---

### Slide 9: Experiment Results
- `[TO BE COMPLETED AFTER ORIGINAL DATA COLLECTION AND MODEL EXECUTION]`
- **Speaker Notes:** "Here we will display the comparative metrics (MAE, RMSE, R2 for regression; Accuracy, F1-score for classification) for all tested models."

---

### Slide 10: Streamlit Dashboard UI
- Premium dark-themed, glassmorphic layout.
- Renders historical analysis graphs when cleaned data is present.
- Displays interactive forms for users to input future lecture details.
- Returns predicted attendance percentage, headcount, band, and low-attendance risk level.
- **Speaker Notes:** "We built a Streamlit application that acts as the user interface for our models, displaying visual trends and predicting slot-wise attendance dynamically."

---

### Slide 11: Limitations & Ethical Boundaries
- **Timetable Swaps:** Spontaneous timetable swaps require manual updates.
- **First-Week Lags:** Lags default to historical means during the first week of the term.
- **Model Usage Policy:** Intended purely for scheduling efficiency, not student grading or disciplinary profiling.
- **Speaker Notes:** "We clearly define limitations, such as lag-defaults in week one, and state that this tool is for scheduling planning, not individual monitoring."

---

### Slide 12: Conclusion & Future Scope
- Successfully designed a privacy-preserving predictive model framework.
- Chronological pipelines run safely and scale to other departments.
- Future work: Integration with automated timetabling software.
- **Speaker Notes:** "In conclusion, this project proves we can get valuable scheduling insights while respecting privacy. I am now open to your questions. Thank you."
