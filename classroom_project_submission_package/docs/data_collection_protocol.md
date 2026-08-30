# Data Collection Protocol

This document outlines the strict guidelines and step-by-step procedures for extracting, compiling, and formatting classroom attendance and academic schedule data for the ML prediction model.

## 1. Allowed Source Documents
All inputs must originate from official institutional records:
- **Master Timetable:** For lecture number, start/end times, assigned classroom, section, subject, and syllabus mapping.
- **Lab Register / Practical logbook:** For laboratory sessions, enrollment splits, and actual session-level present counts.
- **Faculty Attendance Register:** For verified, physically checked attendance records of individual class sessions.
- **Department Attendance Sheet:** Monthly summaries used to double-check raw lecture logs.
- **Academic Calendar:** For holiday scheduling, semester week numbers, and non-instructional days.
- **Examination Schedule:** For internal test weeks (midterms) and final exams.
- **Official Holiday Schedules:** For validating pre/post holiday status.

## 2. Steps for Data Entry
1. **Extraction:**
   - Locate the attendance register for the class division (e.g., MCA Final Year, Section A/B).
   - Locate the department timetables.
   - For each class session, extract the date, lecture slot, and aggregate student head counts.
2. **Aggregating:**
   - Sum the number of present students manually from the physical register row.
   - Look up the official total enrollment of that division (e.g., 60 or 205).
   - Calculate the attendance percentage: `(Students_Present / Total_Enrolled_Students) * 100`.
3. **Anonymization and Coding:**
   - Assign a sequential `Lecture_ID` starting from `LEC0001`.
   - Match the instructor's name to an encoded `Faculty_ID` (e.g., `F001`, `F002`). **Do not type faculty names.**
   - Leave student details out entirely. Do not copy individual checkmarks, student roll numbers, or personal notes.
4. **Validating:**
   - Cross-check that `Students_Present` does not exceed `Total_Enrolled_Students`.
   - Ensure the date conforms to `YYYY-MM-DD`.

## 3. Data Entry Auditing
- Verify that every cell in required columns is non-empty.
- Verify that previous lecture attendance and gaps are left blank if not known, or computed systematically via the feature engineering scripts.
