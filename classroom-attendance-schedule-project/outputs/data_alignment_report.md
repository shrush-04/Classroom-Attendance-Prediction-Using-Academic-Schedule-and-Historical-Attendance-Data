# Data Alignment Report

This report documents the transformations and mappings applied during the construction of the canonical raw dataset.

## 1. Source and Target Schemas

- **Source File:** `lecture_level_dataset.csv` merged with `attendance_stage1_final.csv`
- **Target File:** `data/raw/raw_lecture_attendance.csv`
- **Target Row Count:** 18 rows
- **Class Strength (Total_Enrolled_Students):** Officially set to **80** as confirmed by the user.

## 2. Column Mapping & Transformations

| Target Column | Source Column | Transformation |
|---|---|---|
| `Lecture_ID` | N/A | Generated sequentially: `LEC0001` to `LEC0018`. |
| `Date` | `Date` | Standardized to `YYYY-MM-DD` format. |
| `Day_of_Week` | `Day_of_Week` | Preserved values. |
| `Lecture_Number` | `Lecture_Number` | Preserved values. |
| `Start_Time` | `Start_Time` | Preserved values. |
| `End_Time` | `End_Time` | Preserved values. |
| `Subject` | `Subject` | Preserved values. |
| `Faculty_ID` | `Faculty_ID` | Preserved anonymized codes (e.g. `F_01+F_13`). |
| `Semester` | `Semester` | Standardized from `III` to `Third Semester`. |
| `Branch` | `Branch` | Preserved values (`MCA`). |
| `Section` | `Section` | Preserved values (`A+B`). |
| `Classroom` | `Classroom` | Preserved values. |
| `Total_Enrolled_Students` | `Total_Enrolled_Students` | Set to official class strength **80**. |
| `Students_Present` | `Students_Present_Count` | Preserved values. |
| `Attendance_Percentage` | `Attendance_Percentage` | Calculated: `(Students_Present / 80) * 100`. |
| `Previous_Lecture_Attendance_Percentage` | N/A | Set as `Not_Collected` to allow feature engineering pipeline calculation. |
| `Gap_Since_Previous_Lecture_Hours` | N/A | Set as `Not_Collected` to allow feature engineering pipeline calculation. |
| `Practical_Theory` | `Subject` | Set to `Practical` if subject contains "Practical" or "Lab", else `Theory`. |
| `Internal_Test_Week` | `Internal_Test_Week` | Preserved values or set to `0` where empty. |
| `Assignment_Due` | `Assignment_Due` | Preserved values or set to `0` where empty. |
| `Holiday_Before_After` | `Holiday_Before_After` | Preserved values or set to `None` where empty. |
| `Weather` | N/A | Set as `Not_Collected`. |
| `Special_Event` | N/A | Set as `Not_Collected`. |

## 3. Excluded Records Log

The following **1 record** was excluded from the canonical raw dataset because it was a stray/incomplete entry:

| Date | Day_of_Week | Subject | Students_Present | Reason |
|---|---|---|---|---|
| 11-08-2026 | Tuesday | DS and ML Practical | 1 | Stray/incomplete register log on holiday/exam day. Single time value, only 1 student present. |

