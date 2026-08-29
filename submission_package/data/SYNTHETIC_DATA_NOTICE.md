# SYNTHETIC DATA NOTICE

> This dataset is synthetic and was generated only for academic demonstration.
> It does not contain real student names, roll numbers, email IDs, or actual
> attendance records of identifiable students.

## Covered Files

| File | Students | Rows | Seed |
|------|----------|------|------|
| student_attendance.csv | STU0001-STU0060 (60) | 1,200 | 42 |
| student_attendance.xlsx | STU0001-STU0060 (60) | 1,200 | 42 |
| student_attendance_205_students.csv | STU0001-STU0205 (205) | 4,100 | 42 (original) + 200 (extended) |
| student_attendance_205_students.xlsx | STU0001-STU0205 (205) | 4,100 | 42 (original) + 200 (extended) |

## Generation Details

- **Method:** Python numpy.random.default_rng with fixed seeds — fully reproducible
- **Real information used:** Only non-identifying classroom parameters:
  - Original cohort: 60 students, Computer Engineering, Third Year, Fifth Semester
  - Extended cohort: +145 students, MCA, Final Year, Third Semester
- **NOT used at any stage:** Student names, roll numbers, college email IDs, biometric data,
  personal contact information, or any file containing real student lists
- **Student identifiers:** Anonymous synthetic codes only (STU0001-STU0205)
- **Mapping to real students:** NONE EXISTS. No mapping was created.
- **Purpose:** Undergraduate Data Science project demonstrating EDA, regression, and
  classification techniques on attendance data

## Privacy Compliance

This project follows a Privacy-by-Design approach:
1. Data minimization - no personal data collected or stored
2. Full anonymization - synthetic IDs only
3. No re-identification risk - no real-to-synthetic mapping exists
4. Transparent labeling - every file and notebook marks data as SYNTHETIC
5. Responsible reporting - conclusions explicitly note the synthetic nature of findings

---
*Last updated: 2026-08-20 | Project: Privacy-Preserving Synthetic Student Attendance Analysis*
