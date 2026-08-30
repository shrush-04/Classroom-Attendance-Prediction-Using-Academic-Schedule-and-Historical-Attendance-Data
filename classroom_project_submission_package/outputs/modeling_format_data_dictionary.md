# Data Dictionary: Modeling Format Dataset

**Dataset Path:** `data/processed/modeling_format_dataset.csv`
**Description:** A simplified, validated version of the cleaned lecture-level attendance dataset, structured specifically for model training and inference.
**Row Count:** 18 rows
**Order:** Chronological (sorted by Date and Time)

---

## Schema Information

| Column Name | Data Type | Description | Source Mapping | Allowed / Expected Values | Validation Rule |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Date** | String | Date of the lecture. | `Date` | `YYYY-MM-DD` | Must match regex `^\d{4}-\d{2}-\d{2}$`. |
| **Time** | String | Start time of the lecture. | `Start_Time` | `HH:MM` (24-hour format, e.g., `08:30`, `09:15`) | Must match regex `^\d{2}:\d{2}$`. |
| **Subject** | String | Name of the subject/course. | `Subject` | e.g. `Mobile Application Development`, `MAD Practical` | No names, roll numbers, or email addresses (PII check passed). |
| **Semester** | String | Academic semester. | `Semester` | e.g. `Third Semester` | Must be a valid semester name. |
| **Day_of_Week** | String | Day of the week. | `Day_of_Week` | `Monday` to `Sunday` | Must match standard days of the week. |
| **Previous_Attendance_Percentage** | Float / Blank | Attendance percentage of the previous lecture. | `Previous_Lecture_Attendance_Percentage` | `0.0` - `100.0` or empty (null) for the first lecture | Must be blank/NaN or between `0` and `100`. |
| **Internal_Test_Week** | Integer | Binary flag indicating if it is an internal test week. | `Internal_Test_Week` | `0` or `1` | Must be `0` or `1`. |
| **Holiday_Tomorrow** | String | Flag indicating if tomorrow is a holiday. | *Not collected in source data* | `Not_Collected` | Always set to `Not_Collected` (not collected in verified data). |
| **Total_Enrolled_Students** | Integer | Total number of students enrolled in the course. | `Total_Enrolled_Students` | Integer > 0 | Must be a positive integer. |
| **Students_Present** | Integer | Count of students present for the lecture. | `Students_Present` | Integer >= 0 | `Students_Present` <= `Total_Enrolled_Students`. |
| **Attendance_Percentage** | Float | Percentage of students present. | `Attendance_Percentage` | `0.0` - `100.0` | Calculated as `(Students_Present / Total_Enrolled_Students) * 100` (verified). |

---

## Validation Summary
The following constraints were programmatically verified upon dataset creation:
1. **PII check:** Confirmed that columns contain no email addresses, roll numbers, or personal names.
2. **Student count sanity check:** Confirmed `Students_Present <= Total_Enrolled_Students` for all rows.
3. **Attendance math verification:** Recalculated `Attendance_Percentage` and verified it matches actual values.
4. **Duplicate detection:** Verified no duplicate rows exist in the generated dataset.
5. **Format check:** Verified that all `Date` entries conform to `YYYY-MM-DD` and all `Time` entries conform to `HH:MM`.
