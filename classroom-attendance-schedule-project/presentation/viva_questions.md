# Viva Questions and Answers

This document contains 45 comprehensive viva questions and answers prepared to help defend this project during the academic evaluation.

---

### Part 1: Data Collection & Schema (Q1 - Q10)

#### Q1: What is the main title and goal of your project?
**A:** The project title is *"Classroom Attendance Prediction Using Academic Schedule and Historical Attendance Data"*. The goal is to build a machine learning system that predicts aggregate classroom attendance for future lecture slots to assist department schedulers, while strictly preserving student privacy.

#### Q2: What department and class does this project focus on?
**A:** It focuses on the Department of Computer Applications (MCA), Final Year, Third Semester. The total enrolled class strength is 205 students (or the actual section strength).

#### Q3: What is the data granularity of your dataset?
**A:** The data granularity is "lecture-level" or "session-level". Each row in the dataset represents a single class session (typically 1 or 2 hours), not an individual student.

#### Q4: Why did you not use a public dataset?
**A:** Public datasets do not reflect the specific schedule, timetable structures, localized weather patterns, syllabus progressions, and holiday calendars of our institution. Using localized, original registers ensures the model yields actionable insights for our department.

#### Q5: What are the columns required in the raw attendance log?
**A:** There are 23 columns including: `Lecture_ID`, `Date`, `Day_of_Week`, `Lecture_Number`, `Start_Time`, `End_Time`, `Subject`, `Faculty_ID`, `Semester`, `Branch`, `Section`, `Classroom`, `Total_Enrolled_Students`, `Students_Present`, `Attendance_Percentage`, `Previous_Lecture_Attendance_Percentage`, `Gap_Since_Previous_Lecture_Hours`, `Practical_Theory`, `Internal_Test_Week`, `Assignment_Due`, `Holiday_Before_After`, `Weather`, and `Special_Event`.

#### Q6: Why did you encode the Faculty names as Faculty_ID (e.g. F001)?
**A:** This is done to preserve faculty privacy. Recording names is unnecessary for the model; encoding names allows us to capture the variation in attendance related to teaching schedules without identifying individual instructors.

#### Q7: How is the Attendance_Percentage column validated mathematically?
**A:** It is validated using the formula:  
$$\text{Attendance\_Percentage} = \left(\frac{\text{Students\_Present}}{\text{Total\_Enrolled\_Students}}\right) \times 100$$  
The validation script checks that this calculation matches the reported percentage within a small rounding tolerance.

#### Q8: What happens if optional fields (like Weather or Special_Event) are missing?
**A:** In accordance with institutional guidelines, we do not fabricate records. The missing values are left blank or logged as `Not_Collected` and documented.

#### Q9: What is the purpose of the Handwritten Logbook Template?
**A:** It provides a physical layout for department representatives to log aggregate attendance counts at the end of each session. This serves as the primary source before digital entry.

#### Q10: What is the format of the Lecture_ID?
**A:** It follows a strict string pattern matching `^LEC\d{4}$` (e.g. `LEC0001`, `LEC0002`).

---

### Part 2: Data Validation & Cleaning (Q11 - Q18)

#### Q11: What are the key checks performed by your validation script?
**A:** The script validates: schema columns, duplicate Lecture_IDs, Date format, Time format, chronological order, enrollment capacities (`Students_Present` <= `Total_Enrolled_Students`), non-negative counts, percentage formulas, missing required values, duplicate rows, categorical levels, subject names, section consistency, and PII presence.

#### Q12: How does your validation script verify that no student personal information is present?
**A:** It performs two checks:
1. **Schema Check:** Ensures no column names contain keywords like "name", "roll", "email", "phone", or "biometric".
2. **Content Check:** Scans string columns for email regex patterns or roll-number patterns.

#### Q13: What files does `validate_raw_data.py` produce?
**A:** It writes a markdown report `outputs/data_quality_report.md` and a text report `outputs/data_quality_report.txt`.

#### Q14: What is your policy on handling missing attendance values?
**A:** We do **not** automatically guess or impute missing attendance values in the raw dataset. If they are missing, they are left as null, documented, and handled by sklearn's imputer pipelines during ML training.

#### Q15: Why is checking chronological sorting important in data validation?
**A:** Our features are time-dependent (lags and rolling statistics). If data is not sorted chronologically, the shift operations will fetch values from incorrect time slots, corrupting historical features.

#### Q16: How does `clean_data.py` standardize category levels?
**A:** It strips leading/trailing whitespaces, standardizes text case (e.g., capitalizing Days of Week), converts times to HH:MM format, and maps empty cells in optional fields to `Not_Collected` or `None`.

#### Q17: What does the file `outputs/missing_values_audit.txt` record?
**A:** It records every missing value detected in optional fields, auditing the reason (such as optional administrative variables not logged at lecture time) to ensure data transparency.

#### Q18: What is the output file of the cleaning script?
**A:** The cleaned dataset is saved to `data/processed/cleaned_lecture_attendance.csv`.

---

### Part 3: Feature Engineering & Data Leakage (Q19 - Q28)

#### Q19: What is "data leakage" and how did you prevent it in your features?
**A:** Data leakage occurs when future information or target variables are used as input features. We prevented it by:
1. Sorting all data chronologically.
2. Shifting all target-derived features (e.g., using `shift(1)` for previous lecture attendance).
3. Using expanding historical metrics instead of future averages.

#### Q20: Explain the `Day_of_Semester` feature.
**A:** It represents the number of days elapsed since the first day of classes. It captures the overall semester timeline, helping the model learn if attendance decreases as the semester progresses.

#### Q21: What is the `Is_Morning` feature and how is it derived?
**A:** It is a binary feature. If the lecture's `Start_Time` is before 12:00 PM, `Is_Morning` is `1`; otherwise, it is `0`.

#### Q22: How is the `Days_Since_Last_Holiday` feature calculated?
**A:** The script compiles a list of all holiday dates (where `Holiday_Before_After` matches holiday tags) and, for each lecture row, calculates the difference in days from the current date to the most recent past holiday.

#### Q23: Is the `Week_Before_Exam` feature considered data leakage?
**A:** No. Institutional examination schedules are pre-planned and published at the start of the semester. Schedulers know exactly when exam weeks occur, so using this feature represents scheduled calendar data, not target leakage.

#### Q24: How do you compute the `Previous_Lecture_Attendance_Percentage` feature safely?
**A:** We group the cleaned dataset by `Section` and shift the `Attendance_Percentage` column by 1:  
`df.groupby('Section')['Attendance_Percentage'].shift(1)`. This ensures only the previous class's attendance is used.

#### Q25: What is `Consecutive_Lecture_Count`?
**A:** It is the count of lectures scheduled for a specific division on the same day. For example, if a section has 3 lectures scheduled on a Monday, the value is 3.

#### Q26: Explain the `Rolling_Average_Previous_3_Lectures` feature.
**A:** It computes the average attendance percentage of the past 3 lectures of the *same subject* and *same section*. It is calculated by applying a rolling window of size 3 to the shifted attendance percentages.

#### Q27: How is the `Subject_Historical_Average` computed?
**A:** It is the expanding cumulative mean of the shifted attendance percentage for each subject. It represents the historical baseline attendance rate for that course up to that point.

#### Q28: Where are the engineered features stored?
**A:** They are saved in `data/processed/feature_engineered_attendance.csv`, and their definitions are written in `outputs/feature_dictionary.md`.

---

### Part 4: Machine Learning Models & Evaluation (Q29 - Q38)

#### Q29: What are your primary and secondary regression targets?
**A:** The primary regression target is `Students_Present` (predicting the actual number of students attending). The secondary regression target is `Attendance_Percentage`.

#### Q30: What is the classification target, and what are the bands?
**A:** The classification target is `Attendance_Band`. The bands are:
- **Low:** Attendance Percentage < 50%
- **Medium:** 50% <= Attendance Percentage <= 75%
- **High:** Attendance Percentage > 75%

#### Q31: What features must be excluded from model inputs?
**A:** We exclude `Lecture_ID`, `Date`, the targets (`Students_Present`, `Attendance_Percentage`, `Attendance_Band`), and any variables that require current-class attendance information.

#### Q32: Why did you use a chronological train-test split instead of a random split?
**A:** Attendance data is chronological. A random split would cause temporal leakage (training on future lectures to predict past lectures). A chronological split (e.g. 80% earlier lectures for training, 20% later lectures for testing) simulates actual forecasting.

#### Q33: Name the regression models trained in your pipeline.
**A:** We train: Linear Regression, Decision Tree Regressor, Random Forest Regressor, and Gradient Boosting Regressor.

#### Q34: Name the classification models trained in your pipeline.
**A:** We train: Logistic Regression, Decision Tree Classifier, Random Forest Classifier, Support Vector Machine (SVC), and k-Nearest Neighbors (k-NN).

#### Q35: How did you implement preprocessing in Scikit-Learn?
**A:** We used a `ColumnTransformer` with two branches:
1. **Numerical features:** Processed using a pipeline containing `SimpleImputer(strategy='median')` and `StandardScaler()`.
2. **Categorical features:** Processed using a pipeline containing `SimpleImputer(strategy='constant')` and `OneHotEncoder(handle_unknown='ignore')`.

#### Q36: What metrics did you use to evaluate regression models?
**A:** Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), Mean Absolute Percentage Error (MAPE), and R-squared ($R^2$) score.

#### Q37: What metrics did you use to evaluate classification models?
**A:** Accuracy, Precision, Recall, F1-score, and ROC-AUC.

#### Q38: Where are the trained model files saved?
**A:** In the `models/` directory: `best_present_count_model.joblib` and `best_attendance_band_model.joblib`.

---

### Part 5: UI, Ethics & Limitations (Q39 - Q45)

#### Q39: What tool did you use to build the dashboard, and what are its sections?
**A:** We used **Streamlit**. It has three sections:
1. **Historical Analysis & Data Status:** Displays dataset summary and trends.
2. **Predictive Model Inference:** An interactive prediction form.
3. **Collection Protocols & Ethics:** Details privacy rules and disclaimers.

#### Q40: What happens in the Streamlit app if model training files are missing?
**A:** The app disables predictions and displays: *"Train the model after adding validated original attendance data."*

#### Q41: How is the "Low-attendance risk indicator" determined during prediction?
**A:** It is marked as **High Risk** if the predicted attendance percentage is less than 50% or if the predicted attendance band is "Low". Otherwise, it is marked as "Normal".

#### Q42: What is your project's policy on student names and roll numbers?
**A:** Student names, roll numbers, emails, and biometrics are strictly excluded. The dataset contains only aggregate lecture-level records.

#### Q43: What are the main limitations of your predictive model?
**A:** 
1. It cannot capture un-loggable external factors (e.g. transportation strikes, weather volatility).
2. For the first week of the term, lag indicators default to historical means.
3. Timetable swaps must be logged manually.

#### Q44: What ethical guidelines govern the use of this project?
**A:** It is designed solely as a resource planning tool to help the department optimize class scheduling. It is **not** to be used for profiling individual student grades or implementing disciplinary actions.

#### Q45: How can a user reproduce your project results?
**A:** By placing the validated original CSV in `data/raw/raw_lecture_attendance.csv` and running the orchestrator script: `python src/run_pipeline.py`.
