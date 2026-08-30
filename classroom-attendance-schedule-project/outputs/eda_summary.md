# Exploratory Data Analysis Summary

This summary provides an overview of findings and patterns observed in the classroom attendance data.

> ⚠️ **Scientific Validity Notice:** This EDA is based on **18 lecture observations** only.
> All findings are descriptive. No inferential claims can be drawn from this sample size.

---

## Descriptive Statistics

|       |   Total_Enrolled_Students |   Students_Present |   Attendance_Percentage |
|:------|--------------------------:|-------------------:|------------------------:|
| count |                        18 |            18      |                 18      |
| mean  |                        80 |            31      |                 38.75   |
| std   |                         0 |            17.5934 |                 21.9918 |
| min   |                        80 |             8      |                 10      |
| 25%   |                        80 |            16      |                 20      |
| 50%   |                        80 |            29      |                 36.25   |
| 75%   |                        80 |            45.25   |                 56.5625 |
| max   |                        80 |            60      |                 75      |

---

## Attendance Band Distribution

| Band | Threshold | Lectures | % of Total |
|:--|:--|--:|--:|
| Low | < 50% | 12 | 66.7% |
| Medium | 50% – 75% | 6 | 33.3% |
| **High** | **> 75%** | **0** | **0%** |

> 🔴 **Critical Finding: The "High" attendance band (>75%) was never observed in any of the
> 18 recorded lectures.** The maximum attendance recorded was exactly 75.0%, which falls at the
> upper boundary of the "Medium" band. This means:
> - Any model predicting "High" attendance would be extrapolating beyond the observed data range.
> - The 3-class attendance band classification schema cannot be fully trained or validated.
> - Attendance in this semester was predominantly "Low" (67% of lectures).

---

## Key Findings

- **Total Lectures Logged:** 18 (2026-06-25 to 2026-08-07)
- **Class Strength:** 80 enrolled students
- **Overall Mean Attendance:** 38.75% (~31 students per lecture)
- **Maximum Attendance:** 75.00% (60 students) — never exceeded the Medium/High boundary
- **Minimum Attendance:** 10.00% (8 students)
- **Standard Deviation:** 22.0 percentage points — high variability relative to the mean
- **Historical Baseline (operational fallback):** 38.75% / ~31 students present

---

## Subjects Covered

- Mobile Application Development (Theory)
- MAD Practical

---

## Charts Generated

Detailed charts showing subject-wise, day-wise, slot-wise, and holiday-proximity attendance
distributions have been saved to `outputs/charts/`.
