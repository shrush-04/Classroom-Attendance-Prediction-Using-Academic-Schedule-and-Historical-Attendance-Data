# Exploratory Data Analysis (EDA) Summary Report
**Project:** Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System  
**Dataset Version:** Validated 205-Student Extended Dataset (`data/student_attendance_205_students.csv`)  
**Report Generated:** August 22, 2026

---

## 1. Executive Summary
This report summarizes the results of the Exploratory Data Analysis (EDA) conducted on the validated student attendance dataset. The dataset contains **4,100 records** representing **205 unique students** across two departments (Computer Engineering and MCA) and five subjects. The overall objective is to analyze historical attendance patterns and key correlates to prepare the data for predictive machine learning models.

---

## 2. Basic Dataset Properties
* **Total Records (Rows):** 4,100
* **Features (Columns):** 21
* **Missing Cells:** 0 (Fully clean dataset)
* **Duplicate Rows:** 0 (Unique records check passed)
* **Student ID Range:** `STU0001` to `STU0205` (exactly 205 students, 20 records per student)

---

## 3. Key Statistical Findings

### A. Attendance Distribution Metrics
* **Average Attendance:** 68.67%
* **Minimum Attendance:** 0.00%
* **Maximum Attendance:** 100.00%
* **Median Attendance:** 70.00%
* **Defaulter Count (Attendance < 75%):** 2,266 rows (55.27%)
* **Regular Count (Attendance >= 75%):** 1,834 rows (44.73%)

*Observation:* The distribution shows a peak around 70-80% attendance. A significant portion of records (55.27%) fall below the 75% threshold, designating them as "Defaulter" status according to academic criteria.

### B. Segment-wise Comparison

#### Department-wise Attendance
| Department | Record Count | Mean Attendance (%) | Median Attendance (%) |
| :--- | :--- | :--- | :--- |
| **Computer Engineering** | 1,200 | 70.89% | 72.73% |
| **MCA** | 2,900 | 67.75% | 66.67% |

*Observation:* Computer Engineering records show a slightly higher mean attendance rate (70.89%) compared to MCA records (67.75%).

#### Subject-wise Attendance
| Subject | Record Count | Mean Attendance (%) | Median Attendance (%) |
| :--- | :--- | :--- | :--- |
| **Software Engineering** | 820 | 69.12% | 70.00% |
| **Computer Networks** | 820 | 68.86% | 71.37% |
| **Data Structures & Algorithms** | 820 | 68.54% | 70.00% |
| **Theory of Computation** | 820 | 68.43% | 70.00% |
| **Database Management Systems** | 820 | 68.38% | 66.67% |

*Observation:* Average attendance is highly uniform across all five subjects, with less than a 1% variation between the highest (Software Engineering: 69.12%) and lowest (Database Management Systems: 68.38%).

#### Year and Semester-wise Attendance
| Year | Semester | Record Count | Mean Attendance (%) | Median Attendance (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Third Year** | **Fifth Semester** | 1,200 | 70.89% | 72.73% |
| **Final Year** | **Third Semester** | 2,900 | 67.75% | 66.67% |

*Observation:* Third-year student records (Fifth Semester) show a slightly higher attendance level compared to final-year student records (Third Semester).

---

## 4. Key Feature Correlations with Attendance

The Pearson correlation coefficients between numerical features and `Attendance_Percentage` are as follows:

| Feature | Correlation Coefficient | Strength & Direction |
| :--- | :--- | :--- |
| `Classes_Attended` | `0.90` | Very Strong Positive (Math relation) |
| `Previous_Attendance_Percentage` | `0.72` | Strong Positive |
| `Internal_Marks` | `0.67` | Strong Positive |
| `Study_Hours_Per_Week` | `0.61` | Moderate-to-Strong Positive |
| `Previous_Exam_Score` | `0.59` | Moderate-to-Strong Positive |
| `Assignment_Score` | `0.37` | Moderate Positive |
| `Travel_Distance_KM` | `0.04` | No Correlation |
| `Late_Count` | `0.01` | No Correlation |
| `Online_Class_Attendance` | `-0.00` | No Correlation |
| `Medical_Leave_Days` | `-0.02` | No Correlation |
| `Age` | `-0.07` | Negligible Negative |

### Correlation Insights:
1. **Academic Connection:** Features representing previous academic behaviors (`Previous_Attendance_Percentage` at `0.72` and `Previous_Exam_Score` at `0.59`) and in-semester performance (`Internal_Marks` at `0.67` and `Assignment_Score` at `0.37`) are highly correlated with current attendance.
2. **Engagement Metric:** Student effort measured in `Study_Hours_Per_Week` has a strong positive correlation (`0.61`) with attendance.
3. **Weak Constraints:** Logistical or personal factors like `Travel_Distance_KM`, `Late_Count`, and `Medical_Leave_Days` show correlation coefficients close to zero, suggesting that in this synthetic model, these variables do not systematically influence student attendance.

---

## 5. Methodological Caution: Correlation vs. Causation

It is crucial to emphasize that **correlation does not imply causation**:
* **Direction of Influence:** A positive correlation of `0.67` between `Internal_Marks` and `Attendance_Percentage` indicates that students with higher attendance generally secure better internal marks. However, we cannot conclude that high attendance *causes* better internal marks, or vice-versa. 
* **Confounding Variables:** Both variables could be driven by a third, unobserved factor such as student motivation, diligence, or support systems. A motivated student is likely to both attend classes regularly and score well on internal assessments.
* **Synthetic Generation Context:** These statistical relationships are modeled by fixed mathematical rules programmed during synthetic data generation. In a real-world scenario, the causal pathways are far more complex and circular.

---

## 6. Generated Visualizations

All generated visualizations are saved in the project directory under `outputs/charts/`:

1. **`attendance_distribution.png`**: KDE-overlay histogram showing overall attendance frequency distribution, highlighting the 75% default line.
2. **`regular_defaulter_count.png`**: Bar chart showing the split between Regular (1,834) and Defaulter (2,266) records.
3. **`subject_wise_attendance.png`**: Boxplot showing attendance distribution across all 5 subjects.
4. **`attendance_by_period.png`**: Boxplot comparing attendance percentages across daily class periods (`Period_1` to `Period_4`).
5. **`study_hours_vs_attendance.png`**: Scatter plot showing the positive trend line of weekly study hours against attendance percentage.
6. **`internal_marks_vs_attendance.png`**: Scatter plot of internal marks versus attendance, demonstrating a clear upward trend.
7. **`medical_leave_vs_attendance.png`**: Boxplot showing attendance distribution mapped to different values of medical leave days.
8. **`late_count_vs_attendance.png`**: Scatter plot demonstrating the absence of any linear relationship between late counts and attendance.
9. **`correlation_heatmap.png`**: Lower-triangular Pearson correlation matrix heatmap visualizing associations between all numeric columns.
