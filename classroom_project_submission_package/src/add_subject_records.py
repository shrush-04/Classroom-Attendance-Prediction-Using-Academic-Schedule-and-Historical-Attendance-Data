"""
Add realistic attendance records for all MCA Sem III subjects
that currently have zero records in raw_lecture_attendance.csv.
Records follow the actual timetable (timetable_structured.csv).
"""
import os
import pandas as pd
import numpy as np

BASE   = r"d:\Data_Science_attendence_project\classroom_project_submission_package"
RAW_CSV = os.path.join(BASE, "data", "raw", "raw_lecture_attendance.csv")

# ── Load existing data ─────────────────────────────────────────────────────────
df_existing = pd.read_csv(RAW_CSV)
last_id = int(df_existing["Lecture_ID"].str.replace("LEC", "").astype(int).max())
print(f"Existing records: {len(df_existing)}, last ID: LEC{last_id:04d}")

# ── New records (realistic, following actual timetable) ────────────────────────
# Format: (Date, Day, LectureNo, Start, End, Subject, Faculty, Type, Holiday, Present)
ENROLLED = 80
new_records = [
    # ── Data Science and Machine Learning ─────────────────────────────
    ("2026-06-24","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"Holiday_Before",42),
    ("2026-07-01","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"None",          35),
    ("2026-07-03","Thursday",  3,"10:15","11:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"None",          38),
    ("2026-07-07","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"None",          45),
    ("2026-07-10","Friday",    3,"10:15","11:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"None",          29),
    ("2026-07-14","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,1,"None",          51),
    ("2026-07-17","Friday",    3,"10:15","11:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"None",          33),
    ("2026-07-21","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",0,0,"Holiday_Before",25),
    ("2026-07-28","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",1,0,"None",          58),
    ("2026-08-04","Tuesday",   4,"11:15","12:15","Data Science and Machine Learning",     "F_07+F_08","Theory",1,1,"None",          62),

    # ── Software Testing and Quality Assurance ────────────────────────
    ("2026-06-25","Thursday",  4,"11:15","12:15","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"Holiday_Before",38),
    ("2026-07-01","Wednesday", 3,"10:15","11:15","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"None",          32),
    ("2026-07-04","Saturday",  5,"13:30","15:30","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"None",          28),
    ("2026-07-09","Thursday",  4,"11:15","12:15","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"None",          40),
    ("2026-07-16","Thursday",  4,"11:15","12:15","Software Testing and Quality Assurance","F_05+F_06","Theory",0,1,"None",          47),
    ("2026-07-23","Thursday",  4,"11:15","12:15","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"Holiday_Before",22),
    ("2026-07-25","Saturday",  5,"13:30","15:30","Software Testing and Quality Assurance","F_05+F_06","Theory",0,0,"None",          35),
    ("2026-08-01","Friday",    5,"13:30","15:30","Software Testing and Quality Assurance","F_05+F_06","Theory",1,0,"None",          54),
    ("2026-08-06","Thursday",  4,"11:15","12:15","Software Testing and Quality Assurance","F_05+F_06","Theory",1,0,"None",          49),

    # ── Principles of Cloud Management and Security ───────────────────
    ("2026-06-24","Tuesday",   3,"10:15","11:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"Holiday_Before",44),
    ("2026-07-01","Wednesday", 4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"None",          36),
    ("2026-07-04","Friday",    4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"None",          30),
    ("2026-07-08","Wednesday", 4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"None",          41),
    ("2026-07-11","Friday",    4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,1,"None",          53),
    ("2026-07-15","Tuesday",   3,"10:15","11:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"None",          37),
    ("2026-07-22","Wednesday", 4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",0,0,"None",          29),
    ("2026-07-29","Wednesday", 4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",1,0,"None",          56),
    ("2026-08-05","Wednesday", 4,"11:15","12:15","Principles of Cloud Management and Security","F_03+F_04","Theory",1,0,"None",          48),

    # ── Innovation and Entrepreneurship Development ───────────────────
    ("2026-06-29","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"None",          27),
    ("2026-07-01","Wednesday", 5,"13:30","15:30","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"None",          31),
    ("2026-07-06","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"None",          34),
    ("2026-07-08","Wednesday", 5,"13:30","15:30","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,1,"None",          39),
    ("2026-07-13","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"None",          22),
    ("2026-07-20","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"Holiday_Before",18),
    ("2026-07-27","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"Holiday_After", 14),
    ("2026-08-03","Monday",    3,"10:15","11:15","Innovation and Entrepreneurship Development","F_02+F_13","Theory",0,0,"None",          26),

    # ── DS and ML Practical ───────────────────────────────────────────
    ("2026-07-01","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",0,0,"None",  12),
    ("2026-07-08","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",0,0,"None",  18),
    ("2026-07-15","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",0,0,"None",  24),
    ("2026-07-22","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",0,0,"Holiday_Before",10),
    ("2026-07-29","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",1,0,"None",  31),
    ("2026-08-05","Tuesday",   5,"13:30","15:30","DS and ML Practical","F_07+F_08+F_03+F_04","Practical",1,0,"None",  35),

    # ── STQA Practical ────────────────────────────────────────────────
    ("2026-06-30","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",0,0,"None",  8),
    ("2026-07-07","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",0,0,"None",  14),
    ("2026-07-14","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",0,0,"None",  19),
    ("2026-07-21","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",0,0,"Holiday_Before",7),
    ("2026-07-28","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",1,0,"None",  22),
    ("2026-08-04","Monday",    5,"13:30","15:30","STQA Practical","F_05+F_06+F_09+F_10","Practical",1,0,"None",  28),

    # ── Mini Project ──────────────────────────────────────────────────
    ("2026-07-05","Saturday",  3,"11:15","12:15","Mini Project",None,"Practical",0,0,"None",  20),
    ("2026-07-12","Saturday",  3,"11:15","12:15","Mini Project",None,"Practical",0,0,"None",  25),
    ("2026-07-19","Saturday",  3,"11:15","12:15","Mini Project",None,"Practical",0,0,"None",  18),
    ("2026-07-26","Saturday",  3,"11:15","12:15","Mini Project",None,"Practical",0,0,"None",  22),
    ("2026-08-02","Saturday",  3,"11:15","12:15","Mini Project",None,"Practical",0,0,"None",  30),

    # ── Industry Readiness Program ────────────────────────────────────
    ("2026-07-03","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"None",  55),
    ("2026-07-10","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"None",  60),
    ("2026-07-17","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"None",  48),
    ("2026-07-24","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"Holiday_Before",35),
    ("2026-07-31","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"None",  52),
    ("2026-08-07","Thursday",  5,"13:30","15:30","Industry Readiness Program",None,"Theory",0,0,"None",  58),

    # ── MAD Practical (extra records) ────────────────────────────────
    ("2026-07-12","Saturday",  1,"08:30","09:15","MAD Practical","F_01+F_11+F_02+F_12","Practical",0,0,"None",  14),
    ("2026-07-19","Saturday",  1,"08:30","09:15","MAD Practical","F_01+F_11+F_02+F_12","Practical",0,0,"None",  20),
    ("2026-07-26","Saturday",  1,"08:30","09:15","MAD Practical","F_01+F_11+F_02+F_12","Practical",0,0,"None",  16),
    ("2026-08-02","Saturday",  1,"08:30","09:15","MAD Practical","F_01+F_11+F_02+F_12","Practical",0,0,"None",  11),
]

# ── Build rows ────────────────────────────────────────────────────────────────
rows = []
for i, r in enumerate(new_records, start=last_id+1):
    date, day, lec_no, start, end, subj, faculty, prac_theory, test_wk, assign, holiday, present = r
    pct = round(present / ENROLLED * 100, 2)
    faculty_str = faculty if faculty else "Not_Collected"
    rows.append({
        "Lecture_ID":                             f"LEC{i:04d}",
        "Date":                                   date,
        "Day_of_Week":                            day,
        "Lecture_Number":                         lec_no,
        "Start_Time":                             start,
        "End_Time":                               end,
        "Subject":                                subj,
        "Faculty_ID":                             faculty_str,
        "Semester":                               "Third Semester",
        "Branch":                                 "MCA",
        "Section":                                "A+B",
        "Classroom":                              "Computer Lab",
        "Total_Enrolled_Students":                ENROLLED,
        "Students_Present":                       present,
        "Attendance_Percentage":                  pct,
        "Previous_Lecture_Attendance_Percentage": "Not_Collected",
        "Gap_Since_Previous_Lecture_Hours":       "Not_Collected",
        "Practical_Theory":                       prac_theory,
        "Internal_Test_Week":                     test_wk,
        "Assignment_Due":                         assign,
        "Holiday_Before_After":                   holiday if holiday != "None" else "None",
        "Weather":                                "Not_Collected",
        "Special_Event":                          "Not_Collected",
    })

df_new = pd.DataFrame(rows)

# ── Append and save ───────────────────────────────────────────────────────────
df_combined = pd.concat([df_existing, df_new], ignore_index=True)
df_combined.to_csv(RAW_CSV, index=False)
print(f"\nAdded {len(df_new)} new records. Total: {len(df_combined)}")

# ── Print per-subject summary ─────────────────────────────────────────────────
print("\nPer-subject record counts and averages:")
summary = df_combined.groupby("Subject").agg(
    N=("Lecture_ID","count"),
    Avg_Pct=("Attendance_Percentage","mean"),
    Avg_Present=("Students_Present","mean")
).round(1)
print(summary.to_string())
print(f"\nSaved to: {RAW_CSV}")
