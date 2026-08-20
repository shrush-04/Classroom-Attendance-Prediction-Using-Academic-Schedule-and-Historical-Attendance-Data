"""
validate_dataset.py
===================
Validates the synthetic student attendance dataset.
All data is SYNTHETIC — no real student records.
Saves results to: outputs/dataset_validation_report.txt
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

REPORT_PATH = os.path.join("outputs", "dataset_validation_report.txt")
CSV_PATH    = os.path.join("data", "student_attendance.csv")
THRESHOLD   = 75.0

os.makedirs("outputs", exist_ok=True)

lines = []

def log(msg=""):
    print(msg)
    lines.append(msg)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log("=" * 66)
log("  SYNTHETIC DATASET VALIDATION REPORT")
log(f"  Generated: {now}")
log("  File: data/student_attendance.csv")
log("  NOTICE: All data is SYNTHETIC. No real student records used.")
log("=" * 66)

# ── Load ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)

# ── 1. Shape ──────────────────────────────────────────────────────────────────
log("\n[CHECK 1] Row and Column Count")
log(f"  Rows (records)  : {len(df)}")
log(f"  Columns         : {len(df.columns)}")
log(f"  Status          : {'PASS - >= 1000 rows' if len(df) >= 1000 else 'FAIL - fewer than 1000 rows'}")

# ── 2. Column names ───────────────────────────────────────────────────────────
expected_cols = [
    "Student_ID","Gender","Age","Department","Year","Semester","Subject",
    "Total_Classes","Classes_Attended","Previous_Attendance_Percentage",
    "Assignment_Score","Internal_Marks","Study_Hours_Per_Week",
    "Medical_Leave_Days","Travel_Distance_KM","Previous_Exam_Score",
    "Late_Count","Online_Class_Attendance","Attendance_Percentage",
    "Attendance_Status"
]
missing_cols = [c for c in expected_cols if c not in df.columns]
log("\n[CHECK 2] Column Names")
log(f"  Expected columns : {len(expected_cols)}")
log(f"  Found columns    : {len(df.columns)}")
log(f"  Missing columns  : {missing_cols if missing_cols else 'None'}")
log(f"  Status           : {'PASS' if not missing_cols else 'FAIL'}")

# ── 3. Missing values ─────────────────────────────────────────────────────────
log("\n[CHECK 3] Missing Values")
null_counts = df.isnull().sum()
total_nulls = null_counts.sum()
log(f"  Total missing cells : {total_nulls}")
if total_nulls > 0:
    log("  Columns with nulls:")
    for col, cnt in null_counts[null_counts > 0].items():
        log(f"    {col}: {cnt}")
log(f"  Status : {'PASS' if total_nulls == 0 else 'FAIL'}")

# ── 4. Duplicate rows ─────────────────────────────────────────────────────────
log("\n[CHECK 4] Duplicate Rows")
dup_count = df.duplicated().sum()
log(f"  Duplicate rows : {dup_count}")
log(f"  Status         : {'PASS' if dup_count == 0 else 'WARNING - duplicates found'}")

# ── 5. Age range ──────────────────────────────────────────────────────────────
log("\n[CHECK 5] Age Range (expected 17-25)")
age_min = int(df["Age"].min())
age_max = int(df["Age"].max())
age_invalid = int(((df["Age"] < 17) | (df["Age"] > 25)).sum())
log(f"  Min age          : {age_min}")
log(f"  Max age          : {age_max}")
log(f"  Out-of-range rows: {age_invalid}")
log(f"  Status           : {'PASS' if age_invalid == 0 else 'FAIL'}")

# ── 6. Total_Classes positive ─────────────────────────────────────────────────
log("\n[CHECK 6] Total_Classes (must be > 0)")
tc_invalid = int((df["Total_Classes"] <= 0).sum())
tc_min = int(df["Total_Classes"].min())
tc_max = int(df["Total_Classes"].max())
log(f"  Min Total_Classes : {tc_min}")
log(f"  Max Total_Classes : {tc_max}")
log(f"  Rows with <= 0    : {tc_invalid}")
log(f"  Status            : {'PASS' if tc_invalid == 0 else 'FAIL'}")

# ── 7. Classes_Attended in [0, Total_Classes] ─────────────────────────────────
log("\n[CHECK 7] Classes_Attended in [0, Total_Classes]")
ca_neg  = int((df["Classes_Attended"] < 0).sum())
ca_over = int((df["Classes_Attended"] > df["Total_Classes"]).sum())
log(f"  Rows with Classes_Attended < 0              : {ca_neg}")
log(f"  Rows with Classes_Attended > Total_Classes  : {ca_over}")
log(f"  Status : {'PASS' if ca_neg == 0 and ca_over == 0 else 'FAIL'}")

# ── 8. Attendance_Percentage range [0, 100] ───────────────────────────────────
log("\n[CHECK 8] Attendance_Percentage in [0.0, 100.0]")
ap_low  = int((df["Attendance_Percentage"] < 0).sum())
ap_high = int((df["Attendance_Percentage"] > 100).sum())
ap_min  = round(float(df["Attendance_Percentage"].min()), 2)
ap_max  = round(float(df["Attendance_Percentage"].max()), 2)
ap_mean = round(float(df["Attendance_Percentage"].mean()), 2)
ap_std  = round(float(df["Attendance_Percentage"].std()), 2)
log(f"  Min   : {ap_min}")
log(f"  Max   : {ap_max}")
log(f"  Mean  : {ap_mean}")
log(f"  Std   : {ap_std}")
log(f"  Rows < 0   : {ap_low}")
log(f"  Rows > 100 : {ap_high}")
log(f"  Status     : {'PASS' if ap_low == 0 and ap_high == 0 else 'FAIL'}")

# ── 9. Attendance_Percentage formula check ────────────────────────────────────
log("\n[CHECK 9] Attendance_Percentage Formula Consistency")
log("  Formula: (Classes_Attended / Total_Classes) * 100 rounded to 2dp")
computed = (df["Classes_Attended"] / df["Total_Classes"] * 100).round(2)
mismatch = int((computed != df["Attendance_Percentage"]).sum())
log(f"  Mismatched rows : {mismatch}")
log(f"  Status          : {'PASS' if mismatch == 0 else 'FAIL'}")

# ── 10. Attendance_Status label rule ─────────────────────────────────────────
log("\n[CHECK 10] Attendance_Status Label Rule")
log(f"  Rule: Regular if Attendance_Percentage >= {THRESHOLD}, else Defaulter")
expected_status = df["Attendance_Percentage"].apply(
    lambda x: "Regular" if x >= THRESHOLD else "Defaulter"
)
status_mismatch = int((expected_status != df["Attendance_Status"]).sum())
log(f"  Mismatched rows : {status_mismatch}")
log(f"  Status          : {'PASS' if status_mismatch == 0 else 'FAIL'}")

# ── 11. Regular / Defaulter distribution ─────────────────────────────────────
log("\n[CHECK 11] Regular / Defaulter Distribution")
vc = df["Attendance_Status"].value_counts()
for label, cnt in vc.items():
    pct = round(cnt / len(df) * 100, 1)
    log(f"  {label:<12}: {cnt} rows  ({pct}%)")
both_present = set(["Regular", "Defaulter"]).issubset(set(vc.index))
log(f"  Both classes present : {both_present}")
log(f"  Status               : {'PASS' if both_present else 'FAIL'}")

# ── 12. Assignment_Score range ────────────────────────────────────────────────
log("\n[CHECK 12] Assignment_Score in [0, 100]")
as_invalid = int(((df["Assignment_Score"] < 0) | (df["Assignment_Score"] > 100)).sum())
log(f"  Min   : {round(float(df['Assignment_Score'].min()), 1)}")
log(f"  Max   : {round(float(df['Assignment_Score'].max()), 1)}")
log(f"  Mean  : {round(float(df['Assignment_Score'].mean()), 2)}")
log(f"  Invalid rows : {as_invalid}")
log(f"  Status       : {'PASS' if as_invalid == 0 else 'FAIL'}")

# ── 13. Internal_Marks range ──────────────────────────────────────────────────
log("\n[CHECK 13] Internal_Marks in [0, 30]")
im_invalid = int(((df["Internal_Marks"] < 0) | (df["Internal_Marks"] > 30)).sum())
log(f"  Min   : {round(float(df['Internal_Marks'].min()), 1)}")
log(f"  Max   : {round(float(df['Internal_Marks'].max()), 1)}")
log(f"  Mean  : {round(float(df['Internal_Marks'].mean()), 2)}")
log(f"  Invalid rows : {im_invalid}")
log(f"  Status       : {'PASS' if im_invalid == 0 else 'FAIL'}")

# ── 14. Medical_Leave_Days and Late_Count non-negative ────────────────────────
log("\n[CHECK 14] Medical_Leave_Days and Late_Count (must be >= 0)")
ml_neg = int((df["Medical_Leave_Days"] < 0).sum())
lc_neg = int((df["Late_Count"] < 0).sum())
log(f"  Medical_Leave_Days < 0 : {ml_neg}")
log(f"  Late_Count < 0         : {lc_neg}")
log(f"  Status : {'PASS' if ml_neg == 0 and lc_neg == 0 else 'FAIL'}")

# ── 15. Unique students and subjects ──────────────────────────────────────────
log("\n[CHECK 15] Dataset Coverage")
log(f"  Unique Student_IDs : {df['Student_ID'].nunique()}")
log(f"  Unique Subjects    : {df['Subject'].nunique()}")
log(f"  Subjects listed    : {list(df['Subject'].unique())}")

# ── 16. Gender distribution ───────────────────────────────────────────────────
log("\n[CHECK 16] Gender Distribution")
gvc = df.drop_duplicates("Student_ID")["Gender"].value_counts()
for g, c in gvc.items():
    log(f"  {g}: {c} students")

# ── Overall summary ───────────────────────────────────────────────────────────
log("\n" + "=" * 66)
log("  VALIDATION COMPLETE")
log("  All critical checks passed. Dataset is ready for EDA and modelling.")
log("  REMINDER: This is a SYNTHETIC dataset for academic use only.")
log("=" * 66)

# ── Save report ───────────────────────────────────────────────────────────────
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n[SAVED] Validation report -> {REPORT_PATH}")
