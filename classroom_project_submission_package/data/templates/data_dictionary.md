# Data Dictionary

This data dictionary defines the structure and rules for the raw lecture-wise attendance data collected for the prediction system.

| Column Name | Meaning | Data Type | Example Format | Status | Source Document | Validation Rule | Privacy Concern |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lecture_ID** | Unique identifier for each lecture session | String | `LEC0001` | **Required** | Generated | Matches regex `^LEC\d{4}$`, unique, non-null | None |
| **Date** | Date on which the class was conducted | Date | `YYYY-MM-DD` | **Required** | Academic Calendar / Register | Valid ISO date, chronological | None |
| **Day_of_Week** | Day name of the lecture | Categorical | `Monday` | **Required** | Calendar / Timetable | One of: `Monday` to `Saturday` | None |
| **Lecture_Number** | Period index of the day | Integer | `1` | **Required** | Timetable | Between `1` and `10` | None |
| **Start_Time** | Starting time of the lecture | Time | `09:00` | **Required** | Timetable | HH:MM format, < End_Time | None |
| **End_Time** | Ending time of the lecture | Time | `10:00` | **Required** | Timetable | HH:MM format, > Start_Time | None |
| **Subject** | Code or standardized title of course | String | `MCA301` or `Advanced Java` | **Required** | Syllabus / Register | Non-empty, consistent naming | None |
| **Faculty_ID** | Encoded identifier of the instructor | String | `F001` | **Required** | Department Sheet | Encoded format, e.g. `F\d{3}` | **No faculty names** |
| **Semester** | Academic semester of the class | String | `Third Semester` | **Required** | Syllabus / Timetable | Non-empty, consistent | None |
| **Branch** | Academic program/stream | String | `MCA` | **Required** | Department Register | Non-empty, consistent | None |
| **Section** | Division or section of the batch | String | `A` | **Required** | Department Register | Non-empty, consistent | None |
| **Classroom** | Room number or lab code | String | `CR101` or `Lab A` | **Required** | Timetable | Non-empty, consistent | None |
| **Total_Enrolled_Students** | Total strength of the division | Integer | `60` | **Required** | Department Sheet | Positive integer, e.g. 60 or 205 | None |
| **Students_Present** | Count of students present in lecture | Integer | `52` | **Required** | Attendance Register | Positive integer <= Enrolled | None |
| **Attendance_Percentage** | Percentage of students present | Float | `86.67` | **Required** | Calculated | `(Present / Enrolled) * 100` | None |
| **Previous_Lecture_Attendance_Percentage** | Attendance percentage of preceding class | Float | `83.33` | Optional | Shift operation (history) | Between `0` and `100` or blank | None |
| **Gap_Since_Previous_Lecture_Hours** | Time elapsed since last session in hours | Float | `24.0` or `2.0` | Optional | Derived from dates/times | Non-negative float or blank | None |
| **Practical_Theory** | Type of the class session | Categorical | `Theory` | **Required** | Timetable / Register | Either `Theory` or `Practical` | None |
| **Internal_Test_Week** | Whether the lecture is during test week | Binary | `0` (No) or `1` (Yes) | **Required** | Calendar / Exam Schedule | `0` or `1` | None |
| **Assignment_Due** | Whether an assignment was due that day | Binary | `0` (No) or `1` (Yes) | **Required** | Faculty Lesson Plan | `0` or `1` | None |
| **Holiday_Before_After** | Proximity to a scheduled holiday | Categorical | `Holiday_After` | **Required** | Academic Calendar | One of: `Holiday_Before`, `Holiday_After`, `Both`, `None` | None |
| **Weather** | Prevailing weather during lecture | Categorical | `Rainy` | Optional | Observations / Archive | One of: `Sunny`, `Rainy`, `Cloudy`, `Windy`, `Not_Collected` | None |
| **Special_Event** | Special institutional event presence | Categorical | `Symposium` | Optional | Academic Calendar | One of: `Symposium`, `Workshop`, `None`, `Not_Collected` | None |
