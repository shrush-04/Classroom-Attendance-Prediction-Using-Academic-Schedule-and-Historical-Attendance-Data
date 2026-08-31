# Classroom Attendance Data Validation Report

- **Data Row Count:** 81
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
| Subject Consistency | ✅ PASS | Subjects recorded (10 types): ['Mobile Application Development', 'Data Science and Machine Learning', 'Principles of Cloud Management and Security', 'Software Testing and Quality Assurance', 'Innovation and Entrepreneurship Development', 'STQA Practical', 'DS and ML Practical', 'Industry Readiness Program', 'Mini Project', 'MAD Practical'] |
| Section Consistency | ✅ PASS | Sections recorded: ['A+B'] |
| Faculty_ID Consistency | ✅ PASS | Faculty_IDs are valid. Faculty count: 9 |
| No PII Columns | ✅ PASS | No personal identifier columns (names, emails, rolls) exist in schema. |
| No PII Data Values | ✅ PASS | No student names, roll numbers, or email values found in cell content. |
