import os
import pandas as pd
import datetime

def get_holiday_proximity(date_obj, holiday_dates):
    # holiday_dates is a set of datetime.date objects
    yesterday = date_obj - datetime.timedelta(days=1)
    tomorrow = date_obj + datetime.timedelta(days=1)
    
    is_after = yesterday in holiday_dates
    is_before = tomorrow in holiday_dates
    
    if is_before and is_after:
        return 'Both'
    elif is_before:
        return 'Holiday_Before'
    elif is_after:
        return 'Holiday_After'
    else:
        return 'None'

def main():
    base_dir = r"d:\Data_Science_attendence_project\classroom_project_submission_package"
    
    # 1. Configuration
    START_DATE = datetime.date(2026, 6, 25)
    END_DATE = datetime.date(2026, 8, 25)
    
    # Verified Holidays
    holidays = {
        datetime.date(2026, 6, 26), # Friday
        datetime.date(2026, 7, 24), # Friday
        datetime.date(2026, 7, 25), # Saturday
        datetime.date(2026, 8, 11)  # Tuesday (holiday/exam day)
    }

    # 2. Paths
    timetable_path = os.path.join(base_dir, "data", "raw", "timetable_structured.csv")
    cleaned_data_path = os.path.join(base_dir, "data", "processed", "cleaned_lecture_attendance.csv")
    
    template_csv_path = os.path.join(base_dir, "data", "templates", "two_month_lecture_collection_template.csv")
    template_xlsx_path = os.path.join(base_dir, "data", "templates", "two_month_lecture_collection_template.xlsx")
    collection_csv_path = os.path.join(base_dir, "data", "raw", "two_month_lecture_attendance_collection.csv")
    report_path = os.path.join(base_dir, "outputs", "two_month_schedule_coverage_report.md")

    # 3. Load input data
    timetable_df = pd.read_csv(timetable_path)
    cleaned_df = pd.read_csv(cleaned_data_path)
    
    # Standardize observed dates
    cleaned_df['Date_parsed'] = pd.to_datetime(cleaned_df['Date']).dt.date
    
    # Create dictionary of observed data for fast lookup by (Date, Lecture_Number, Subject)
    observed_map = {}
    for _, row in cleaned_df.iterrows():
        key = (row['Date_parsed'], int(row['Lecture_Number']), row['Subject'].strip())
        observed_map[key] = row

    # 4. Generate the full scheduled rows list
    all_rows = []
    current_date = START_DATE
    
    # Track statistics for report
    total_holidays_excluded = 0
    
    while current_date <= END_DATE:
        # Check if Sunday
        if current_date.weekday() == 6:  # 6 is Sunday
            current_date += datetime.timedelta(days=1)
            continue
            
        # Check if holiday
        if current_date in holidays:
            total_holidays_excluded += 1
            current_date += datetime.timedelta(days=1)
            continue
            
        day_name = current_date.strftime('%A')
        
        # Get timetable slots for this day of the week
        slots = timetable_df[timetable_df['Day_of_Week'].str.strip().str.capitalize() == day_name].copy()
        
        if not slots.empty:
            # Sort slots by Lecture_Number
            slots = slots.sort_values(by='Lecture_Number')
            
            for _, slot in slots.iterrows():
                lecture_num = int(slot['Lecture_Number'])
                subject = slot['Subject'].strip()
                
                # Check if this slot was observed in register data
                key = (current_date, lecture_num, subject)
                
                # Default timetable details
                row_dict = {
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Day_of_Week': day_name,
                    'Lecture_Number': lecture_num,
                    'Start_Time': slot['Start_Time'],
                    'End_Time': slot['End_Time'],
                    'Subject': subject,
                    'Faculty_ID': slot['Faculty_ID'] if pd.notna(slot['Faculty_ID']) and slot['Faculty_ID'] != 'NULL' else 'Not_Assigned',
                    'Semester': 'Third Semester' if slot['Semester'] == 'III' else slot['Semester'],
                    'Branch': slot['Branch'],
                    'Section': slot['Section'],
                    'Classroom': slot['Classroom'],
                    'Total_Enrolled_Students': 80,  # Cohort size is 80
                    'Students_Present': None,
                    'Attendance_Percentage': None,
                    'Previous_Lecture_Attendance_Percentage': None,
                    'Gap_Since_Previous_Lecture_Hours': None,
                    'Practical_Theory': 'Practical' if 'practical' in subject.lower() or 'lab' in slot['Classroom'].lower() else 'Theory',
                    'Internal_Test_Week': 0,
                    'Assignment_Due': 0,
                    'Holiday_Before_After': get_holiday_proximity(current_date, holidays),
                    'Holiday_Tomorrow': 'Not_Collected',
                    'Weather': 'Not_Collected',
                    'Special_Event': 'Not_Collected',
                    'Attendance_Record_Status': 'Pending Register Verification',
                    'Source_Timetable': 'timetable_structured.csv',
                    'Source_Attendance_Register': 'None'
                }
                
                # If observed register entry exists, populate actual values
                if key in observed_map:
                    obs = observed_map[key]
                    row_dict['Students_Present'] = int(obs['Students_Present'])
                    row_dict['Attendance_Percentage'] = round((obs['Students_Present'] / 80) * 100, 2)
                    row_dict['Previous_Lecture_Attendance_Percentage'] = obs['Previous_Lecture_Attendance_Percentage'] if pd.notna(obs['Previous_Lecture_Attendance_Percentage']) else None
                    row_dict['Gap_Since_Previous_Lecture_Hours'] = obs['Gap_Since_Previous_Lecture_Hours'] if pd.notna(obs['Gap_Since_Previous_Lecture_Hours']) else None
                    row_dict['Internal_Test_Week'] = int(obs['Internal_Test_Week']) if pd.notna(obs['Internal_Test_Week']) else 0
                    row_dict['Assignment_Due'] = int(obs['Assignment_Due']) if pd.notna(obs['Assignment_Due']) else 0
                    row_dict['Weather'] = obs['Weather'] if pd.notna(obs['Weather']) else 'Not_Collected'
                    row_dict['Special_Event'] = obs['Special_Event'] if pd.notna(obs['Special_Event']) else 'Not_Collected'
                    row_dict['Holiday_Before_After'] = obs['Holiday_Before_After'] if pd.notna(obs['Holiday_Before_After']) else row_dict['Holiday_Before_After']
                    row_dict['Attendance_Record_Status'] = 'Verified from Register'
                    row_dict['Source_Attendance_Register'] = 'cleaned_lecture_attendance.csv'
                
                all_rows.append(row_dict)
                
        current_date += datetime.timedelta(days=1)

    # 5. Create DataFrames
    full_schedule_df = pd.DataFrame(all_rows)
    
    # Generate sequential Lecture_ID
    full_schedule_df.insert(0, 'Lecture_ID', [f"LEC{i+1:04d}" for i in range(len(full_schedule_df))])

    # 6. Save files
    os.makedirs(os.path.dirname(template_csv_path), exist_ok=True)
    os.makedirs(os.path.dirname(collection_csv_path), exist_ok=True)
    
    # 6a. Create template file (all register fields blank, status Pending Register Verification)
    template_df = full_schedule_df.copy()
    template_df['Students_Present'] = None
    template_df['Attendance_Percentage'] = None
    template_df['Previous_Lecture_Attendance_Percentage'] = None
    template_df['Gap_Since_Previous_Lecture_Hours'] = None
    template_df['Attendance_Record_Status'] = 'Pending Register Verification'
    template_df['Source_Attendance_Register'] = 'None'
    
    template_df.to_csv(template_csv_path, index=False)
    template_df.to_excel(template_xlsx_path, index=False)
    print(f"Template files saved to:\n  - CSV: {template_csv_path}\n  - Excel: {template_xlsx_path}")

    # 6b. Save final collection file (retaining both observed verified and pending blank rows)
    full_schedule_df.to_csv(collection_csv_path, index=False)
    print(f"Collection file saved to: {collection_csv_path}")

    # 7. Collect statistics for coverage report
    total_lectures = len(full_schedule_df)
    verified_count = len(full_schedule_df[full_schedule_df['Attendance_Record_Status'] == 'Verified from Register'])
    pending_count = len(full_schedule_df[full_schedule_df['Attendance_Record_Status'] == 'Pending Register Verification'])
    
    subjects_list = full_schedule_df['Subject'].unique().tolist()
    sections_list = full_schedule_df['Section'].unique().tolist()
    
    lectures_per_subject = full_schedule_df['Subject'].value_counts().to_dict()
    
    dates_requiring_register = full_schedule_df[
        full_schedule_df['Attendance_Record_Status'] == 'Pending Register Verification'
    ]['Date'].unique().tolist()
    
    # 8. Generate report
    report_content = f"""# Schedule Coverage and Verification Report

**Configured Date Range:** {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}

---

## 1. Summary Statistics

| Statistic | Value |
| :--- | :--- |
| **Total Scheduled Lectures** | {total_lectures} |
| **Verified Attendance Records** | {verified_count} |
| **Pending Register Verification** | {pending_count} |
| **Holidays Excluded** | {total_holidays_excluded} (Sundays excluded automatically) |
| **Unique Subjects** | {len(subjects_list)} |
| **Unique Sections** | {len(sections_list)} |

---

## 2. Subject-wise Lecture Breakdown

| Subject | Lecture Count |
| :--- | :--- |
"""
    for sub, count in lectures_per_subject.items():
        report_content += f"| {sub} | {count} |\n"
        
    report_content += f"""
---

## 3. List of Dates Requiring Register Entry

Below are the dates within the range that have scheduled lectures requiring manual physical register verification:

"""
    for dt in sorted(dates_requiring_register):
        # Find which subjects are scheduled on this date
        day_subjects = full_schedule_df[full_schedule_df['Date'] == dt]['Subject'].unique().tolist()
        report_content += f"- **{dt}**: {', '.join(day_subjects)}\n"

    report_content += """
---

> [!WARNING]
> ## Scientific Validity and Machine Learning Guidelines
> **Timetable-only rows (status: `Pending Register Verification`) MUST NOT be used for training or evaluating machine-learning models.** These rows represent future or unverified schedules and lack observed attendance metrics (`Students_Present` and `Attendance_Percentage`).
> Using fabricated, estimated, or randomly populated attendance values will compromise model validity and result in scientific errors. Only rows marked as `Verified from Register` may be used for modeling.
"""
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"Report written to: {report_path}")

    # Output parameters for next steps
    print(f"SCHEDULE_ROWS_CREATED: {total_lectures}")
    print(f"VERIFIED_ROWS: {verified_count}")
    print(f"PENDING_ROWS: {pending_count}")
    print(f"HOLIDAYS_EXCLUDED: {total_holidays_excluded}")

if __name__ == '__main__':
    main()
