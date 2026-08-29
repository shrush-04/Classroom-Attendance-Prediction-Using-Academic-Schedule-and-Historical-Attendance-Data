# Dataset Dictionary
## student_attendance.csv / student_attendance.xlsx
### Privacy-Preserving Synthetic Student Attendance Dataset

> SYNTHETIC DATA: No real student information is present in this dataset.

---

| # | Column Name | Data Type | Example Value | Valid Range / Values | Purpose |
|---|-------------|-----------|--------------|----------------------|---------|
| 1 | Student_ID | String | STU0023 | STU0001 to STU0060 | Anonymous synthetic student identifier. Not linked to any real student. |
| 2 | Gender | String | Male | Male, Female, Other | Synthetic demographic attribute. Randomly assigned per student. |
| 3 | Age | Integer | 21 | 17 to 25 | Synthetic age. Realistic for third-year engineering students (19–23 in this dataset). |
| 4 | Department | String | Computer Engineering | Fixed: "Computer Engineering" | Academic department. Non-identifying classroom parameter. |
| 5 | Year | String | Third Year | Fixed: "Third Year" | Academic year. Non-identifying classroom parameter. |
| 6 | Semester | String | Fifth Semester | Fixed: "Fifth Semester" | Semester. Non-identifying classroom parameter. |
| 7 | Subject | String | Computer Networks | One of 5 fixed subject names | The subject for which the attendance record applies. |
| 8 | Total_Classes | Integer | 10 | 8 to 12 (positive integer) | Number of classes held in the attendance period for this subject. Always > 0. |
| 9 | Classes_Attended | Integer | 8 | 0 to Total_Classes | Number of classes the student attended in this period. Cannot exceed Total_Classes. |
| 10 | Previous_Attendance_Percentage | Float | 76.50 | 40.0 to 100.0 | Attendance percentage from a prior assessment period. Per student-subject combination. |
| 11 | Assignment_Score | Float | 65.4 | 0.0 to 100.0 | Score on assignments for this subject. Mildly correlated with study hours. |
| 12 | Internal_Marks | Float | 13.2 | 0.0 to 30.0 | Internal assessment marks (max 30). Weakly linked to attendance in this period. |
| 13 | Study_Hours_Per_Week | Float | 9.5 | 2.0 to 20.0 | Self-reported synthetic study hours per week. Stable per student across all records. |
| 14 | Medical_Leave_Days | Integer | 1 | 0 to 10 | Days of medical leave taken in this period. Non-negative. Poisson-distributed. |
| 15 | Travel_Distance_KM | Float | 14.3 | 0.5 to 60.0 | Distance from home to college in km. Stable per student. Exponentially distributed. |
| 16 | Previous_Exam_Score | Float | 58.7 | 0.0 to 100.0 | Score in a previous examination. Stable per student with small per-period noise. |
| 17 | Late_Count | Integer | 2 | 0 to 15 | Number of times the student was late to class in this period. Non-negative. |
| 18 | Online_Class_Attendance | Float | 68.0 | 0.0 to 100.0 | Percentage of online/virtual classes attended. Independent of in-person attendance. |
| 19 | Attendance_Percentage | Float | 80.00 | 0.0 to 100.0 | DERIVED: (Classes_Attended / Total_Classes) * 100, rounded to 2 decimal places. |
| 20 | Attendance_Status | String | Regular | Regular, Defaulter | DERIVED: "Regular" if Attendance_Percentage >= 75.0, else "Defaulter". Target variable for classification. |

---

## Subject Reference

| Subject Code (Internal) | Subject Name |
|------------------------|--------------|
| SUB01 | Data Structures & Algorithms |
| SUB02 | Database Management Systems |
| SUB03 | Computer Networks |
| SUB04 | Theory of Computation |
| SUB05 | Software Engineering |

---

## Derived Column Rules

### Attendance_Percentage
```
Attendance_Percentage = round((Classes_Attended / Total_Classes) * 100, 2)
```

### Attendance_Status
```
if Attendance_Percentage >= 75.0:
    Attendance_Status = "Regular"
else:
    Attendance_Status = "Defaulter"
```

---

## Dataset Structure

- **Total rows    :** 1,200
- **Total columns :** 20
- **Structure     :** 60 students x 5 subjects x 4 attendance periods
- **Random seed   :** 42 (fully reproducible)
- **Missing values:** 0

---

## Usage Notes

- `Attendance_Percentage` and `Attendance_Status` are the **target variables** for modelling.
- `Attendance_Percentage` is used for **regression**.
- `Attendance_Status` is used for **binary classification**.
- Features `Total_Classes`, `Classes_Attended`, `Previous_Attendance_Percentage`,
  `Assignment_Score`, `Internal_Marks`, `Study_Hours_Per_Week`, `Medical_Leave_Days`,
  `Travel_Distance_KM`, `Previous_Exam_Score`, `Late_Count`, `Online_Class_Attendance`
  are the **predictor features**.
- `Student_ID`, `Gender`, `Age`, `Department`, `Year`, `Semester`, `Subject`
  are **metadata / grouping** columns.

---
*Dictionary generated: 2026-08-20 | All data is SYNTHETIC.*
