"""
generate_dataset.py
===================
Generates a fully SYNTHETIC student attendance dataset for academic demonstration.

IMPORTANT NOTICE
----------------
This script does NOT read, import, or access any real student data, roll numbers,
names, email IDs, or private files of any kind.
All records are computer-generated using random number generation seeded at 42.
The output is labelled SYNTHETIC throughout.

Dataset Parameters (non-identifying classroom facts used as statistical inputs):
  - Students      : 60 (anonymous IDs: STU0001 - STU0060)
  - Subjects      : 5
  - Periods       : 4 per student-subject combination (e.g., 4 assessment weeks/blocks)
  - Total rows    : >= 1000  (60 x 5 x 4 = 1200 rows)
  - Department    : Computer Engineering
  - Year/Semester : Third Year, Fifth Semester
  - Attendance range : ~50% to ~98%  |  Mean: ~78%
"""

import numpy as np
import pandas as pd
import os

# ── Reproducibility ──────────────────────────────────────────────────────────
RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)

# ── Constants ─────────────────────────────────────────────────────────────────
NUM_STUDENTS    = 60
NUM_PERIODS     = 4          # attendance periods / assessment blocks per subject

SUBJECTS = [
    "Data Structures & Algorithms",
    "Database Management Systems",
    "Computer Networks",
    "Theory of Computation",
    "Software Engineering",
]

DEPARTMENT     = "Computer Engineering"
YEAR_LABEL     = "Third Year"
SEMESTER_LABEL = "Fifth Semester"

# Each period has a slightly different total classes count (realistic)
PERIOD_CLASSES = [8, 9, 10, 11, 12]     # possible classes per period block
ATTENDANCE_THRESHOLD = 75.0

# ── Step 1: Generate stable per-student base attributes ──────────────────────

student_ids = [f"STU{str(i).zfill(4)}" for i in range(1, NUM_STUDENTS + 1)]

ages = rng.integers(19, 24, size=NUM_STUDENTS)

gender_choices = rng.choice(
    ["Male", "Female", "Other"],
    size=NUM_STUDENTS,
    p=[0.55, 0.43, 0.02]
)

# Per-student latent attendance tendency (0.50 to 0.99)
# Beta distribution creates realistic spread — most students are mid-range
base_tendency = rng.beta(a=4.0, b=1.8, size=NUM_STUDENTS)
base_tendency = np.clip(base_tendency, 0.50, 0.99)

# Study hours per week: stable per student, mildly correlated with tendency
study_hours = np.round(
    3.0 + base_tendency * 14.0 + rng.normal(0, 1.5, size=NUM_STUDENTS), 1
)
study_hours = np.clip(study_hours, 2.0, 20.0)

# Travel distance in KM: stable per student, independent
travel_km = np.round(
    rng.exponential(scale=10.0, size=NUM_STUDENTS) + 0.5, 1
)
travel_km = np.clip(travel_km, 0.5, 60.0)

# Previous exam score: stable per student
prev_exam_base = np.round(
    30.0 + base_tendency * 55.0 + rng.normal(0, 8, size=NUM_STUDENTS), 1
)
prev_exam_base = np.clip(prev_exam_base, 0.0, 100.0)

# ── Step 2: Generate rows: student x subject x period ────────────────────────

records = []

for s_idx, s_id in enumerate(student_ids):
    tendency = base_tendency[s_idx]

    for subject in SUBJECTS:
        # Previous attendance is stable per student-subject (before this semester)
        prev_att_pct = round(float(np.clip(
            tendency * 100.0 + rng.normal(0, 7), 40.0, 100.0
        )), 2)

        # Assignment score: per student-subject, mild study hours link
        assignment_score = round(float(np.clip(
            18.0 + study_hours[s_idx] * 3.2 + rng.normal(0, 10), 0.0, 100.0
        )), 1)

        for period_num in range(1, NUM_PERIODS + 1):
            # Total classes in this period
            total_classes = int(rng.choice(PERIOD_CLASSES))

            # Classes attended: noisy around tendency, each period independent
            mean_attend = tendency * total_classes
            std_attend  = max(0.5, total_classes * 0.12)
            attended    = int(np.round(rng.normal(loc=mean_attend, scale=std_attend)))
            attended    = int(np.clip(attended, 0, total_classes))

            att_pct    = round((attended / total_classes) * 100, 2)
            att_status = "Regular" if att_pct >= ATTENDANCE_THRESHOLD else "Defaulter"

            # Internal marks: 0–30, per period, weakly linked to attendance
            internal_marks = round(float(np.clip(
                att_pct * 0.18 + rng.normal(0, 4.0), 0.0, 30.0
            )), 1)

            # Medical leave: Poisson, per period
            medical_leave = int(np.clip(rng.poisson(lam=1.0), 0, 10))

            # Late count: Poisson, per period
            late_count = int(np.clip(rng.poisson(lam=1.8), 0, 15))

            # Online class attendance %: independent per period
            online_att = round(float(np.clip(
                rng.normal(loc=70.0, scale=16.0), 0.0, 100.0
            )), 1)

            # Previous exam score: per student, with small period-level noise
            prev_exam = round(float(np.clip(
                prev_exam_base[s_idx] + rng.normal(0, 3), 0.0, 100.0
            )), 1)

            records.append({
                "Student_ID"                    : s_id,
                "Gender"                        : gender_choices[s_idx],
                "Age"                           : int(ages[s_idx]),
                "Department"                    : DEPARTMENT,
                "Year"                          : YEAR_LABEL,
                "Semester"                      : SEMESTER_LABEL,
                "Subject"                       : subject,
                "Total_Classes"                 : total_classes,
                "Classes_Attended"              : attended,
                "Previous_Attendance_Percentage": prev_att_pct,
                "Assignment_Score"              : assignment_score,
                "Internal_Marks"                : internal_marks,
                "Study_Hours_Per_Week"          : float(study_hours[s_idx]),
                "Medical_Leave_Days"            : medical_leave,
                "Travel_Distance_KM"            : float(travel_km[s_idx]),
                "Previous_Exam_Score"           : prev_exam,
                "Late_Count"                    : late_count,
                "Online_Class_Attendance"       : online_att,
                "Attendance_Percentage"         : att_pct,
                "Attendance_Status"             : att_status,
            })

# ── Step 3: Build DataFrame ───────────────────────────────────────────────────

df = pd.DataFrame(records)

print("=" * 58)
print("  SYNTHETIC DATASET GENERATION — SUMMARY")
print("=" * 58)
print(f"  Total rows      : {len(df)}")
print(f"  Total columns   : {len(df.columns)}")
print(f"  Unique students : {df['Student_ID'].nunique()}")
print(f"  Unique subjects : {df['Subject'].nunique()}")
print(f"  Periods per S×S : {NUM_PERIODS}")
print("=" * 58)
print("\nAttendance_Status distribution:")
print(df["Attendance_Status"].value_counts().to_string())
print("\nAttendance_Percentage descriptive stats:")
print(df["Attendance_Percentage"].describe().round(2).to_string())

# ── Step 4: Save CSV and Excel ────────────────────────────────────────────────

os.makedirs("data", exist_ok=True)

csv_path  = os.path.join("data", "student_attendance.csv")
xlsx_path = os.path.join("data", "student_attendance.xlsx")

df.to_csv(csv_path, index=False)
print(f"\n[SAVED] {csv_path}  ({os.path.getsize(csv_path):,} bytes)")

df.to_excel(xlsx_path, index=False, engine="openpyxl")
print(f"[SAVED] {xlsx_path}  ({os.path.getsize(xlsx_path):,} bytes)")

print("\n[DONE] All data is SYNTHETIC. No real student records were used.")
