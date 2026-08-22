"""
validate_final_dataset.py
Comprehensive validation of data/student_attendance_205_students.csv
Saves report to outputs/final_dataset_validation_report.txt
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = r"d:\Data_Science_attendence_project"
DATA_FILE  = os.path.join(BASE_DIR, "data", "student_attendance_205_students.csv")
OUT_FILE   = os.path.join(BASE_DIR, "outputs", "final_dataset_validation_report.txt")

lines = []
PASS_COUNT = 0
FAIL_COUNT = 0

def log(msg=""):
    lines.append(msg)
    print(msg.encode("ascii", errors="replace").decode("ascii"))

def section(title):
    bar = "=" * 70
    log(bar)
    log(f"  {title}")
    log(bar)

def check(label, passed, detail=""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {label}"
    if detail:
        msg += f"\n         -> {detail}"
    log(msg)
    return passed

# ══════════════════════════════════════════════════════════════════════════════
log("=" * 70)
log(f"  FINAL DATASET VALIDATION REPORT")
log(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
log("=" * 70)
log()

# ── CHECK 1 : File path ───────────────────────────────────────────────────────
section("CHECK 1 · Dataset File Path")
file_exists = os.path.isfile(DATA_FILE)
log(f"  Path : {DATA_FILE}")
check("File exists at the expected path", file_exists)
log()

if not file_exists:
    log("CRITICAL: Dataset file not found. Aborting validation.")
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    raise SystemExit(1)

# ── Load ──────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_FILE)

# ── CHECK 2 : Dimensions ──────────────────────────────────────────────────────
section("CHECK 2 · Total Rows and Columns")
total_rows, total_cols = df.shape
log(f"  Rows    : {total_rows:,}")
log(f"  Columns : {total_cols}")
log(f"  Columns : {list(df.columns)}")
check("Dataset has rows > 0", total_rows > 0, f"{total_rows:,} rows")
check("Dataset has columns > 0", total_cols > 0, f"{total_cols} columns")
log()

# ── CHECK 3 & 4 : Unique Student_ID count ─────────────────────────────────────
section("CHECK 3 & 4 · Unique Student_ID Count (Expected: 205)")
unique_ids = df["Student_ID"].nunique()
log(f"  Unique Student_IDs : {unique_ids}")
check("Student_ID column present", "Student_ID" in df.columns)
check("Unique students == 205", unique_ids == 205, f"Found {unique_ids}")
log()

# ── CHECK 5 : ID range STU0001 – STU0205 ─────────────────────────────────────
section("CHECK 5 · Student_ID Range (Expected: STU0001 – STU0205)")
id_list = sorted(df["Student_ID"].dropna().unique().tolist())
first_id = id_list[0]  if id_list else "N/A"
last_id  = id_list[-1] if id_list else "N/A"
log(f"  First ID : {first_id}")
log(f"  Last ID  : {last_id}")
check("First ID == STU0001", first_id == "STU0001", f"Got {first_id}")
check("Last ID  == STU0205", last_id  == "STU0205", f"Got {last_id}")
log()

# ── CHECK 6 : Missing / invalid Student_IDs ───────────────────────────────────
section("CHECK 6 · Missing or Invalid Student_IDs")
pattern = re.compile(r"^STU\d{4}$")

null_ids    = df["Student_ID"].isna().sum()
invalid_ids = [s for s in df["Student_ID"].dropna().unique()
               if not pattern.match(str(s))]

expected_ids = {f"STU{i:04d}" for i in range(1, 206)}
present_ids  = set(df["Student_ID"].dropna().unique())
missing_from_dataset = expected_ids - present_ids

log(f"  Null Student_IDs         : {null_ids}")
log(f"  Malformed Student_IDs    : {len(invalid_ids)}")
log(f"  IDs missing from STU0001-STU0205 range : {len(missing_from_dataset)}")
if missing_from_dataset:
    log(f"  Missing : {sorted(missing_from_dataset)[:10]} ...")
if invalid_ids:
    log(f"  Invalid : {invalid_ids[:10]}")

check("No null Student_IDs",     null_ids == 0,           f"{null_ids} nulls")
check("No malformed Student_IDs",len(invalid_ids) == 0,   f"{len(invalid_ids)} invalid")
check("No IDs missing from STU0001-STU0205",
      len(missing_from_dataset) == 0,
      f"{len(missing_from_dataset)} missing")
log()

# ── CHECK 7 & 8 : Rows per Student_ID ────────────────────────────────────────
section("CHECK 7 & 8 · Rows per Student_ID (Every Student Must Have Multiple Rows)")
rows_per_student = df.groupby("Student_ID").size()
min_rows = int(rows_per_student.min())
max_rows = int(rows_per_student.max())
mean_rows = rows_per_student.mean()
log(f"  Min rows per student  : {min_rows}")
log(f"  Max rows per student  : {max_rows}")
log(f"  Mean rows per student : {mean_rows:.2f}")
students_single_row = (rows_per_student == 1).sum()
log(f"  Students with only 1 row : {students_single_row}")
check("Every student has > 1 row", min_rows > 1,
      f"Min rows = {min_rows}")
log()

# ── CHECK 9 : Unique subjects ─────────────────────────────────────────────────
section("CHECK 9 · Unique Subjects")
if "Subject" in df.columns:
    subjects = sorted(df["Subject"].dropna().unique().tolist())
    log(f"  Unique subjects ({len(subjects)}) : {subjects}")
    check("At least 5 subjects found", len(subjects) >= 5,
          f"Found {len(subjects)}: {subjects}")
else:
    log("  'Subject' column NOT found.")
    check("Subject column present", False)
log()

# ── CHECK 10 : Every student has all 5 subjects ───────────────────────────────
section("CHECK 10 · Every Student Has All 5 Subjects")
if "Subject" in df.columns:
    all_subjects = set(df["Subject"].dropna().unique())
    pivot = df.groupby("Student_ID")["Subject"].apply(set)
    students_missing_subjects = pivot[pivot != all_subjects]
    log(f"  Students missing ≥1 subject : {len(students_missing_subjects)}")
    if not students_missing_subjects.empty:
        for sid, subs in students_missing_subjects.head(5).items():
            log(f"    {sid} has : {subs}")
    check("Every student has all subjects",
          len(students_missing_subjects) == 0,
          f"{len(students_missing_subjects)} students have incomplete subjects")
log()

# ── CHECK 11 : Missing values ────────────────────────────────────────────────
section("CHECK 11 · Missing Values")
missing = df.isnull().sum()
total_missing = missing.sum()
log(f"  Total missing cells : {total_missing}")
if total_missing > 0:
    log("  Per-column breakdown:")
    for col, cnt in missing[missing > 0].items():
        log(f"    {col}: {cnt}")
check("No missing values", total_missing == 0, f"{total_missing} missing")
log()

# ── CHECK 12 : Duplicate rows ────────────────────────────────────────────────
section("CHECK 12 · Duplicate Rows")
dup_count = df.duplicated().sum()
log(f"  Duplicate rows : {dup_count}")
check("No duplicate rows", dup_count == 0, f"{dup_count} duplicates")
log()

# ── CHECK 13 : Classes_Attended <= Total_Classes ──────────────────────────────
section("CHECK 13 · Classes_Attended ≤ Total_Classes")
ca_col = "Classes_Attended"
tc_col = "Total_Classes"
if ca_col in df.columns and tc_col in df.columns:
    invalid_rows = (df[ca_col] > df[tc_col]).sum()
    log(f"  Rows where Classes_Attended > Total_Classes : {invalid_rows}")
    check("Classes_Attended ≤ Total_Classes for all rows",
          invalid_rows == 0, f"{invalid_rows} violations")
    log(f"  Classes_Attended range : [{df[ca_col].min()}, {df[ca_col].max()}]")
    log(f"  Total_Classes    range : [{df[tc_col].min()}, {df[tc_col].max()}]")
else:
    log(f"  Columns '{ca_col}' and/or '{tc_col}' not found.")
    check("Required columns present", False)
log()

# ── CHECK 14 : Recalculate Attendance_Percentage ─────────────────────────────
section("CHECK 14 · Recalculate Attendance_Percentage")
ap_col = "Attendance_Percentage"
if ca_col in df.columns and tc_col in df.columns and ap_col in df.columns:
    recalc = (df[ca_col] / df[tc_col] * 100).round(2)
    diff   = (df[ap_col].round(2) - recalc).abs()
    max_diff       = diff.max()
    mismatch_count = (diff > 0.05).sum()           # allow ±0.05 rounding
    log(f"  Max difference (stored vs recalculated) : {max_diff:.4f}")
    log(f"  Rows with |diff| > 0.05                 : {mismatch_count}")
    check("Attendance_Percentage matches recalculated values",
          mismatch_count == 0, f"{mismatch_count} mismatches (max diff={max_diff:.4f})")
else:
    log(f"  Required columns missing.")
    check("Required columns for recalculation present", False)
log()

# ── CHECK 15 & 16 : Attendance_Status ────────────────────────────────────────
section("CHECK 15 & 16 · Attendance_Status Logic and Counts")
as_col = "Attendance_Status"
if ap_col in df.columns and as_col in df.columns:
    df["_expected_status"] = df[ap_col].apply(
        lambda x: "Regular" if x >= 75 else "Defaulter"
    )
    status_mismatch = (df[as_col] != df["_expected_status"]).sum()
    status_counts   = df[as_col].value_counts()

    log(f"  Status distribution:")
    for status, cnt in status_counts.items():
        log(f"    {status} : {cnt:,}")

    regular_count   = int(status_counts.get("Regular",   0))
    defaulter_count = int(status_counts.get("Defaulter", 0))

    log(f"  Status mismatches (stored vs rule-based) : {status_mismatch}")
    check("Attendance_Status follows the ≥75/< 75 rule",
          status_mismatch == 0, f"{status_mismatch} mismatches")
    check("Both 'Regular' and 'Defaulter' labels exist",
          regular_count > 0 and defaulter_count > 0,
          f"Regular={regular_count:,}, Defaulter={defaulter_count:,}")
    df.drop(columns=["_expected_status"], inplace=True)
else:
    log(f"  '{ap_col}' and/or '{as_col}' columns missing.")
    check("Required columns for status check present", False)
    regular_count   = 0
    defaulter_count = 0
log()

# ── CHECK 17 : Numeric ranges ────────────────────────────────────────────────
section("CHECK 17 · Numeric Column Ranges")
numeric_checks = {
    "Attendance_Percentage": (0, 100),
    "Classes_Attended":      (0, None),
    "Total_Classes":         (1, None),
}
for col, (lo, hi) in numeric_checks.items():
    if col not in df.columns:
        check(f"{col} present", False, "Column missing")
        continue
    numeric_series = pd.to_numeric(df[col], errors="coerce")
    col_min = float(numeric_series.min())
    col_max = float(numeric_series.max())
    lo_ok = (col_min >= lo) if lo is not None else True
    hi_ok = (col_max <= hi) if hi is not None else True
    log(f"  {col}: min={col_min}, max={col_max}  (expected [{lo}, {hi if hi else 'inf'}])")
    check(f"{col} within expected range", lo_ok and hi_ok,
          f"min={col_min}, max={col_max}")

# Semester is stored as text (e.g. 'Third Semester', 'Fifth Semester')
if "Semester" in df.columns:
    sem_values = df["Semester"].dropna().unique().tolist()
    log(f"  Semester (text label) unique values : {sorted(sem_values)}")
    check("Semester column present and non-empty", len(sem_values) > 0,
          f"{len(sem_values)} unique semester labels: {sorted(sem_values)}")
else:
    check("Semester column present", False, "Column missing")
log()

# ── CHECK 18 : No private data (names / roll-no / email) ─────────────────────
section("CHECK 18 · No Private Data (Names / Roll Numbers / College Emails)")
email_pattern = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
col_names_lower = [c.lower() for c in df.columns]

suspicious_col_keywords = ["name", "roll", "email", "phone", "mobile",
                            "address", "id_card", "aadhaar"]
suspicious_cols = [
    c for c in df.columns
    if any(kw in c.lower() for kw in suspicious_col_keywords)
    and c.lower() != "student_id"
]

log(f"  Columns that may contain private data : {suspicious_cols}")

# Scan string columns for email patterns
email_hits = []
for col in df.select_dtypes(include="object").columns:
    if col == "Student_ID":
        continue
    hits = df[col].dropna().astype(str).apply(lambda v: bool(email_pattern.search(v)))
    if hits.any():
        email_hits.append(col)

log(f"  Columns containing email-like strings : {email_hits}")
check("No suspicious private-data columns", len(suspicious_cols) == 0,
      f"Suspicious columns: {suspicious_cols}")
check("No email-like strings in any column", len(email_hits) == 0,
      f"Email hits in: {email_hits}")
log()

# ── SUMMARY ───────────────────────────────────────────────────────────────────
section("VALIDATION SUMMARY")
all_passed = FAIL_COUNT == 0
log(f"  Total checks : {PASS_COUNT + FAIL_COUNT}")
log(f"  PASSED       : {PASS_COUNT}")
log(f"  FAILED       : {FAIL_COUNT}")
log()
log(f"  Dataset path         : {DATA_FILE}")
log(f"  Total rows           : {total_rows:,}")
log(f"  Total columns        : {total_cols}")
log(f"  Unique students      : {unique_ids}")
log(f"  Student_ID range     : {first_id} - {last_id}")
log(f"  Unique subjects      : {len(subjects) if 'Subject' in df.columns else 'N/A'}")
log(f"  Missing values       : {total_missing}")
log(f"  Duplicate rows       : {dup_count}")
log(f"  Regular records      : {regular_count:,}")
log(f"  Defaulter records    : {defaulter_count:,}")
log()
if all_passed:
    log("  [ALL PASS]  ALL CHECKS PASSED -- Dataset is ready for machine learning.")
else:
    log("  [FAILURES]  SOME CHECKS FAILED -- Fix the dataset before proceeding to ML.")
log("=" * 70)

# ── Save report ───────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"\nReport saved -> {OUT_FILE}")

# Return structured results for PROJECT_STATUS update
print("\n__RESULTS__")
print(f"total_rows={total_rows}")
print(f"total_cols={total_cols}")
print(f"unique_students={unique_ids}")
print(f"first_id={first_id}")
print(f"last_id={last_id}")
print(f"unique_subjects={len(subjects) if 'Subject' in df.columns else 0}")
print(f"missing_values={total_missing}")
print(f"duplicate_rows={dup_count}")
print(f"regular_count={regular_count}")
print(f"defaulter_count={defaulter_count}")
print(f"all_passed={all_passed}")
print(f"pass_count={PASS_COUNT}")
print(f"fail_count={FAIL_COUNT}")
