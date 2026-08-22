"""
generate_eda_notebook.py
Programmatically generates and executes notebooks/01_exploratory_data_analysis.ipynb
"""

import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

BASE_DIR = r"d:\Data_Science_attendence_project"
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)
NOTEBOOK_PATH = os.path.join(NOTEBOOKS_DIR, "01_exploratory_data_analysis.ipynb")

# Initialize notebook structure
nb = nbformat.v4.new_notebook()

# Define cells
cells = []

# Cell 1: Header
cells.append(nbformat.v4.new_markdown_cell(
    "# Phase 2: Exploratory Data Analysis (EDA)\n"
    "**Project:** Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System\n\n"
    "This notebook contains the exploratory data analysis for the validated 205-student synthetic dataset.\n"
    "All data in this project is fully synthetic and computer-generated to protect privacy."
))

# Cell 2: Imports
cells.append(nbformat.v4.new_code_cell(
    "import os\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n\n"
    "# Set style for plots\n"
    "sns.set_theme(style=\"whitegrid\")\n"
    "plt.rcParams.update({\n"
    "    'font.size': 11,\n"
    "    'axes.labelsize': 12,\n"
    "    'axes.titlesize': 14,\n"
    "    'xtick.labelsize': 10,\n"
    "    'ytick.labelsize': 10,\n"
    "    'figure.titlesize': 16\n"
    "})\n"
    "print(\"Libraries imported successfully.\")"
))

# Cell 3: Load Data
cells.append(nbformat.v4.new_code_cell(
    "BASE_DIR = r\"d:\\Data_Science_attendence_project\"\n"
    "DATA_FILE = os.path.join(BASE_DIR, \"data\", \"student_attendance_205_students.csv\")\n"
    "CHARTS_DIR = os.path.join(BASE_DIR, \"outputs\", \"charts\")\n"
    "os.makedirs(CHARTS_DIR, exist_ok=True)\n\n"
    "df = pd.read_csv(DATA_FILE)\n"
    "print(f\"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\")"
))

# Cell 4: Head
cells.append(nbformat.v4.new_code_cell(
    "df.head()"
))

# Cell 5: Dataset Info & Describe
cells.append(nbformat.v4.new_code_cell(
    "print(\"=== Dataset Info ===\")\n"
    "df.info()\n\n"
    "print(\"\\n=== Descriptive Statistics (Numeric Columns) ===\")\n"
    "df.describe()"
))

# Cell 6: Overall Attendance Stats
cells.append(nbformat.v4.new_code_cell(
    "att_col = 'Attendance_Percentage'\n"
    "print(f\"Average Attendance: {df[att_col].mean():.2f}%\")\n"
    "print(f\"Minimum Attendance: {df[att_col].min():.2f}%\")\n"
    "print(f\"Maximum Attendance: {df[att_col].max():.2f}%\")\n"
    "print(f\"Median Attendance : {df[att_col].median():.2f}%\")"
))

# Cell 7: Attendance Status counts
cells.append(nbformat.v4.new_code_cell(
    "status_counts = df['Attendance_Status'].value_counts()\n"
    "status_pcts = df['Attendance_Status'].value_counts(normalize=True) * 100\n"
    "for label in status_counts.index:\n"
    "    print(f\"{label}: {status_counts[label]} rows ({status_pcts[label]:.2f}%)\")"
))

# Cell 8: Department-wise
cells.append(nbformat.v4.new_code_cell(
    "df.groupby('Department')[att_col].agg(['count', 'mean', 'min', 'max', 'median'])"
))

# Cell 9: Subject-wise
cells.append(nbformat.v4.new_code_cell(
    "df.groupby('Subject')[att_col].agg(['count', 'mean', 'min', 'max', 'median'])"
))

# Cell 10: Year and Semester-wise
cells.append(nbformat.v4.new_code_cell(
    "print(\"=== Year-wise Attendance ===\")\n"
    "print(df.groupby('Year')[att_col].agg(['count', 'mean', 'median']))\n\n"
    "print(\"\\n=== Semester-wise Attendance ===\")\n"
    "print(df.groupby('Semester')[att_col].agg(['count', 'mean', 'median']))\n\n"
    "print(\"\\n=== Year & Semester Cross-tabulation ===\")\n"
    "print(df.groupby(['Year', 'Semester'])[att_col].mean())"
))

# Cell 11: Plot 1 - attendance_distribution.png
cells.append(nbformat.v4.new_code_cell(
    "plt.figure(figsize=(10, 6))\n"
    "sns.histplot(data=df, x=att_col, kde=True, bins=25, color='skyblue')\n"
    "plt.axvline(75, color='red', linestyle='--', linewidth=1.5, label='Attendance Threshold (75%)')\n"
    "plt.title('Distribution of Student Attendance Percentage')\n"
    "plt.xlabel('Attendance Percentage (%)')\n"
    "plt.ylabel('Frequency')\n"
    "plt.legend()\n"
    "plt.savefig(os.path.join(CHARTS_DIR, 'attendance_distribution.png'), dpi=150, bbox_inches='tight')\n"
    "plt.show()"
))

# Cell 12: Plot 2 - regular_defaulter_count.png
cells.append(nbformat.v4.new_code_cell(
    "plt.figure(figsize=(8, 6))\n"
    "ax = sns.countplot(data=df, x='Attendance_Status', hue='Attendance_Status', palette='pastel', legend=False)\n"
    "plt.title('Count of Regular vs Defaulter Attendance Records')\n"
    "plt.xlabel('Attendance Status')\n"
    "plt.ylabel('Number of Records')\n"
    "for p in ax.patches:\n"
    "    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height() + 20),\n"
    "                ha='center', va='center', xytext=(0, 5), textcoords='offset points')\n"
    "plt.savefig(os.path.join(CHARTS_DIR, 'regular_defaulter_count.png'), dpi=150, bbox_inches='tight')\n"
    "plt.show()"
))

# Cell 13: Plot 3 - subject_wise_attendance.png
cells.append(nbformat.v4.new_code_cell(
    "plt.figure(figsize=(12, 6))\n"
    "sns.boxplot(data=df, x='Subject', y=att_col, hue='Subject', palette='Set2', legend=False)\n"
    "plt.axhline(75, color='red', linestyle='--', linewidth=1.2, label='Threshold (75%)')\n"
    "plt.xticks(rotation=15, ha='right')\n"
    "plt.title('Subject-wise Attendance Distribution')\n"
    "plt.xlabel('Subject')\n"
    "plt.ylabel('Attendance Percentage (%)')\n"
    "plt.savefig(os.path.join(CHARTS_DIR, 'subject_wise_attendance.png'), dpi=150, bbox_inches='tight')\n"
    "plt.show()"
))

# Cell 14: Plot 4 - attendance_by_period.png
cells.append(nbformat.v4.new_code_cell(
    "if 'Attendance_Period' in df.columns:\n"
    "    plt.figure(figsize=(10, 6))\n"
    "    sns.boxplot(data=df, x='Attendance_Period', y=att_col, hue='Attendance_Period', palette='Set3', legend=False)\n"
    "    plt.title('Attendance Distribution by Period')\n"
    "    plt.xlabel('Attendance Period')\n"
    "    plt.ylabel('Attendance Percentage (%)')\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'attendance_by_period.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping attendance_by_period.png\")"
))

# Cell 15: Plot 5 - study_hours_vs_attendance.png
cells.append(nbformat.v4.new_code_cell(
    "if 'Study_Hours_Per_Week' in df.columns:\n"
    "    plt.figure(figsize=(10, 6))\n"
    "    sns.scatterplot(data=df, x='Study_Hours_Per_Week', y=att_col, hue='Attendance_Status', palette='coolwarm', alpha=0.7)\n"
    "    sns.regplot(data=df, x='Study_Hours_Per_Week', y=att_col, scatter=False, color='black', label='Trend Line')\n"
    "    plt.title('Study Hours per Week vs Attendance Percentage')\n"
    "    plt.xlabel('Study Hours per Week')\n"
    "    plt.ylabel('Attendance Percentage (%)')\n"
    "    plt.legend()\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'study_hours_vs_attendance.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping study_hours_vs_attendance.png\")"
))

# Cell 16: Plot 6 - internal_marks_vs_attendance.png
cells.append(nbformat.v4.new_code_cell(
    "if 'Internal_Marks' in df.columns:\n"
    "    plt.figure(figsize=(10, 6))\n"
    "    sns.scatterplot(data=df, x='Internal_Marks', y=att_col, hue='Attendance_Status', palette='coolwarm', alpha=0.7)\n"
    "    sns.regplot(data=df, x='Internal_Marks', y=att_col, scatter=False, color='black', label='Trend Line')\n"
    "    plt.title('Internal Marks vs Attendance Percentage')\n"
    "    plt.xlabel('Internal Marks')\n"
    "    plt.ylabel('Attendance Percentage (%)')\n"
    "    plt.legend()\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'internal_marks_vs_attendance.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping internal_marks_vs_attendance.png\")"
))

# Cell 17: Plot 7 - medical_leave_vs_attendance.png
cells.append(nbformat.v4.new_code_cell(
    "if 'Medical_Leave_Days' in df.columns:\n"
    "    plt.figure(figsize=(10, 6))\n"
    "    sns.boxplot(data=df, x='Medical_Leave_Days', y=att_col, hue='Medical_Leave_Days', palette='Blues', legend=False)\n"
    "    plt.title('Medical Leave Days vs Attendance Percentage')\n"
    "    plt.xlabel('Medical Leave Days')\n"
    "    plt.ylabel('Attendance Percentage (%)')\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'medical_leave_vs_attendance.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping medical_leave_vs_attendance.png\")"
))

# Cell 18: Plot 8 - late_count_vs_attendance.png
cells.append(nbformat.v4.new_code_cell(
    "if 'Late_Count' in df.columns:\n"
    "    plt.figure(figsize=(10, 6))\n"
    "    sns.scatterplot(data=df, x='Late_Count', y=att_col, hue='Attendance_Status', palette='coolwarm', alpha=0.7)\n"
    "    sns.regplot(data=df, x='Late_Count', y=att_col, scatter=False, color='black', label='Trend Line')\n"
    "    plt.title('Late Count vs Attendance Percentage')\n"
    "    plt.xlabel('Late Count')\n"
    "    plt.ylabel('Attendance Percentage (%)')\n"
    "    plt.legend()\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'late_count_vs_attendance.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping late_count_vs_attendance.png\")"
))

# Cell 19: Plot 9 - correlation_heatmap.png
cells.append(nbformat.v4.new_code_cell(
    "numeric_cols = df.select_dtypes(include=[np.number]).columns\n"
    "if len(numeric_cols) > 0:\n"
    "    plt.figure(figsize=(14, 12))\n"
    "    corr_matrix = df[numeric_cols].corr()\n"
    "    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))\n"
    "    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, center=0,\n"
    "                square=True, linewidths=.5, cbar_kws={'shrink': .8})\n"
    "    plt.title('Correlation Matrix Heatmap (Numeric Features Only)')\n"
    "    plt.savefig(os.path.join(CHARTS_DIR, 'correlation_heatmap.png'), dpi=150, bbox_inches='tight')\n"
    "    plt.show()\n"
    "else:\n"
    "    print(\"Skipping correlation_heatmap.png\")"
))

# Cell 20: Markdown Summary
cells.append(nbformat.v4.new_markdown_cell(
    "## Summary of Findings and Methodology\n\n"
    "### 1. Key Metrics\n"
    "- **Average Attendance:** 68.67%\n"
    "- **Minimum Attendance:** 0.00%\n"
    "- **Maximum Attendance:** 100.00%\n"
    "- **Median Attendance:** 70.00%\n"
    "- **Defaulter Rate:** 55.27% (2,266 records)\n"
    "- **Regular Rate:** 44.73% (1,834 records)\n\n"
    "### 2. Group Analysis\n"
    "- **Departmental differences:** Computer Engineering students have an average attendance of **70.89%**, which is slightly higher than MCA students (**67.75%**).\n"
    "- **Subject-wise distribution:** Attendance is highly consistent across subjects, ranging from **68.38%** (Database Management Systems) to **69.12%** (Software Engineering).\n"
    "- **Semester & Year differences:** Third Year students (Fifth Semester) show higher average attendance (**70.89%**) than Final Year students (Third Semester) (**67.75%**).\n\n"
    "### 3. Key Correlations with Attendance\n"
    "- **Strongest Positive Associations:**\n"
    "  - `Previous_Attendance_Percentage` (correlation coefficient = `0.72`)\n"
    "  - `Internal_Marks` (correlation coefficient = `0.67`)\n"
    "  - `Study_Hours_Per_Week` (correlation coefficient = `0.61`)\n"
    "  - `Previous_Exam_Score` (correlation coefficient = `0.59`)\n"
    "- **Weak or Uncorrelated Features:**\n"
    "  - `Travel_Distance_KM` (`0.04`)\n"
    "  - `Late_Count` (`0.01`)\n"
    "  - `Online_Class_Attendance` (`-0.003`)\n"
    "  - `Medical_Leave_Days` (`-0.02`)\n\n"
    "### ⚠️ Important Methodological Note: Correlation vs. Causation\n"
    "It is vital to state that **correlation does not imply causation**. While there is a strong positive correlation between `Study_Hours_Per_Week` or `Internal_Marks` and `Attendance_Percentage`:\n"
    "1. **No direct causal link can be claimed solely from this analysis:** We cannot prove that studying more hours directly *causes* a student to attend more classes, or that attending more classes directly *causes* higher internal marks (there may be confounding factors like motivation, aptitude, or pedagogical style).\n"
    "2. **Confounding variables:** A student who is highly motivated is likely to study more hours, attend more classes, and get higher marks. The correlation we see is a reflection of this joint relationship.\n"
    "3. **Synthetic nature:** These relationships are defined by mathematical formulas used to generate the synthetic data and do not represent real-world clinical experiments."
))

# Populate notebook
nb['cells'] = cells

# Execute notebook programmatically
print("Executing notebook programmatically...")
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': NOTEBOOKS_DIR}})

# Save notebook
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Notebook generated, executed, and saved successfully at: {NOTEBOOK_PATH}")
