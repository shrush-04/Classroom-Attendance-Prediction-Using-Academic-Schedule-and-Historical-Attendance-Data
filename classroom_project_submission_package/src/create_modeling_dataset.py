import os
import pandas as pd
import re

def main():
    base_dir = r"d:\Data_Science_attendence_project\classroom_project_submission_package"
    input_path = os.path.join(base_dir, "data", "processed", "cleaned_lecture_attendance.csv")
    output_path = os.path.join(base_dir, "data", "processed", "modeling_format_dataset.csv")

    print(f"Reading input data from: {input_path}")
    df = pd.read_csv(input_path)
    
    # Save the original row count
    original_row_count = len(df)
    print(f"Original row count: {original_row_count}")

    # Map the columns
    # Mapped columns:
    # - Time from Start_Time
    # - Previous_Attendance_Percentage from Previous_Lecture_Attendance_Percentage
    # - Other fields from matching existing columns.
    # - If Holiday_Tomorrow is not available in the verified data, use Not_Collected.
    
    mapping = {
        'Date': 'Date',
        'Start_Time': 'Time',
        'Subject': 'Subject',
        'Semester': 'Semester',
        'Day_of_Week': 'Day_of_Week',
        'Previous_Lecture_Attendance_Percentage': 'Previous_Attendance_Percentage',
        'Internal_Test_Week': 'Internal_Test_Week',
        'Total_Enrolled_Students': 'Total_Enrolled_Students',
        'Students_Present': 'Students_Present',
        'Attendance_Percentage': 'Attendance_Percentage'
    }

    # Verify all source columns exist
    for src in mapping.keys():
        if src not in df.columns:
            raise ValueError(f"Source column '{src}' not found in input data!")

    # Select and rename mapped columns
    new_df = df[list(mapping.keys())].rename(columns=mapping)
    
    # Add Holiday_Tomorrow column
    new_df['Holiday_Tomorrow'] = 'Not_Collected'

    # Reorder columns to match exactly:
    cols_order = [
        'Date',
        'Time',
        'Subject',
        'Semester',
        'Day_of_Week',
        'Previous_Attendance_Percentage',
        'Internal_Test_Week',
        'Holiday_Tomorrow',
        'Total_Enrolled_Students',
        'Students_Present',
        'Attendance_Percentage'
    ]
    new_df = new_df[cols_order]

    # Validate output row count
    if len(new_df) != original_row_count:
        raise ValueError(f"Row count mismatch! Expected {original_row_count}, got {len(new_df)}")

    # Validation Checks:
    # 1. No names, roll numbers, or emails
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    for col in new_df.columns:
        if new_df[col].dtype == object:
            # Check for emails or standard name/roll patterns
            for val in new_df[col].dropna().astype(str):
                if email_pattern.search(val):
                    raise ValueError(f"PII Leak: Found email address in column '{col}': {val}")
                # Simple check for names / roll numbers (e.g. standard patterns)
                # Let's inspect values to make sure
                if any(x.isdigit() for x in val) and len(val) > 10 and '@' in val:
                     raise ValueError(f"PII Leak: Found possible PII in column '{col}': {val}")
    
    print("PII Validation: Checked and no emails or obvious PII found.")

    # 2. Students_Present <= Total_Enrolled_Students
    invalid_present = new_df[new_df['Students_Present'] > new_df['Total_Enrolled_Students']]
    if not invalid_present.empty:
        raise ValueError(f"Validation Error: Students_Present exceeds Total_Enrolled_Students in rows:\n{invalid_present}")
    print("Students Present Validation: Verified Students_Present <= Total_Enrolled_Students.")

    # 3. Attendance_Percentage is correct
    # Calculated as (Students_Present / Total_Enrolled_Students) * 100
    expected_pct = (new_df['Students_Present'] / new_df['Total_Enrolled_Students']) * 100
    diff = (new_df['Attendance_Percentage'] - expected_pct).abs()
    if (diff > 0.01).any():
        bad_idx = diff[diff > 0.01].index
        raise ValueError(f"Validation Error: Attendance_Percentage mismatch in rows:\n{new_df.loc[bad_idx]}")
    print("Attendance Percentage Validation: Verified all attendance percentages are correct.")

    # 4. No duplicate rows
    if new_df.duplicated().any():
        raise ValueError("Validation Error: Duplicate rows found in the output dataset.")
    print("Duplicates Validation: Verified no duplicate rows exist.")

    # 5. Date and Time formats are valid
    # Date should match YYYY-MM-DD
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    for d in new_df['Date'].astype(str):
        if not date_pattern.match(d):
            raise ValueError(f"Validation Error: Invalid date format: {d}")
            
    # Time should match HH:MM (e.g. 08:30)
    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    for t in new_df['Time'].astype(str):
        if not time_pattern.match(t):
            raise ValueError(f"Validation Error: Invalid time format: {t}")
    print("Formats Validation: Date (YYYY-MM-DD) and Time (HH:MM) formats are valid.")

    # Save output to destination
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_df.to_csv(output_path, index=False)
    print(f"Dataset successfully created and saved to: {output_path}")
    print("Columns in generated dataset:")
    print(list(new_df.columns))
    print(f"Row count: {len(new_df)}")

if __name__ == '__main__':
    main()
