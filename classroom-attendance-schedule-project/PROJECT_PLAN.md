# Academic Project Plan

## 1. Problem Statement
Maintaining consistent classroom attendance is vital for student success, especially in professional programs like MCA. Identifying future low-attendance classes allows department heads to optimize timetable scheduling, prevent class voids, and plan academic events more effectively. 
However, typical prediction systems track student-level files, raising severe privacy issues and violating institutional data ethics. This project solves this conflict by using **Privacy by Design**—constructing a predictive model based purely on **aggregate lecture-level metadata** (timetable coordinates, exam calendars, historical lags) rather than tracking individual students.

## 2. Project Objectives
1. **Develop templates & guidelines** for secure, privacy-preserving attendance aggregation.
2. **Implement validation & pipeline scripts** to parse, clean, and enrich schedule logs.
3. **Engineers leakage-free historical variables** (lags, rolling averages, Expanding averages).
4. **Train multiple regression and classification pipelines** to predict `Students_Present` and `Attendance_Band`.
5. **Construct a high-fidelity dashboard** to visualize historical trends and input parameters for future slot predictions.

## 3. Scope & Parameters
- **Target Audience:** MCA Final Year (Semester III)
- **Data Granularity:** One row per scheduled lecture slot.
- **Primary Target:** Students Present (regression).
- **Secondary Targets:** Attendance Percentage (regression) and Attendance Band (Low <50%, Medium 50-75%, High >75% classification).
- **Class Strength Parameters:** 205 students or specific batch strength.

## 4. Work Breakdown Structure (WBS)
- **Phase 1: Administrative Safeguards & Protocols:** Design Excel/CSV schemas, handwritten log templates, and privacy policies.
- **Phase 2: Validation & ETL Code:** Write scripts to detect PII leakage and validate logic bounds.
- **Phase 3: Preprocessing & Feature Engineering:** Code shifted lag calculations and chronological splits to prevent test-set data leakage.
- **Phase 4: ML Training & Evaluation:** Develop and compare regression (Linear, Tree, Random Forest, GBR) and classification (Logistic, Tree, Random Forest, SVM, KNN) pipelines.
- **Phase 5: User Interface:** Build a dark-themed interactive Streamlit application.
- **Phase 6: Reporting & Thesis:** Assemble thesis content, viva preparations, and audits.
