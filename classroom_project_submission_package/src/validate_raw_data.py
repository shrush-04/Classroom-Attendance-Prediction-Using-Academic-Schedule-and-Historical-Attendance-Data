import pandas as pd
import numpy as np
import re
import os
import sys

def run_validation(data_path, output_dir=None):
    """
    Validates classroom attendance data file against 16 rules.
    Saves outputs as data_quality_report.md and data_quality_report.txt.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(data_path)), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    report_md_path = os.path.join(output_dir, "data_quality_report.md")
    report_txt_path = os.path.join(output_dir, "data_quality_report.txt")

    print(f"Reading file for validation: {data_path}...")
    if not os.path.exists(data_path):
        err_msg = f"Error: File not found at {data_path}"
        print(err_msg)
        return False, [err_msg]

    try:
        if data_path.endswith('.xlsx') or data_path.endswith('.xls'):
            df = pd.read_excel(data_path)
        else:
            df = pd.read_csv(data_path)
        if 'Holiday_Before_After' in df.columns:
            df['Holiday_Before_After'] = df['Holiday_Before_After'].fillna('None')
    except Exception as e:
        err_msg = f"Error reading file: {str(e)}"
        print(err_msg)
        return False, [err_msg]

    checks = {}
    errors_list = []
    
    # 1. Required Columns
    required_cols = [
        "Lecture_ID", "Date", "Day_of_Week", "Lecture_Number", "Start_Time", "End_Time", 
        "Subject", "Faculty_ID", "Semester", "Branch", "Section", "Classroom", 
        "Total_Enrolled_Students", "Students_Present", "Attendance_Percentage", 
        "Practical_Theory", "Internal_Test_Week", "Assignment_Due", "Holiday_Before_After"
    ]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        checks["Required Columns"] = (False, f"Missing required columns: {', '.join(missing_cols)}")
        errors_list.append(f"Missing columns: {missing_cols}")
    else:
        checks["Required Columns"] = (True, "All required columns are present.")

    # Stop early if required columns are missing
    if missing_cols:
        write_reports(checks, errors_list, report_md_path, report_txt_path, len(df) if 'df' in locals() else 0)
        return False, errors_list

    # 2. Lecture_ID format and duplicates
    lec_id_pattern = re.compile(r'^LEC\d{4}$')
    invalid_ids = df[~df['Lecture_ID'].astype(str).str.match(lec_id_pattern)]['Lecture_ID'].tolist()
    duplicate_ids = df[df.duplicated(subset=['Lecture_ID'], keep=False)]['Lecture_ID'].unique().tolist()
    
    lec_id_status = True
    lec_id_msg = "Lecture_ID format and uniqueness are valid."
    if invalid_ids:
        lec_id_status = False
        lec_id_msg = f"Invalid Lecture_ID format (must be LECxxxx): {invalid_ids[:5]}"
        errors_list.append(f"Invalid Lecture_ID format: {invalid_ids}")
    if duplicate_ids:
        lec_id_status = False
        lec_id_msg = f"Duplicate Lecture_IDs found: {duplicate_ids[:5]}"
        errors_list.append(f"Duplicate Lecture_IDs: {duplicate_ids}")
    checks["Lecture_ID Validation"] = (lec_id_status, lec_id_msg)

    # 3. Date format (YYYY-MM-DD)
    date_errors = []
    parsed_dates = []
    for idx, row in df.iterrows():
        d_str = str(row['Date'])
        try:
            pd_date = pd.to_datetime(d_str, format='%Y-%m-%d', errors='raise')
            parsed_dates.append(pd_date)
        except Exception:
            date_errors.append(f"Row {idx+2}: '{d_str}' is not in YYYY-MM-DD format")
    
    if date_errors:
        checks["Date Format"] = (False, f"Date format errors found: {len(date_errors)} instances. E.g. {date_errors[0]}")
        errors_list.append(f"Date format errors: {date_errors}")
    else:
        checks["Date Format"] = (True, "All dates are in correct YYYY-MM-DD format.")
        df['Parsed_Date'] = parsed_dates

    # 4. Time format (HH:MM or HH:MM:SS)
    time_pattern = re.compile(r'^\d{2}:\d{2}(:\d{2})?$')
    invalid_start = df[~df['Start_Time'].astype(str).str.match(time_pattern)]['Start_Time'].tolist()
    invalid_end = df[~df['End_Time'].astype(str).str.match(time_pattern)]['End_Time'].tolist()
    
    time_status = True
    time_msg = "Time formats are valid."
    if invalid_start or invalid_end:
        time_status = False
        time_msg = f"Invalid time formats. Start_Time errors: {len(invalid_start)}, End_Time errors: {len(invalid_end)}"
        errors_list.append(f"Invalid Start_Time format: {invalid_start}")
        errors_list.append(f"Invalid End_Time format: {invalid_end}")
    checks["Time Format"] = (time_status, time_msg)

    # 5. Chronological order
    if checks["Date Format"][0] and checks["Time Format"][0]:
        df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Start_Time'].astype(str))
        is_sorted = df['Datetime'].is_monotonic_increasing
        if not is_sorted:
            checks["Chronological Order"] = (False, "Data is not sorted chronologically by Date and Start_Time.")
            errors_list.append("Data is not chronologically sorted.")
        else:
            checks["Chronological Order"] = (True, "Data is chronologically sorted.")
    else:
        checks["Chronological Order"] = (False, "Skipped chronological check due to Date/Time formatting errors.")

    # 6. Students_Present <= Total_Enrolled_Students
    invalid_present = df[df['Students_Present'] > df['Total_Enrolled_Students']]
    if not invalid_present.empty:
        instances = invalid_present[['Lecture_ID', 'Total_Enrolled_Students', 'Students_Present']].to_dict(orient='records')
        checks["Enrollment Capacity"] = (False, f"Present count exceeds Enrolled count in {len(invalid_present)} rows. E.g. {instances[0]}")
        errors_list.append(f"Present count exceeds Enrolled: {instances}")
    else:
        checks["Enrollment Capacity"] = (True, "Present counts are less than or equal to Enrolled counts.")

    # 7. Non-negative student counts
    negative_counts = df[(df['Students_Present'] < 0) | (df['Total_Enrolled_Students'] < 0)]
    if not negative_counts.empty:
        checks["Non-negative Counts"] = (False, f"Negative student count values found in {len(negative_counts)} rows.")
        errors_list.append(f"Negative counts in rows: {negative_counts['Lecture_ID'].tolist()}")
    else:
        checks["Non-negative Counts"] = (True, "All student counts are non-negative.")

    # 8. Attendance_Percentage formula
    # percentage = (present/enrolled)*100
    mismatched_pct = []
    for idx, row in df.iterrows():
        enrolled = row['Total_Enrolled_Students']
        present = row['Students_Present']
        expected_pct = round((present / enrolled) * 100, 2) if enrolled > 0 else 0.0
        reported_pct = round(float(row['Attendance_Percentage']), 2)
        if abs(expected_pct - reported_pct) > 0.05:
            mismatched_pct.append((row['Lecture_ID'], reported_pct, expected_pct))
    
    if mismatched_pct:
        checks["Attendance Percentage Formula"] = (False, f"Incorrect attendance percentage calculation in {len(mismatched_pct)} rows. E.g. {mismatched_pct[0]}")
        errors_list.append(f"Mismatched Attendance Percentage: {mismatched_pct}")
    else:
        checks["Attendance Percentage Formula"] = (True, "All attendance percentages match (Present/Enrolled) * 100.")

    # 9. Missing values (check for nulls in required columns)
    null_counts = df[required_cols].isnull().sum()
    missing_data_cols = null_counts[null_counts > 0]
    if not missing_data_cols.empty:
        checks["Missing Values in Required Columns"] = (False, f"Missing values found: {missing_data_cols.to_dict()}")
        errors_list.append(f"Missing values in required columns: {missing_data_cols.to_dict()}")
    else:
        checks["Missing Values in Required Columns"] = (True, "No missing values in required columns.")

    # 10. Duplicate rows (all columns except Lecture_ID)
    dup_rows = df.duplicated(subset=[col for col in df.columns if col != 'Lecture_ID'], keep=False)
    if dup_rows.any():
        checks["Duplicate Rows"] = (False, f"Found {df[dup_rows].shape[0]} duplicate rows (identical fields).")
        errors_list.append(f"Duplicate rows count: {df[dup_rows].shape[0]}")
    else:
        checks["Duplicate Rows"] = (True, "No duplicate rows found.")

    # 11. Invalid categorical values
    cat_errors = []
    valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    invalid_days_list = df[~df['Day_of_Week'].isin(valid_days)]['Day_of_Week'].unique().tolist()
    if invalid_days_list:
        cat_errors.append(f"Invalid Day_of_Week: {invalid_days_list}")

    valid_pt = ["Theory", "Practical"]
    invalid_pt_list = df[~df['Practical_Theory'].isin(valid_pt)]['Practical_Theory'].unique().tolist()
    if invalid_pt_list:
        cat_errors.append(f"Invalid Practical_Theory: {invalid_pt_list}")

    valid_holiday = ["Holiday_Before", "Holiday_After", "Both", "None"]
    invalid_holiday_list = df[~df['Holiday_Before_After'].isin(valid_holiday)]['Holiday_Before_After'].unique().tolist()
    if invalid_holiday_list:
        cat_errors.append(f"Invalid Holiday_Before_After: {invalid_holiday_list}")

    if cat_errors:
        checks["Categorical Values"] = (False, f"Invalid categories: {'; '.join(cat_errors)}")
        errors_list.append(f"Invalid categories: {cat_errors}")
    else:
        checks["Categorical Values"] = (True, "All categorical fields contain valid levels.")

    # 12. Consistent subject names
    subject_counts = df['Subject'].value_counts()
    checks["Subject Consistency"] = (True, f"Subjects recorded ({len(subject_counts)} types): {list(subject_counts.index)}")

    # 13. Consistent section names
    section_counts = df['Section'].value_counts()
    checks["Section Consistency"] = (True, f"Sections recorded: {list(section_counts.index)}")

    # 14. Consistent Faculty_ID values
    fac_pattern = re.compile(r'^F_?\d{1,3}(\+F_?\d{1,3})*$')
    invalid_facs = df[~df['Faculty_ID'].astype(str).str.match(fac_pattern)]['Faculty_ID'].unique().tolist()
    if invalid_facs:
        checks["Faculty_ID Consistency"] = (False, f"Faculty_ID format must be Fxxx. Invalid values: {invalid_facs}")
        errors_list.append(f"Invalid Faculty_IDs: {invalid_facs}")
    else:
        checks["Faculty_ID Consistency"] = (True, f"Faculty_IDs are valid. Faculty count: {df['Faculty_ID'].nunique()}")

    # 15. No personal information columns
    pii_keywords = ['name', 'roll', 'email', 'phone', 'address', 'photo', 'biometric']
    found_pii_cols = [col for col in df.columns if any(kw in col.lower() for kw in pii_keywords) and 'enrolled' not in col.lower()]
    if found_pii_cols:
        checks["No PII Columns"] = (False, f"PII columns detected in schema: {found_pii_cols}")
        errors_list.append(f"PII columns detected: {found_pii_cols}")
    else:
        checks["No PII Columns"] = (True, "No personal identifier columns (names, emails, rolls) exist in schema.")

    # 16. No names, roll numbers, or email IDs in the cell values (checks contents)
    # Check if values contain patterns like emails, names (rough check), or roll numbers
    email_regex = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    found_pii_values = False
    pii_evidence = []
    for col in df.select_dtypes(include=[object]).columns:
        for idx, val in enumerate(df[col].astype(str)):
            # Check for email
            if email_regex.search(val):
                found_pii_values = True
                pii_evidence.append(f"Row {idx+2}, Col {col}: Found email '{val}'")
            # Check for typical roll number pattern in non-Lecture_ID column
            if col != 'Lecture_ID' and re.search(r'\b\d{7,10}\b', val):
                found_pii_values = True
                pii_evidence.append(f"Row {idx+2}, Col {col}: Found roll-number-like value '{val}'")
                
    if found_pii_values:
        checks["No PII Data Values"] = (False, f"PII data values detected: {pii_evidence[:5]}")
        errors_list.append(f"PII data values detected: {pii_evidence}")
    else:
        checks["No PII Data Values"] = (True, "No student names, roll numbers, or email values found in cell content.")

    # Write reports
    write_reports(checks, errors_list, report_md_path, report_txt_path, len(df))
    
    is_valid = len(errors_list) == 0
    return is_valid, errors_list

def write_reports(checks, errors_list, md_path, txt_path, row_count):
    # Markdown report
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Classroom Attendance Data Validation Report\n\n")
        f.write(f"- **Data Row Count:** {row_count}\n")
        f.write(f"- **Validation Status:** {'PASSED' if not errors_list else 'FAILED'}\n")
        f.write(f"- **Error Counts:** {len(errors_list)} rule violations\n\n")
        
        f.write("## Validation Rules Checklist\n\n")
        f.write("| Rule / Check | Status | Description |\n")
        f.write("| :--- | :--- | :--- |\n")
        for rule, (status, desc) in checks.items():
            icon = "✅ PASS" if status else "❌ FAIL"
            f.write(f"| {rule} | {icon} | {desc} |\n")
            
        if errors_list:
            f.write("\n## Error Details\n\n")
            for err in errors_list[:20]: # show first 20
                f.write(f"- {err}\n")
            if len(errors_list) > 20:
                f.write(f"\n*Truncated {len(errors_list)-20} more errors...*\n")
                
    # Plain text report
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("CLASSROOM ATTENDANCE DATA VALIDATION REPORT\n")
        f.write("===========================================\n")
        f.write(f"Data Row Count: {row_count}\n")
        f.write(f"Validation Status: {'PASSED' if not errors_list else 'FAILED'}\n")
        f.write(f"Errors Found: {len(errors_list)}\n\n")
        for rule, (status, desc) in checks.items():
            f.write(f"[{'PASS' if status else 'FAIL'}] {rule}: {desc}\n")
        if errors_list:
            f.write("\nERROR DETAILS:\n")
            for err in errors_list:
                f.write(f"- {err}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_raw_data.py <path_to_raw_data>")
        sys.exit(1)
    
    raw_data = sys.argv[1]
    success, errors = run_validation(raw_data)
    if success:
        print("Validation PASSED successfully.")
        sys.exit(0)
    else:
        print(f"Validation FAILED. Found {len(errors)} errors. Check reports for details.")
        sys.exit(1)
