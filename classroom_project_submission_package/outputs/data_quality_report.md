# Classroom Attendance Data Validation Report

- **Data Row Count:** 18
- **Validation Status:** PASSED
- **Error Counts:** 0 rule violations

## Validation Rules Checklist

| Rule / Check | Status | Description |
| :--- | :--- | :--- |
| Required Columns | ✅ PASS | All required columns are present. |
| Lecture_ID Validation | ✅ PASS | Lecture_ID format and uniqueness are valid. |
| Date Format | ✅ PASS | All dates are in correct YYYY-MM-DD format. |
| Time Format | ✅ PASS | Time formats are valid. |
| Chronological Order | ✅ PASS | Data is chronologically sorted. |
| Enrollment Capacity | ✅ PASS | Present counts are less than or equal to Enrolled counts. |
| Non-negative Counts | ✅ PASS | All student counts are non-negative. |
| Attendance Percentage Formula | ✅ PASS | All attendance percentages match (Present/Enrolled) * 100. |
| Missing Values in Required Columns | ✅ PASS | No missing values in required columns. |
| Duplicate Rows | ✅ PASS | No duplicate rows found. |
| Categorical Values | ✅ PASS | All categorical fields contain valid levels. |
| Subject Consistency | ✅ PASS | Subjects recorded (2 types): ['Mobile Application Development', 'MAD Practical'] |
| Section Consistency | ✅ PASS | Sections recorded: ['A+B'] |
| Faculty_ID Consistency | ✅ PASS | Faculty_IDs are valid. Faculty count: 2 |
| No PII Columns | ✅ PASS | No personal identifier columns (names, emails, rolls) exist in schema. |
| No PII Data Values | ✅ PASS | No student names, roll numbers, or email values found in cell content. |
