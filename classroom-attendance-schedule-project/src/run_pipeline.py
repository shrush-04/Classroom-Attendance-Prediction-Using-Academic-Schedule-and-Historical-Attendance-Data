import os
import sys
import pandas as pd
import numpy as np

# Add src folder to system path to import modules
sys.path.append(os.path.dirname(__file__))

# Import pipeline steps
import validate_raw_data
import clean_data
import feature_engineering
import train_models
import evaluate_models

def run_eda(processed_path, charts_dir, outputs_dir):
    """
    Generates Exploratory Data Analysis (EDA) charts and writes outputs/eda_summary.md.
    Only executed if cleaned data is present.
    """
    print("Running Exploratory Data Analysis (EDA)...")
    df = pd.read_csv(processed_path)
    os.makedirs(charts_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    summary_md_path = os.path.join(outputs_dir, "eda_summary.md")
    
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # 1. Attendance percentage distribution
        plt.figure(figsize=(8, 5))
        sns.histplot(df['Attendance_Percentage'], kde=True, color='purple', bins=15)
        plt.title('Distribution of Attendance Percentage')
        plt.xlabel('Attendance %')
        plt.ylabel('Count of Lectures')
        plt.savefig(os.path.join(charts_dir, 'attendance_percentage_distribution.png'), dpi=300)
        plt.close()

        # 2. Subject-wise attendance
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='Subject', y='Attendance_Percentage', palette='Set2')
        plt.title('Subject-wise Attendance Distribution')
        plt.xticks(rotation=45)
        plt.savefig(os.path.join(charts_dir, 'subject_wise_attendance.png'), dpi=300)
        plt.close()

        # 3. Day-wise attendance
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        plt.figure(figsize=(8, 5))
        sns.barplot(data=df, x='Day_of_Week', y='Attendance_Percentage', order=[d for d in day_order if d in df['Day_of_Week'].unique()], errorbar=None, palette='viridis')
        plt.title('Average Attendance by Day of Week')
        plt.savefig(os.path.join(charts_dir, 'day_wise_attendance.png'), dpi=300)
        plt.close()

        # 4. Time-slot-wise attendance
        if 'Time_of_Day' in df.columns:
            plt.figure(figsize=(6, 5))
            sns.boxplot(data=df, x='Time_of_Day', y='Attendance_Percentage', palette='pastel')
            plt.title('Attendance by Time of Day')
            plt.savefig(os.path.join(charts_dir, 'time_slot_wise_attendance.png'), dpi=300)
            plt.close()

        # 5. Lecture-number-wise attendance
        plt.figure(figsize=(8, 5))
        sns.lineplot(data=df, x='Lecture_Number', y='Attendance_Percentage', marker='o', errorbar=None, color='teal')
        plt.title('Average Attendance by Lecture Slot Number')
        plt.savefig(os.path.join(charts_dir, 'lecture_number_wise_attendance.png'), dpi=300)
        plt.close()

        # 6. Practical versus Theory attendance
        plt.figure(figsize=(6, 5))
        sns.boxplot(data=df, x='Practical_Theory', y='Attendance_Percentage', palette='coolwarm')
        plt.title('Attendance: Practical vs Theory')
        plt.savefig(os.path.join(charts_dir, 'practical_vs_theory_attendance.png'), dpi=300)
        plt.close()

        # 7. Attendance before or after holidays
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df, x='Holiday_Before_After', y='Attendance_Percentage', palette='muted')
        plt.title('Attendance Proximity to Holidays')
        plt.savefig(os.path.join(charts_dir, 'holiday_proximity_attendance.png'), dpi=300)
        plt.close()

        # 8. Attendance during internal-test weeks
        plt.figure(figsize=(6, 5))
        sns.boxplot(data=df, x='Internal_Test_Week', y='Attendance_Percentage', palette='Set1')
        plt.title('Attendance During Internal Test Weeks')
        plt.savefig(os.path.join(charts_dir, 'internal_test_attendance.png'), dpi=300)
        plt.close()

        # 9. Attendance before examinations
        if 'Week_Before_Exam' in df.columns:
            plt.figure(figsize=(6, 5))
            sns.boxplot(data=df, x='Week_Before_Exam', y='Attendance_Percentage', palette='Set3')
            plt.title('Attendance in Week Before Exam')
            plt.savefig(os.path.join(charts_dir, 'week_before_exam_attendance.png'), dpi=300)
            plt.close()

        # 10. Correlation heatmap of numeric columns
        plt.figure(figsize=(10, 8))
        numeric_df = df.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df.corr(), annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
        plt.title('Feature Correlation Matrix')
        plt.savefig(os.path.join(charts_dir, 'correlation_heatmap.png'), dpi=300)
        plt.close()
        
        print(f"EDA charts generated in: {charts_dir}")
    except Exception as e:
        print(f"Skipping chart plotting because plotting library is unavailable or error occurred: {str(e)}")

    # Generate eda_summary.md report
    with open(summary_md_path, 'w', encoding='utf-8') as f:
        f.write("# Exploratory Data Analysis Summary\n\n")
        f.write("This summary provides an overview of findings and patterns observed in the classroom attendance data.\n\n")
        f.write("## Descriptive Statistics\n\n")
        f.write(df[['Total_Enrolled_Students', 'Students_Present', 'Attendance_Percentage']].describe().to_markdown() + "\n\n")
        f.write("## Key Findings\n")
        f.write(f"- **Total Lectures Logged:** {len(df)}\n")
        f.write(f"- **Overall Mean Attendance Rate:** {df['Attendance_Percentage'].mean():.2f}%\n")
        f.write(f"- **Maximum Session Attendance:** {df['Attendance_Percentage'].max():.2f}%\n")
        f.write(f"- **Minimum Session Attendance:** {df['Attendance_Percentage'].min():.2f}%\n\n")
        f.write("Detailed charts showing subject-wise, day-wise, and slot-wise attendance distributions have been saved to the outputs directory.\n")

    print(f"EDA summary report saved to: {summary_md_path}")

def run_pipeline():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    templates_dir = os.path.join(project_root, "data", "templates")
    outputs_dir = os.path.join(project_root, "outputs")
    charts_dir = os.path.join(outputs_dir, "charts")
    models_dir = os.path.join(project_root, "models")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    # Paths
    csv_template = os.path.join(templates_dir, "raw_lecture_attendance_template.csv")
    xlsx_template = os.path.join(templates_dir, "raw_lecture_attendance_template.xlsx")
    
    raw_csv = os.path.join(raw_dir, "raw_lecture_attendance.csv")
    raw_xlsx = os.path.join(raw_dir, "raw_lecture_attendance.xlsx")

    # 1. Check if raw data exists
    raw_data_path = None
    if os.path.exists(raw_csv):
        raw_data_path = raw_csv
    elif os.path.exists(raw_xlsx):
        raw_data_path = raw_xlsx

    if raw_data_path is None:
        # Create templates if they do not exist
        print("Raw lecture attendance data is not present in data/raw/.")
        
        # Verify CSV template is ready
        if not os.path.exists(csv_template):
            print("Creating CSV template...")
            headers = "Lecture_ID,Date,Day_of_Week,Lecture_Number,Start_Time,End_Time,Subject,Faculty_ID,Semester,Branch,Section,Classroom,Total_Enrolled_Students,Students_Present,Attendance_Percentage,Previous_Lecture_Attendance_Percentage,Gap_Since_Previous_Lecture_Hours,Practical_Theory,Internal_Test_Week,Assignment_Due,Holiday_Before_After,Weather,Special_Event\n"
            with open(csv_template, 'w', encoding='utf-8') as f:
                f.write(headers)
        
        # Verify Excel template is ready
        if not os.path.exists(xlsx_template):
            print("Creating Excel template...")
            try:
                df_temp = pd.DataFrame(columns=[
                    "Lecture_ID", "Date", "Day_of_Week", "Lecture_Number", "Start_Time", "End_Time", 
                    "Subject", "Faculty_ID", "Semester", "Branch", "Section", "Classroom", 
                    "Total_Enrolled_Students", "Students_Present", "Attendance_Percentage", 
                    "Previous_Lecture_Attendance_Percentage", "Gap_Since_Previous_Lecture_Hours", 
                    "Practical_Theory", "Internal_Test_Week", "Assignment_Due", "Holiday_Before_After", 
                    "Weather", "Special_Event"
                ])
                df_temp.to_excel(xlsx_template, index=False)
            except Exception as e:
                print(f"Could not write xlsx template directly: {e}")

        print("=" * 80)
        print("NOTICE: TEMPLATES GENERATED")
        print(f"Please copy academic schedule attendance data into: {os.path.abspath(raw_csv)}")
        print("Then, re-run this pipeline script to train models and run evaluations.")
        print("=" * 80)
        return True

    # 2. Raw data exists. Run validation
    print(f"Found raw dataset at {raw_data_path}. Running validation...")
    valid, errors = validate_raw_data.run_validation(raw_data_path, outputs_dir)
    if not valid:
        print("=" * 80)
        print("ERROR: DATA VALIDATION FAILED")
        print(f"Data validation checks failed with {len(errors)} errors. Please check outputs/data_quality_report.md.")
        print("Pipeline execution aborted.")
        print("=" * 80)
        return False

    print("Data validation passed.")

    # 3. Clean data
    clean_csv_path = os.path.join(processed_dir, "cleaned_lecture_attendance.csv")
    clean_data.clean_data(raw_data_path, clean_csv_path)

    # 4. Feature engineering
    engineered_csv_path = os.path.join(processed_dir, "feature_engineered_attendance.csv")
    feature_engineering.engineer_features(clean_csv_path, engineered_csv_path)

    # 5. Exploratory Data Analysis (EDA)
    run_eda(clean_csv_path, charts_dir, outputs_dir)

    # 6. Train Models
    success = train_models.train_and_save_models(engineered_csv_path, models_dir, outputs_dir)
    if not success:
        print("Pipeline aborted during model training.")
        return False

    # 7. Evaluate Models
    evaluate_models.evaluate_models(engineered_csv_path, models_dir, charts_dir)

    print("=" * 80)
    print("SUCCESS: PIPELINE COMPLETED END-TO-END")
    print(f"Trained models saved to: {models_dir}")
    print(f"Model comparisons and charts saved to: {outputs_dir}")
    print("Pre-requisites completed. You can now launch the Streamlit dashboard: streamlit run app/streamlit_app.py")
    print("=" * 80)
    return True

if __name__ == "__main__":
    run_pipeline()
