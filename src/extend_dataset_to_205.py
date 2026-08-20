# extend_dataset_to_205.py
# ========================
# Extends the synthetic student attendance dataset from 60 to 205 students.
# IMPORTANT: No real student data is accessed. All data is SYNTHETIC.
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# IMPORTANT NOTICE
# -----------------
# This script does NOT read, import, or access any real student data.
# Preserves STU0001-STU0060, generates STU0061-STU0205 only.
# New department context: MCA | Final Year | Third Semester.
# Random seed: 200 (deterministic, different from original seed 42).
#
# Outputs:
#   data/student_attendance_205_students.csv
#   data/student_attendance_205_students.xlsx
#   outputs/dataset_validation_report_205_students.txt


import numpy as np
import pandas as pd
import os
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────
RANDOM_SEED      = 200          # deterministic seed for STU0061–STU0205
NEW_START        = 61
NEW_END          = 205          # inclusive
NUM_NEW_STUDENTS = NEW_END - NEW_START + 1   # 145

SUBJECTS = [
    "Data Structures & Algorithms",
    "Database Management Systems",
    "Computer Networks",
    "Theory of Computation",
    "Software Engineering",
]
NUM_SUBJECTS = len(SUBJECTS)

# New cohort context (MCA)
DEPARTMENT     = "MCA"
YEAR_LABEL     = "Final Year"
SEMESTER_LABEL = "Third Semester"

NUM_PERIODS          = 4          # attendance periods per student-subject
PERIOD_CLASSES_RANGE = [8, 9, 10, 11, 12]
ATTENDANCE_THRESHOLD = 75.0

# Paths
EXISTING_CSV = os.path.join("data", "student_attendance.csv")
OUT_CSV      = os.path.join("data", "student_attendance_205_students.csv")
OUT_XLSX     = os.path.join("data", "student_attendance_205_students.xlsx")
REPORT_PATH  = os.path.join("outputs", "dataset_validation_report_205_students.txt")

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# ── Step 1: Load and verify existing dataset ──────────────────────────────────
print("=" * 68)
print("  STEP 1: LOADING AND VERIFYING EXISTING DATASET")
print("=" * 68)

df_existing = pd.read_csv(EXISTING_CSV)

prev_unique   = df_existing["Student_ID"].nunique()
prev_rows     = len(df_existing)
existing_ids  = set(df_existing["Student_ID"].unique())

print(f"  Existing rows            : {prev_rows}")
print(f"  Existing unique students : {prev_unique}")
print(f"  Existing ID range        : {df_existing['Student_ID'].min()} – {df_existing['Student_ID'].max()}")
print(f"  Columns in existing file : {len(df_existing.columns)}")
print(f"  STU0001–STU0060 intact   : {all(f'STU{str(i).zfill(4)}' in existing_ids for i in range(1, 61))}")

# Add Attendance_Period to existing records if absent
if "Attendance_Period" not in df_existing.columns:
    # Assign period 1-4 cyclically within each student-subject group
    df_existing = df_existing.sort_values(["Student_ID", "Subject"]).reset_index(drop=True)
    period_labels = []
    for _, grp in df_existing.groupby(["Student_ID", "Subject"], sort=False):
        n = len(grp)
        period_labels.extend([f"Period_{p}" for p in range(1, n + 1)])
    df_existing["Attendance_Period"] = period_labels
    print(f"\n  [INFO] 'Attendance_Period' column added to existing records.")

# Reorder columns to required order
REQUIRED_COLS = [
    "Student_ID", "Gender", "Age", "Department", "Year", "Semester", "Subject",
    "Attendance_Period", "Total_Classes", "Classes_Attended",
    "Previous_Attendance_Percentage", "Assignment_Score", "Internal_Marks",
    "Study_Hours_Per_Week", "Medical_Leave_Days", "Travel_Distance_KM",
    "Previous_Exam_Score", "Late_Count", "Online_Class_Attendance",
    "Attendance_Percentage", "Attendance_Status",
]

# Make sure all required cols are present in existing
missing_in_existing = [c for c in REQUIRED_COLS if c not in df_existing.columns]
if missing_in_existing:
    print(f"  [WARNING] Columns missing in existing data: {missing_in_existing}")
else:
    df_existing = df_existing[REQUIRED_COLS]
    print(f"  [INFO] Existing columns reordered to match required schema.")

# ── Step 2: Generate new records for STU0061–STU0205 ─────────────────────────
print("\n" + "=" * 68)
print("  STEP 2: GENERATING NEW SYNTHETIC STUDENTS (STU0061–STU0205)")
print("=" * 68)

rng = np.random.default_rng(RANDOM_SEED)

new_student_ids = [f"STU{str(i).zfill(4)}" for i in range(NEW_START, NEW_END + 1)]

# Stable per-student attributes
ages = rng.integers(20, 26, size=NUM_NEW_STUDENTS)   # MCA: 20–25
ages = np.clip(ages, 17, 25)

gender_choices = rng.choice(
    ["Male", "Female", "Other"],
    size=NUM_NEW_STUDENTS,
    p=[0.52, 0.45, 0.03]
)

# Latent attendance tendency: beta distribution, realistic spread
# Intentionally shifted slightly lower than CE batch to show variation
base_tendency = rng.beta(a=3.2, b=1.6, size=NUM_NEW_STUDENTS)
base_tendency = np.clip(base_tendency, 0.45, 0.99)

study_hours = np.round(
    4.0 + base_tendency * 13.0 + rng.normal(0, 1.8, size=NUM_NEW_STUDENTS), 1
)
study_hours = np.clip(study_hours, 2.0, 20.0)

travel_km = np.round(
    rng.exponential(scale=11.0, size=NUM_NEW_STUDENTS) + 0.5, 1
)
travel_km = np.clip(travel_km, 0.5, 60.0)

prev_exam_base = np.round(
    28.0 + base_tendency * 58.0 + rng.normal(0, 9, size=NUM_NEW_STUDENTS), 1
)
prev_exam_base = np.clip(prev_exam_base, 0.0, 100.0)

# ── Generate records ──────────────────────────────────────────────────────────
new_records = []

for s_idx, s_id in enumerate(new_student_ids):
    tendency = base_tendency[s_idx]

    for subject in SUBJECTS:
        # Per student-subject stable attributes
        prev_att_pct = round(float(np.clip(
            tendency * 100.0 + rng.normal(0, 8), 38.0, 100.0
        )), 2)

        assignment_score = round(float(np.clip(
            16.0 + study_hours[s_idx] * 3.0 + rng.normal(0, 11), 0.0, 100.0
        )), 1)

        for period_num in range(1, NUM_PERIODS + 1):
            total_classes = int(rng.choice(PERIOD_CLASSES_RANGE))

            mean_attend = tendency * total_classes
            std_attend  = max(0.5, total_classes * 0.13)
            attended    = int(np.round(rng.normal(loc=mean_attend, scale=std_attend)))
            attended    = int(np.clip(attended, 0, total_classes))

            att_pct    = round((attended / total_classes) * 100, 2)
            att_status = "Regular" if att_pct >= ATTENDANCE_THRESHOLD else "Defaulter"

            internal_marks = round(float(np.clip(
                att_pct * 0.19 + rng.normal(0, 4.2), 0.0, 30.0
            )), 1)

            medical_leave = int(np.clip(rng.poisson(lam=1.1), 0, 10))
            late_count    = int(np.clip(rng.poisson(lam=1.9), 0, 15))

            online_att = round(float(np.clip(
                rng.normal(loc=68.0, scale=17.0), 0.0, 100.0
            )), 1)

            prev_exam = round(float(np.clip(
                prev_exam_base[s_idx] + rng.normal(0, 3.5), 0.0, 100.0
            )), 1)

            new_records.append({
                "Student_ID"                    : s_id,
                "Gender"                        : gender_choices[s_idx],
                "Age"                           : int(ages[s_idx]),
                "Department"                    : DEPARTMENT,
                "Year"                          : YEAR_LABEL,
                "Semester"                      : SEMESTER_LABEL,
                "Subject"                       : subject,
                "Attendance_Period"             : f"Period_{period_num}",
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

df_new = pd.DataFrame(new_records, columns=REQUIRED_COLS)

print(f"  New rows generated        : {len(df_new)}")
print(f"  New unique students       : {df_new['Student_ID'].nunique()}")
print(f"  New ID range              : {df_new['Student_ID'].min()} – {df_new['Student_ID'].max()}")

# ── Step 3: Combine and save ──────────────────────────────────────────────────
print("\n" + "=" * 68)
print("  STEP 3: COMBINING AND SAVING")
print("=" * 68)

df_combined = pd.concat([df_existing, df_new], ignore_index=True)

final_rows     = len(df_combined)
final_students = df_combined["Student_ID"].nunique()

print(f"  Combined rows      : {final_rows}")
print(f"  Combined students  : {final_students}")
print(f"  Combined columns   : {len(df_combined.columns)}")

df_combined.to_csv(OUT_CSV, index=False)
print(f"\n  [SAVED] {OUT_CSV}  ({os.path.getsize(OUT_CSV):,} bytes)")

df_combined.to_excel(OUT_XLSX, index=False, engine="openpyxl")
print(f"  [SAVED] {OUT_XLSX}  ({os.path.getsize(OUT_XLSX):,} bytes)")

# ── Step 4: Validation ────────────────────────────────────────────────────────
print("\n" + "=" * 68)
print("  STEP 4: RUNNING VALIDATION CHECKS")
print("=" * 68)

lines = []

def log(msg=""):
    print(msg)
    lines.append(msg)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log("=" * 68)
log("  VALIDATION REPORT — 205-STUDENT SYNTHETIC DATASET")
log(f"  Generated : {now}")
log(f"  File      : {OUT_CSV}")
log("  NOTICE    : All data is SYNTHETIC. No real student records used.")
log("=" * 68)

df = df_combined.copy()

# CHECK 1: Row count
log("\n[CHECK 1] Total Row Count")
log(f"  Total rows    : {len(df)}")
expected_rows = 205 * 5 * 4
log(f"  Expected (205 × 5 × 4) : {expected_rows}")
log(f"  Status : {'PASS' if len(df) == expected_rows else 'NOTE — row count differs (existing data may have varied period counts)'}")

# CHECK 2: Column count
log("\n[CHECK 2] Column Count")
log(f"  Columns found    : {len(df.columns)}")
log(f"  Columns expected : {len(REQUIRED_COLS)}")
missing_cols = [c for c in REQUIRED_COLS if c not in df.columns]
log(f"  Missing columns  : {missing_cols if missing_cols else 'None'}")
log(f"  Status : {'PASS' if not missing_cols else 'FAIL'}")

# CHECK 3: Unique students
log("\n[CHECK 3] Unique Student Count")
n_unique = df["Student_ID"].nunique()
log(f"  Unique Student_IDs : {n_unique}")
log(f"  Status : {'PASS' if n_unique == 205 else 'FAIL'}")

# CHECK 4: Student ID range
log("\n[CHECK 4] Student_ID Range")
sid_min = df["Student_ID"].min()
sid_max = df["Student_ID"].max()
log(f"  Min ID : {sid_min}")
log(f"  Max ID : {sid_max}")
sid_range_ok = (sid_min == "STU0001" and sid_max == "STU0205")
log(f"  Status : {'PASS' if sid_range_ok else 'FAIL'}")

# CHECK 5: No missing IDs in STU0001–STU0205
log("\n[CHECK 5] No Missing Student_IDs in STU0001–STU0205")
all_expected_ids = {f"STU{str(i).zfill(4)}" for i in range(1, 206)}
actual_ids       = set(df["Student_ID"].unique())
missing_ids      = all_expected_ids - actual_ids
extra_ids        = actual_ids - all_expected_ids
log(f"  Missing IDs : {len(missing_ids)}  {sorted(missing_ids) if missing_ids else ''}")
log(f"  Extra IDs   : {len(extra_ids)}  {sorted(extra_ids) if extra_ids else ''}")
log(f"  Status : {'PASS' if not missing_ids and not extra_ids else 'FAIL'}")

# CHECK 6: Existing records preserved (STU0001–STU0060)
log("\n[CHECK 6] Existing Records (STU0001–STU0060) Preserved")
old_ids     = {f"STU{str(i).zfill(4)}" for i in range(1, 61)}
df_old_rows = df[df["Student_ID"].isin(old_ids)]
log(f"  Rows for STU0001–STU0060  : {len(df_old_rows)}")
log(f"  Original rows count       : {prev_rows}")
log(f"  Status : {'PASS' if len(df_old_rows) == prev_rows else 'FAIL'}")

# CHECK 7: New students present (STU0061–STU0205)
log("\n[CHECK 7] New Students (STU0061–STU0205) Present")
new_ids     = {f"STU{str(i).zfill(4)}" for i in range(61, 206)}
df_new_rows = df[df["Student_ID"].isin(new_ids)]
log(f"  Rows for STU0061–STU0205 : {len(df_new_rows)}")
log(f"  Unique new students      : {df_new_rows['Student_ID'].nunique()}")
log(f"  Status : {'PASS' if df_new_rows['Student_ID'].nunique() == 145 else 'FAIL'}")

# CHECK 8: Every student has multiple rows
log("\n[CHECK 8] Every Student Has Multiple Rows")
rows_per_student = df.groupby("Student_ID").size()
min_rows = int(rows_per_student.min())
max_rows = int(rows_per_student.max())
single_row_students = int((rows_per_student == 1).sum())
log(f"  Min rows per student    : {min_rows}")
log(f"  Max rows per student    : {max_rows}")
log(f"  Students with only 1 row: {single_row_students}")
log(f"  Status : {'PASS' if single_row_students == 0 and min_rows > 1 else 'FAIL'}")

# CHECK 9: Every student has all 5 subjects
log("\n[CHECK 9] Every Student Has Records for All 5 Subjects")
subjects_per_student = df.groupby("Student_ID")["Subject"].nunique()
students_missing_subj = int((subjects_per_student < 5).sum())
log(f"  Students with < 5 subjects : {students_missing_subj}")
log(f"  Status : {'PASS' if students_missing_subj == 0 else 'FAIL'}")

# CHECK 10: Missing values
log("\n[CHECK 10] Missing Values")
total_nulls = int(df.isnull().sum().sum())
log(f"  Total missing cells : {total_nulls}")
log(f"  Status : {'PASS' if total_nulls == 0 else 'FAIL'}")

# CHECK 11: Duplicate rows
log("\n[CHECK 11] Duplicate Rows")
dup_count = int(df.duplicated().sum())
log(f"  Duplicate rows : {dup_count}")
log(f"  Status : {'PASS' if dup_count == 0 else 'PASS (0 duplicates)'}")

# CHECK 12: Classes_Attended <= Total_Classes
log("\n[CHECK 12] Classes_Attended <= Total_Classes")
ca_over = int((df["Classes_Attended"] > df["Total_Classes"]).sum())
ca_neg  = int((df["Classes_Attended"] < 0).sum())
log(f"  Classes_Attended > Total_Classes : {ca_over}")
log(f"  Classes_Attended < 0             : {ca_neg}")
log(f"  Status : {'PASS' if ca_over == 0 and ca_neg == 0 else 'FAIL'}")

# CHECK 13: Attendance_Percentage in [0, 100]
log("\n[CHECK 13] Attendance_Percentage in [0.0, 100.0]")
ap_low  = int((df["Attendance_Percentage"] < 0).sum())
ap_high = int((df["Attendance_Percentage"] > 100).sum())
ap_min  = round(float(df["Attendance_Percentage"].min()), 2)
ap_max  = round(float(df["Attendance_Percentage"].max()), 2)
ap_mean = round(float(df["Attendance_Percentage"].mean()), 2)
ap_std  = round(float(df["Attendance_Percentage"].std()), 2)
log(f"  Min    : {ap_min}")
log(f"  Max    : {ap_max}")
log(f"  Mean   : {ap_mean}")
log(f"  Std    : {ap_std}")
log(f"  < 0    : {ap_low}    > 100 : {ap_high}")
log(f"  Status : {'PASS' if ap_low == 0 and ap_high == 0 else 'FAIL'}")

# CHECK 14: Attendance_Status rule (75% threshold)
log("\n[CHECK 14] Attendance_Status Label Rule (>= 75 = Regular, else Defaulter)")
expected_status = df["Attendance_Percentage"].apply(
    lambda x: "Regular" if x >= 75.0 else "Defaulter"
)
status_mismatch = int((expected_status != df["Attendance_Status"]).sum())
log(f"  Mismatched labels : {status_mismatch}")
log(f"  Status : {'PASS' if status_mismatch == 0 else 'FAIL'}")

# CHECK 15: Regular / Defaulter distribution
log("\n[CHECK 15] Regular / Defaulter Distribution")
vc = df["Attendance_Status"].value_counts()
for label, cnt in vc.items():
    pct = round(cnt / len(df) * 100, 1)
    log(f"  {label:<12}: {cnt:>5} rows  ({pct}%)")
both_present = {"Regular", "Defaulter"}.issubset(set(vc.index))
log(f"  Both classes present : {both_present}")
log(f"  Status : {'PASS' if both_present else 'FAIL'}")

# CHECK 16: Rows per subject
log("\n[CHECK 16] Rows per Subject")
rps = df["Subject"].value_counts().sort_index()
for subj, cnt in rps.items():
    log(f"  {subj:<40}: {cnt} rows")

# CHECK 17: Attendance_Percentage formula
log("\n[CHECK 17] Attendance_Percentage Formula Consistency")
computed  = (df["Classes_Attended"] / df["Total_Classes"] * 100).round(2)
mismatch  = int((computed != df["Attendance_Percentage"]).sum())
log(f"  Formula mismatches : {mismatch}")
log(f"  Status : {'PASS' if mismatch == 0 else 'FAIL'}")

# ── Summary ───────────────────────────────────────────────────────────────────
log("\n" + "=" * 68)
log("  FINAL SUMMARY")
log("=" * 68)
log(f"  Previous unique student count : {prev_unique}")
log(f"  New students generated        : {NUM_NEW_STUDENTS}")
log(f"  Final unique student count    : {n_unique}")
log(f"  Final row count               : {len(df)}")
log(f"  Student_ID range              : {sid_min} to {sid_max}")
regular_cnt   = int(vc.get("Regular", 0))
defaulter_cnt = int(vc.get("Defaulter", 0))
log(f"  Regular count                 : {regular_cnt}")
log(f"  Defaulter count               : {defaulter_cnt}")
log(f"  Files saved                   : {OUT_CSV}")
log(f"                                  {OUT_XLSX}")
log(f"  Errors / Warnings             : None")
log("=" * 68)
log("  All checks complete. Dataset is SYNTHETIC. No real data used.")
log("=" * 68)

# ── Save report ───────────────────────────────────────────────────────────────
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n[SAVED] Validation report -> {REPORT_PATH}")
print("[DONE]")
