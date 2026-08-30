import pandas as pd
import numpy as np
import os
import sys
import joblib
import re

def predict_lecture_attendance(lecture_data, models_dir=None):
    """
    Predicts attendance statistics for a future class session.
    Input dictionary: lecture_data must contain all required timetable/historical properties.
    """
    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

    reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
    clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")

    if not os.path.exists(reg_model_path) or not os.path.exists(clf_model_path):
        return {
            "success": False,
            "message": "Model files are not trained. Please add validated attendance records and run training first."
        }

    # Load serialized packages
    reg_package = joblib.load(reg_model_path)
    clf_package = joblib.load(clf_model_path)

    # Derive missing feature engineering inputs from input values
    date_parsed = pd.to_datetime(lecture_data['Date'])
    
    # Day_of_Week_Int
    day_of_week_int = date_parsed.dayofweek
    
    # Day_of_Semester (we can approximate it or default it if not available)
    day_of_semester = lecture_data.get('Day_of_Semester', 50) # default midpoint
    
    # Week_Number
    week_number = date_parsed.isocalendar().week
    
    # Is_Morning / Is_Afternoon
    start_hour = int(lecture_data['Start_Time'].split(':')[0])
    is_morning = 1 if start_hour < 12 else 0
    is_afternoon = 1 if start_hour >= 12 else 0
    time_of_day = 'Morning' if start_hour < 12 else 'Afternoon'
    
    # Days_Since_Last_Holiday (approximation or direct input)
    days_since_last_holiday = lecture_data.get('Days_Since_Last_Holiday', 7.0)
    
    # Week_Before_Exam (direct input or default to 0)
    week_before_exam = lecture_data.get('Week_Before_Exam', 0)
    
    # Consecutive_Lecture_Count (direct input or default to 1)
    consecutive_lecture_count = lecture_data.get('Consecutive_Lecture_Count', 1)

    # Rolling_Average_Previous_3_Lectures (direct or previous attendance)
    prev_pct = lecture_data.get('Previous_Lecture_Attendance_Percentage', 78.0)
    if pd.isna(prev_pct) or prev_pct == "Not_Collected":
        prev_pct = 75.0 # baseline mean
    
    rolling_3 = lecture_data.get('Rolling_Average_Previous_3_Lectures', prev_pct)
    subj_avg = lecture_data.get('Subject_Historical_Average', prev_pct)
    gap_hours = lecture_data.get('Gap_Since_Previous_Lecture_Hours', 24.0)

    # Prepare input dictionary aligned with the model's training columns
    model_input = {
        'Day_of_Week': lecture_data['Day_of_Week'],
        'Lecture_Number': int(lecture_data['Lecture_Number']),
        'Start_Time': lecture_data['Start_Time'],
        'End_Time': lecture_data['End_Time'],
        'Subject': lecture_data['Subject'],
        'Faculty_ID': lecture_data['Faculty_ID'],
        'Semester': lecture_data['Semester'],
        'Branch': lecture_data['Branch'],
        'Section': lecture_data['Section'],
        'Classroom': lecture_data['Classroom'],
        'Practical_Theory': lecture_data['Practical_Theory'],
        'Internal_Test_Week': int(lecture_data['Internal_Test_Week']),
        'Assignment_Due': int(lecture_data['Assignment_Due']),
        'Holiday_Before_After': lecture_data['Holiday_Before_After'],
        'Weather': lecture_data.get('Weather', 'Not_Collected'),
        'Special_Event': lecture_data.get('Special_Event', 'Not_Collected'),
        'Day_of_Week_Int': day_of_week_int,
        'Day_of_Semester': day_of_semester,
        'Week_Number': week_number,
        'Time_of_Day': time_of_day,
        'Is_Morning': is_morning,
        'Is_Afternoon': is_afternoon,
        'Days_Since_Last_Holiday': float(days_since_last_holiday),
        'Week_Before_Exam': int(week_before_exam),
        'Consecutive_Lecture_Count': int(consecutive_lecture_count),
        'Previous_Lecture_Attendance_Percentage': float(prev_pct),
        'Gap_Since_Previous_Lecture_Hours': float(gap_hours),
        'Rolling_Average_Previous_3_Lectures': float(rolling_3),
        'Subject_Historical_Average': float(subj_avg)
    }

    input_df = pd.DataFrame([model_input])

    # Predict Students_Present
    reg_features = reg_package['features']
    reg_pipeline = reg_package['pipeline']
    predicted_present = reg_pipeline.predict(input_df[reg_features])[0]
    
    # Cap between 0 and Enrolled Students
    enrolled = int(lecture_data['Total_Enrolled_Students'])
    predicted_present = max(0, min(enrolled, int(round(predicted_present))))

    # Predict Attendance_Band
    clf_features = clf_package['features']
    clf_pipeline = clf_package['pipeline']
    predicted_band = clf_pipeline.predict(input_df[clf_features])[0]

    # Calculate Attendance Percentage
    predicted_pct = round((predicted_present / enrolled) * 100, 2) if enrolled > 0 else 0.0

    # Calculate low-attendance risk indicator
    # High Risk if predicted pct < 50% or band is Low
    risk_level = "High Risk" if (predicted_pct < 50.0 or predicted_band == 'Low') else "Normal"

    return {
        "success": True,
        "predicted_present": predicted_present,
        "predicted_percentage": predicted_pct,
        "predicted_band": predicted_band,
        "risk_level": risk_level
    }

if __name__ == "__main__":
    # Example dry run format
    test_lecture = {
        'Date': '2026-09-01',
        'Day_of_Week': 'Tuesday',
        'Lecture_Number': 2,
        'Start_Time': '10:15',
        'End_Time': '11:15',
        'Subject': 'MCA301',
        'Faculty_ID': 'F001',
        'Semester': 'Third Semester',
        'Branch': 'MCA',
        'Section': 'A',
        'Classroom': 'CR201',
        'Total_Enrolled_Students': 60,
        'Practical_Theory': 'Theory',
        'Internal_Test_Week': 0,
        'Assignment_Due': 0,
        'Holiday_Before_After': 'None',
        'Weather': 'Sunny',
        'Special_Event': 'None',
        'Previous_Lecture_Attendance_Percentage': 85.0,
        'Gap_Since_Previous_Lecture_Hours': 24.0,
        'Rolling_Average_Previous_3_Lectures': 82.0,
        'Subject_Historical_Average': 80.0
    }
    
    result = predict_lecture_attendance(test_lecture)
    print("Prediction dry run result:")
    print(result)
