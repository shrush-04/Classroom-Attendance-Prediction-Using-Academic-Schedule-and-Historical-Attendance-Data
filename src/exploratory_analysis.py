"""
exploratory_analysis.py
Reusable script for exploratory data analysis (EDA) of synthetic student attendance dataset.
Saves analysis results and visual charts.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for plots
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16
})

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = r"d:\Data_Science_attendence_project"
DATA_FILE  = os.path.join(BASE_DIR, "data", "student_attendance_205_students.csv")
CHARTS_DIR = os.path.join(BASE_DIR, "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1. Load data
# ══════════════════════════════════════════════════════════════════════════════
print("Loading dataset...")
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"Dataset not found at {DATA_FILE}")

df = pd.read_csv(DATA_FILE)
print(f"Dataset loaded successfully from: {DATA_FILE}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. Basic dataset properties
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("1. DATASET OVERVIEW")
print("=" * 50)
print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
print("\nColumns and Data Types:")
print(df.dtypes)
print("\nFirst 5 Rows:")
print(df.head())

print("\nSummary Statistics for Numeric Columns:")
print(df.describe())

# ══════════════════════════════════════════════════════════════════════════════
# 3. Overall Attendance Statistics
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("2. OVERALL ATTENDANCE STATISTICS")
print("=" * 50)
att_col = "Attendance_Percentage"
avg_att = df[att_col].mean()
min_att = df[att_col].min()
max_att = df[att_col].max()
med_att = df[att_col].median()

print(f"Average Attendance: {avg_att:.2f}%")
print(f"Minimum Attendance: {min_att:.2f}%")
print(f"Maximum Attendance: {max_att:.2f}%")
print(f"Median Attendance : {med_att:.2f}%")

# ══════════════════════════════════════════════════════════════════════════════
# 4. Status Counts and Percentages
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("3. REGULAR VS DEFAULTER COUNTS & PERCENTAGES")
print("=" * 50)
status_counts = df["Attendance_Status"].value_counts()
status_pcts = df["Attendance_Status"].value_counts(normalize=True) * 100

for label in status_counts.index:
    print(f"{label}: {status_counts[label]} rows ({status_pcts[label]:.2f}%)")

# ══════════════════════════════════════════════════════════════════════════════
# 5. Department-wise Attendance
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("4. DEPARTMENT-WISE ATTENDANCE")
print("=" * 50)
dept_stats = df.groupby("Department")[att_col].agg(["count", "mean", "min", "max", "median"])
print(dept_stats)

# ══════════════════════════════════════════════════════════════════════════════
# 6. Subject-wise Attendance
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("5. SUBJECT-WISE ATTENDANCE")
print("=" * 50)
subject_stats = df.groupby("Subject")[att_col].agg(["count", "mean", "min", "max", "median"])
print(subject_stats)

# ══════════════════════════════════════════════════════════════════════════════
# 7. Year-wise and Semester-wise Attendance
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 50)
print("6. YEAR-WISE & SEMESTER-WISE ATTENDANCE")
print("=" * 50)
print("Year-wise:")
year_stats = df.groupby("Year")[att_col].agg(["count", "mean", "median"])
print(year_stats)

print("\nSemester-wise:")
sem_stats = df.groupby("Semester")[att_col].agg(["count", "mean", "median"])
print(sem_stats)

print("\nYear and Semester cross-tabulation mean:")
year_sem_stats = df.groupby(["Year", "Semester"])[att_col].mean()
print(year_sem_stats)


# ══════════════════════════════════════════════════════════════════════════════
# 8. Chart Creation
# ══════════════════════════════════════════════════════════════════════════════
print("\nGenerating charts...")

def save_plot(filename):
    path = os.path.join(CHARTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {filename}")

# Chart 1: attendance_distribution.png
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x=att_col, kde=True, bins=25, color="skyblue")
plt.axvline(75, color="red", linestyle="--", linewidth=1.5, label="Attendance Threshold (75%)")
plt.title("Distribution of Student Attendance Percentage")
plt.xlabel("Attendance Percentage (%)")
plt.ylabel("Frequency")
plt.legend()
save_plot("attendance_distribution.png")

# Chart 2: regular_defaulter_count.png
plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df, x="Attendance_Status", hue="Attendance_Status", palette="pastel", legend=False)
plt.title("Count of Regular vs Defaulter Attendance Records")
plt.xlabel("Attendance Status")
plt.ylabel("Number of Records")
# Add values on top of bars
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height() + 20),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points')
save_plot("regular_defaulter_count.png")

# Chart 3: subject_wise_attendance.png
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x="Subject", y=att_col, hue="Subject", palette="Set2", legend=False)
plt.axhline(75, color="red", linestyle="--", linewidth=1.2, label="Threshold (75%)")
plt.xticks(rotation=15, ha='right')
plt.title("Subject-wise Attendance Distribution")
plt.xlabel("Subject")
plt.ylabel("Attendance Percentage (%)")
save_plot("subject_wise_attendance.png")

# Chart 4: attendance_by_period.png
if "Attendance_Period" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Attendance_Period", y=att_col, hue="Attendance_Period", palette="Set3", legend=False)
    plt.title("Attendance Distribution by Period")
    plt.xlabel("Attendance Period")
    plt.ylabel("Attendance Percentage (%)")
    save_plot("attendance_by_period.png")
else:
    print("Skipping attendance_by_period.png: Attendance_Period not found")

# Chart 5: study_hours_vs_attendance.png
if "Study_Hours_Per_Week" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Study_Hours_Per_Week", y=att_col, hue="Attendance_Status", palette="coolwarm", alpha=0.7)
    # Add a regression trend line using regplot without hue
    sns.regplot(data=df, x="Study_Hours_Per_Week", y=att_col, scatter=False, color="black", label="Trend Line")
    plt.title("Study Hours per Week vs Attendance Percentage")
    plt.xlabel("Study Hours per Week")
    plt.ylabel("Attendance Percentage (%)")
    plt.legend()
    save_plot("study_hours_vs_attendance.png")
else:
    print("Skipping study_hours_vs_attendance.png: Study_Hours_Per_Week not found")

# Chart 6: internal_marks_vs_attendance.png
if "Internal_Marks" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Internal_Marks", y=att_col, hue="Attendance_Status", palette="coolwarm", alpha=0.7)
    sns.regplot(data=df, x="Internal_Marks", y=att_col, scatter=False, color="black", label="Trend Line")
    plt.title("Internal Marks vs Attendance Percentage")
    plt.xlabel("Internal Marks")
    plt.ylabel("Attendance Percentage (%)")
    plt.legend()
    save_plot("internal_marks_vs_attendance.png")
else:
    print("Skipping internal_marks_vs_attendance.png: Internal_Marks not found")

# Chart 7: medical_leave_vs_attendance.png
if "Medical_Leave_Days" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="Medical_Leave_Days", y=att_col, hue="Medical_Leave_Days", palette="Blues", legend=False)
    plt.title("Medical Leave Days vs Attendance Percentage")
    plt.xlabel("Medical Leave Days")
    plt.ylabel("Attendance Percentage (%)")
    save_plot("medical_leave_vs_attendance.png")
else:
    print("Skipping medical_leave_vs_attendance.png: Medical_Leave_Days not found")

# Chart 8: late_count_vs_attendance.png
if "Late_Count" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="Late_Count", y=att_col, hue="Attendance_Status", palette="coolwarm", alpha=0.7)
    sns.regplot(data=df, x="Late_Count", y=att_col, scatter=False, color="black", label="Trend Line")
    plt.title("Late Count vs Attendance Percentage")
    plt.xlabel("Late Count")
    plt.ylabel("Attendance Percentage (%)")
    plt.legend()
    save_plot("late_count_vs_attendance.png")
else:
    print("Skipping late_count_vs_attendance.png: Late_Count not found")

# Chart 9: correlation_heatmap.png
numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    plt.figure(figsize=(14, 12))
    corr_matrix = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .8})
    plt.title("Correlation Matrix Heatmap (Numeric Features Only)")
    save_plot("correlation_heatmap.png")
else:
    print("Skipping correlation_heatmap.png: No numeric columns found")

print("\nEDA processing complete!")
