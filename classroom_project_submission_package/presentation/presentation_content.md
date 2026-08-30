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
- **Speaker Notes:** "The main issue is balancing academic planning with data ethics. Schedulers need aggregate statistics, not private student-level details. This project bridges that gap."

---

### Slide 3: Project Objectives
- Create a template architecture for aggregate lecture log collection.
- Code a complete pipeline for validation, cleaning, and lag feature engineering.
- Implement chronological splitting to eliminate predictive data leakage.
- Compare multiple regression and classification algorithms against naive baselines.
- Deploy an interactive dashboard with honest model validity indicators.
- **Speaker Notes:** "Our objective is to deliver a complete ETL and ML pipeline that runs safely, validates rules automatically, and outputs predictions on a scheduler dashboard — with clear warnings when data is insufficient."

---

### Slide 4: Data Collection Methodology
- **Administrative Registers:** Timetables, lab logs, exam tables, and official registers.
- **Zero Student PII:** Student names, roll numbers, emails, or biometrics are never imported.
- **Faculty Encoding:** Faculty names are mapped to anonymous codes (`F_01`, `F_02`) to protect instructor privacy.
- **Granularity:** Each row represents a single scheduled class session.
- **Speaker Notes:** "Our data collection is aggregate. We only count the total number of present students per lecture slot. Faculty names are also encoded to ensure privacy."

---

### Slide 5: Schema and Templates
- **Required Columns:** Lecture_ID, Date, Day_of_Week, Lecture_Number, Start/End Time, Subject, Faculty_ID, Total_Enrolled_Students, Students_Present, Attendance_Percentage, Practical_Theory, Internal_Test_Week, Assignment_Due, Holiday_Before_After.
- **Optional Columns:** Weather, Special_Event.
- **Validation:** 16 automated checks enforce formats, capacities, chronological order, and PII absence.
- **Speaker Notes:** "We created standardized CSV templates to ensure that raw data is uniform and complies with our 23-column data dictionary."

---

### Slide 6: Preprocessing & Feature Engineering
- **Validation:** 16 rules enforcing formats, chronological order, capacity constraints, and PII filtering.
- **Feature Engineering (No Leakage):**
  - Time indicators (Morning/Afternoon, Day of Semester, Week of Year).
  - Shifted previous lecture attendance percentage (Lag-1).
  - Shifted rolling average of previous 3 lectures.
  - Expanding subject historical average (no lookahead).
- **Speaker Notes:** "Data leakage is a major risk in time-series forecasting. We strictly sort all data chronologically and apply shift operations so future data is never leaked into past training rows."

---

### Slide 7: Exploratory Data Analysis (EDA)
- **Valid lectures collected:** 18 (June 25 – August 7, 2026)
- **Class strength:** 80 enrolled students
- **Attendance range:** 10.0% – 75.0% | Mean: 38.75%
- **Band distribution:** 12 Low (<50%), 6 Medium (50–75%), **0 High (>75%)**
- ⚠️ **"High" attendance band was never observed in the collected data.**
- **Speaker Notes:** "The EDA revealed that attendance was predominantly low throughout the semester, with a mean of 38.75%. Critically, the High attendance class — above 75% — was never recorded. This is an important finding that directly affects our classification model."

---

### Slide 8: Machine Learning Pipelines
- **Regression (Target: Students_Present):**
  - Dummy Baseline, Linear Regression, Decision Tree, Random Forest, Gradient Boosting.
- **Classification (Target: Attendance_Band — Low/Medium only):**
  - Dummy Baseline, Logistic Regression, Decision Tree, Random Forest, SVM, k-NN.
- **Split:** Chronological 80/20 → 14 training rows, 4 test rows.
- **Speaker Notes:** "We construct sklearn Pipeline objects combining preprocessing and model steps. The chronological split is critical — random splits would leak future information into training."

---

### Slide 9: Experiment Results

#### Regression (Baseline MAE: 14.50)
| Model | MAE | Result |
|:--|--:|:--|
| Random Forest | 14.02 | Marginally better — EXPLORATORY ONLY |
| All others | >22.0 | Worse than baseline |

#### Classification (Baseline Accuracy: 0.50)
| Best Model | Accuracy | Result |
|:--|--:|:--|
| Logistic Regression | 0.50 | Ties baseline — INVALID for operational use |

- ⚠️ **4-row test set — results cannot establish generalization.**
- ⚠️ **High class (>75%) never appeared in training or test data.**
- **Speaker Notes:** "The honest finding is that with only 18 lectures and a 4-row test set, we cannot claim our models generalize reliably. Random Forest marginally beat the baseline in regression, but this is exploratory. No classification model beat the baseline at all."

---

### Slide 10: Streamlit Dashboard UI
- Premium dark-themed, glassmorphic layout.
- **Tab 1:** Historical analysis charts from cleaned attendance data.
- **Tab 2:** Prediction form with explicit model validity warnings:
  - Regression shows "Exploratory / Limited Data" warning.
  - Classification shows "Attendance band unavailable — historical baseline only."
  - Fallback prediction displayed: **Historical mean = 38.75% / ~31 students**.
- **Tab 3:** Ethics and privacy protocols.
- **Speaker Notes:** "The dashboard is honest about what the system can and cannot do. When the classifier does not beat the baseline, it clearly says so and defaults to the historical average instead of showing a false confident prediction."

---

### Slide 11: Limitations & Ethical Boundaries
1. **Small dataset (n=18):** Insufficient for statistically reliable ML.
2. **4-row test set:** No metric is statistically meaningful on 4 observations.
3. **High class unobserved:** Max attendance was 75.0% — the "High" band was never reached.
4. **Exploratory regression only:** Random Forest marginally beat baseline but cannot be called production-ready.
5. **Invalid classifier:** The classification model tied the dummy baseline and must not automate attendance-band decisions.
6. **Model usage policy:** Intended purely for scheduling insights, not student grading or disciplinary profiling.
- **Speaker Notes:** "We clearly state all limitations upfront. This is scientifically rigorous. Overstating model performance would be dishonest and potentially harmful if used for administrative decisions."

---

### Slide 12: Conclusion & Future Scope

**Conclusion:**
> The available dataset contained only 18 valid lecture observations. The regression experiment produced a small improvement over the historical-average baseline, but the test set contained only four observations, so the result is exploratory and cannot establish reliable generalization. The classification model did not outperform the dummy baseline and should not be used for operational decisions. More physically verified lecture records are required before deploying a reliable predictive system.

**What is complete:**
- Full validation, cleaning, and feature engineering pipeline ✅
- Model training with dummy baselines and chronological splits ✅
- Honest `is_valid` metadata in serialized models ✅
- Dashboard with fallback warnings ✅

**Next steps:**
- Continue logging lecture attendance each month.
- Re-run `python src/run_pipeline.py` after each new batch.
- When sufficient data exists, the `is_valid` flag will automatically upgrade to ML predictions.

- **Speaker Notes:** "In conclusion, this project delivers a scientifically honest, privacy-preserving prediction framework. The infrastructure is complete and will improve automatically as more data is collected. I am now open to your questions. Thank you."
