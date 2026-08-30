import pandas as pd
import numpy as np
import os
import sys

def clean_data(input_path, output_path=None):
    """
    Cleans raw lecture attendance data.
    Standardizes categorical entries, formats columns, documents missing values.
    Saves cleaned data to data/processed/cleaned_lecture_attendance.csv.
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(os.path.dirname(input_path)), "processed", "cleaned_lecture_attendance.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print(f"Reading file for cleaning: {input_path}...")
    if input_path.endswith('.xlsx') or input_path.endswith('.xls'):
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    # 1. Standardize types
    df['Lecture_ID'] = df['Lecture_ID'].astype(str).str.strip()
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    df['Day_of_Week'] = df['Day_of_Week'].astype(str).str.strip().str.capitalize()
    df['Subject'] = df['Subject'].astype(str).str.strip()
    df['Faculty_ID'] = df['Faculty_ID'].astype(str).str.strip().str.upper()
    df['Semester'] = df['Semester'].astype(str).str.strip()
    df['Branch'] = df['Branch'].astype(str).str.strip().str.upper()
    df['Section'] = df['Section'].astype(str).str.strip().str.upper()
    df['Classroom'] = df['Classroom'].astype(str).str.strip()
    df['Practical_Theory'] = df['Practical_Theory'].astype(str).str.strip().str.capitalize()
    
    # Numeric conversions
    df['Lecture_Number'] = df['Lecture_Number'].astype(int)
    df['Total_Enrolled_Students'] = df['Total_Enrolled_Students'].astype(int)
    df['Students_Present'] = df['Students_Present'].astype(int)
    df['Attendance_Percentage'] = df['Attendance_Percentage'].astype(float)
    df['Internal_Test_Week'] = df['Internal_Test_Week'].astype(int)
    df['Assignment_Due'] = df['Assignment_Due'].astype(int)

    # 2. Document missing values in optional columns
    # We will look for missing values in optional columns and standardize them as 'Not_Collected' or NaN
    optional_cols = [
        "Previous_Lecture_Attendance_Percentage", 
        "Gap_Since_Previous_Lecture_Hours", 
        "Weather", 
        "Special_Event"
    ]
    
    missing_report = []
    for col in optional_cols:
        if col in df.columns:
            # Mark various empty values as standard nulls or 'Not_Collected'
            df[col] = df[col].replace(['', ' ', 'nan', 'NAN', 'None', 'null', 'Not_Collected'], np.nan)
            null_count = df[col].isnull().sum()
            if null_count > 0:
                missing_report.append(f"Column '{col}': {null_count} missing values. Reason: Optional academic/environmental field not logged at lecture time.")
                # For categorical columns, we can fill with "Not_Collected"
                if df[col].dtype == object or col in ["Weather", "Special_Event"]:
                    df[col] = df[col].fillna("Not_Collected")
                # For numerical columns, we leave as NaN, to be handled by ML Imputers
        else:
            missing_report.append(f"Column '{col}': Column is completely absent in raw input.")
            df[col] = np.nan if col in ["Previous_Lecture_Attendance_Percentage", "Gap_Since_Previous_Lecture_Hours"] else "Not_Collected"

    # Save missing values audit report
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(output_path)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    audit_report_path = os.path.join(outputs_dir, "missing_values_audit.txt")
    with open(audit_report_path, 'w', encoding='utf-8') as f:
        f.write("MISSING VALUES LOG & ETHICAL AUDIT\n")
        f.write("==================================\n\n")
        f.write("In compliance with academic data constraints, missing data is documented rather than fabricated.\n\n")
        for log in missing_report:
            f.write(f"- {log}\n")

    # 3. Double check calculations
    df['Attendance_Percentage'] = (df['Students_Present'] / df['Total_Enrolled_Students'] * 100).round(2)

    # 4. Standardize Holiday_Before_After
    if 'Holiday_Before_After' in df.columns:
        df['Holiday_Before_After'] = df['Holiday_Before_After'].replace(['', ' ', 'nan', 'NAN', 'None', 'null'], 'None')
        df['Holiday_Before_After'] = df['Holiday_Before_After'].fillna('None').astype(str).str.strip()

    # Save cleaned file
    df.to_csv(output_path, index=False)
    print(f"Data cleaning completed. Cleaned dataset saved to: {output_path}")
    print(f"Missing values log written to: {audit_report_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_data.py <path_to_raw_data>")
        sys.exit(1)
    raw_path = sys.argv[1]
    clean_data(raw_path)
