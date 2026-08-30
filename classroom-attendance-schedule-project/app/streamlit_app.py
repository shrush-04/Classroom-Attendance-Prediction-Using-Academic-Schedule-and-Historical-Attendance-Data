import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import joblib

# Set page config
st.set_page_config(
    page_title="Classroom Attendance Prediction Dashboard",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling (Glassmorphism & Dark Slate palette)
st.markdown("""
<style>
    /* Main body background and font */
    body {
        background-color: #0b0f19;
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium Title styling */
    .title-text {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        color: #8fa0b5;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(17, 25, 40, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.075);
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .card-title {
        color: #00f2fe;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 8px;
    }
    
    /* Alert cards */
    .warning-card {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 15px;
        color: #fca5a5;
        margin-bottom: 20px;
    }
    
    .info-card {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 8px;
        padding: 15px;
        color: #bfdbfe;
        margin-bottom: 20px;
    }

    .success-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 8px;
        padding: 15px;
        color: #a7f3d0;
        margin-bottom: 20px;
    }
    
    /* Sidebar adjustments */
    .sidebar .sidebar-content {
        background-color: #0b0f19;
    }
    
    /* Quick indicator metrics */
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
    }
    
    .metric-lbl {
        font-size: 0.85rem;
        color: #8fa0b5;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Project paths setup
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_data_path = os.path.join(project_root, "data", "raw", "raw_lecture_attendance.csv")
cleaned_data_path = os.path.join(project_root, "data", "processed", "cleaned_lecture_attendance.csv")
models_dir = os.path.join(project_root, "models")
reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")

# Check resources
data_exists = os.path.exists(cleaned_data_path)
models_trained = os.path.exists(reg_model_path) and os.path.exists(clf_model_path)

# Header Section
st.markdown("<div class='title-text'>Classroom Attendance Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>Lecture-level predictive insights derived from timetables, exam calendars, and historical registers (MCA Final Year - Sem III)</div>", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTENT -----------------
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/calendar.png", width=70)
    st.markdown("### **System Status**")
    
    if data_exists:
        st.markdown("🟢 **Cleaned Data:** Available")
    else:
        st.markdown("🔴 **Cleaned Data:** Missing")
        
    if models_trained:
        st.markdown("🟢 **Model Pipelines:** Trained")
    else:
        st.markdown("🔴 **Model Pipelines:** Untrained")
        
    st.markdown("---")
    st.markdown("### **Privacy Notice**")
    st.caption("In compliance with academic guidelines and privacy regulations, no student names, roll numbers, or personal details are collected, processed, or stored. All predictions are generated at the aggregate lecture level.")
    
    st.markdown("---")
    st.markdown("### **Verification Rules**")
    st.caption("Timetable schedules and present student registers are cross-validated. Maximum capacity values are checked against current enrollments dynamically.")

# ----------------- MAIN LAYOUT -----------------

# Tab configuration
tabs = st.tabs(["📊 Historical Analysis & Data Status", "🔮 Predictive Model Inference", "📜 Collection Protocols & Ethics"])

# ================= TAB 1: DATA STATUS & VISUALIZATIONS =================
with tabs[0]:
    if not data_exists:
        st.markdown("""
        <div class='warning-card'>
            <h4>⚠️ Attendance Data is Missing</h4>
            <p>The system has not loaded any cleaned lecture registers. The charts below are hidden because no original records are present in the project workspace.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='glass-card'>
                <div class='card-title'>How to Load Your Data</div>
                <ol>
                    <li>Extract aggregate attendance from registers and timetables.</li>
                    <li>Open <code>data/templates/raw_lecture_attendance_template.csv</code>.</li>
                    <li>Fill in raw data rows according to the schema rules.</li>
                    <li>Save the spreadsheet to <code>data/raw/raw_lecture_attendance.csv</code>.</li>
                    <li>Execute the pipeline: <code>python src/run_pipeline.py</code>.</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='glass-card'>
                <div class='card-title'>Data Schema Summary</div>
                <ul>
                    <li><b>Total Enrolled Students:</b> MCA class capacity (typically 60-205).</li>
                    <li><b>Students Present:</b> Physical headcount count.</li>
                    <li><b>Attendance Percentage:</b> Present / Enrolled * 100.</li>
                    <li><b>Holiday Before/After:</b> Holiday proximity checks.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        # Load cleaned data
        df = pd.read_csv(cleaned_data_path)
        
        # Display high-level stats
        st.markdown("### **Academic Attendance Summary**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Total Lectures Logged</div><div class='metric-val'>{len(df)}</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Avg Attendance Rate</div><div class='metric-val'>{df['Attendance_Percentage'].mean():.2f}%</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Highest Attendance</div><div class='metric-val'>{df['Attendance_Percentage'].max():.2f}%</div></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Lowest Attendance</div><div class='metric-val'>{df['Attendance_Percentage'].min():.2f}%</div></div>", unsafe_allow_html=True)
            
        # Visualizations (Matplotlib / Seaborn)
        st.markdown("### **Attendance Distribution & Trend Analysis**")
        col_v1, col_v2 = st.columns(2)
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        with col_v1:
            st.markdown("<div class='glass-card'><div class='card-title'>Subject-wise Attendance Distribution</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x='Subject', y='Attendance_Percentage', ax=ax, palette='Set2')
            plt.xticks(rotation=30)
            ax.set_ylabel('Attendance Percentage')
            ax.set_xlabel('Subjects')
            fig.patch.set_facecolor('#111928')
            ax.set_facecolor('#1f2937')
            ax.spines['bottom'].set_color('#ffffff')
            ax.spines['left'].set_color('#ffffff')
            ax.xaxis.label.set_color('#ffffff')
            ax.yaxis.label.set_color('#ffffff')
            ax.tick_params(colors='#ffffff')
            ax.title.set_color('#ffffff')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_v2:
            st.markdown("<div class='glass-card'><div class='card-title'>Attendance Trends by Time of Day</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Simple morning/afternoon grouping
            if 'Start_Time' in df.columns:
                start_hour = pd.to_datetime(df['Start_Time'], format='%H:%M').dt.hour
                df['Time_slot'] = np.where(start_hour < 12, 'Morning', 'Afternoon')
                sns.boxplot(data=df, x='Time_slot', y='Attendance_Percentage', ax=ax, palette='pastel')
            else:
                sns.boxplot(data=df, x='Lecture_Number', y='Attendance_Percentage', ax=ax, palette='pastel')
                
            ax.set_ylabel('Attendance Percentage')
            fig.patch.set_facecolor('#111928')
            ax.set_facecolor('#1f2937')
            ax.spines['bottom'].set_color('#ffffff')
            ax.spines['left'].set_color('#ffffff')
            ax.xaxis.label.set_color('#ffffff')
            ax.yaxis.label.set_color('#ffffff')
            ax.tick_params(colors='#ffffff')
            ax.title.set_color('#ffffff')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        col_v3, col_v4 = st.columns(2)
        with col_v3:
            st.markdown("<div class='glass-card'><div class='card-title'>Average Attendance by Day of Week</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            sns.barplot(data=df, x='Day_of_Week', y='Attendance_Percentage', order=[d for d in day_order if d in df['Day_of_Week'].unique()], ax=ax, errorbar=None, palette='viridis')
            ax.set_ylabel('Attendance Percentage')
            fig.patch.set_facecolor('#111928')
            ax.set_facecolor('#1f2937')
            ax.spines['bottom'].set_color('#ffffff')
            ax.spines['left'].set_color('#ffffff')
            ax.xaxis.label.set_color('#ffffff')
            ax.yaxis.label.set_color('#ffffff')
            ax.tick_params(colors='#ffffff')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_v4:
            st.markdown("<div class='glass-card'><div class='card-title'>Historical Attendance Timeline Trend</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            df_sorted = df.sort_values(by='Date')
            sns.lineplot(data=df_sorted, x='Date', y='Attendance_Percentage', ax=ax, color='#00f2fe', marker='o', errorbar=None)
            plt.xticks(rotation=45)
            ax.set_ylabel('Attendance Percentage')
            fig.patch.set_facecolor('#111928')
            ax.set_facecolor('#1f2937')
            ax.spines['bottom'].set_color('#ffffff')
            ax.spines['left'].set_color('#ffffff')
            ax.xaxis.label.set_color('#ffffff')
            ax.yaxis.label.set_color('#ffffff')
            ax.tick_params(colors='#ffffff')
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2: INTERACTIVE PREDICTOR =================
with tabs[1]:
    if not models_trained:
        st.markdown("""
        <div class='warning-card'>
            <h4>🔮 Prediction Unavailable</h4>
            <p>Machine learning models have not been trained yet. Train the model after adding validated original attendance data.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### **Lecture Parameter Entry**")
        
        # Load best model features
        reg_package = joblib.load(reg_model_path)
        feature_cols = reg_package['features']
        
        # Predictor Input Form
        with st.form("prediction_form"):
            col_in1, col_in2, col_in3 = st.columns(3)
            with col_in1:
                date_input = st.date_input("Date")
                day_input = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                lecture_number = st.slider("Lecture Number Slot", 1, 8, 1)
                start_time = st.selectbox("Start Time", ["09:00", "10:15", "11:30", "13:30", "14:45", "16:00"])
                end_time = st.selectbox("End_Time", ["10:00", "11:15", "12:30", "14:30", "15:45", "17:00"])
                
            with col_in2:
                subject = st.text_input("Subject Code (e.g. MCA301)", value="MCA301")
                faculty_id = st.text_input("Faculty ID (e.g. F001)", value="F001")
                semester = st.selectbox("Semester", ["Third Semester"])
                branch = st.selectbox("Branch", ["MCA"])
                section = st.selectbox("Section", ["A", "B"])
                classroom = st.text_input("Classroom (e.g. CR201)", value="CR201")
                
            with col_in3:
                enrolled = st.number_input("Total Enrolled Students (Class Strength)", min_value=1, max_value=250, value=60)
                practical_theory = st.selectbox("Practical / Theory", ["Theory", "Practical"])
                test_week = st.selectbox("Internal Test Week?", [0, 1])
                assignment = st.selectbox("Assignment Due?", [0, 1])
                holiday_prox = st.selectbox("Holiday Proximity", ["None", "Holiday_Before", "Holiday_After", "Both"])
                
            st.markdown("#### **Historical Lag Features (Previous Class Context)**")
            col_in4, col_in5 = st.columns(2)
            with col_in4:
                prev_attendance = st.slider("Previous Lecture Attendance Percentage (%)", 0.0, 100.0, 78.0)
                gap_hours = st.number_input("Gap Since Previous Lecture (Hours)", min_value=0.0, max_value=168.0, value=24.0)
            with col_in5:
                rolling_3 = st.slider("Rolling Average of Previous 3 Lectures (%)", 0.0, 100.0, 78.0)
                subj_avg = st.slider("Subject Historical Average Attendance (%)", 0.0, 100.0, 78.0)
                
            submit = st.form_submit_button("Generate Prediction Insights")
            
        if submit:
            # Package inputs
            from predict_future_lecture import predict_lecture_attendance
            
            lecture_dict = {
                'Date': date_input.strftime('%Y-%m-%d'),
                'Day_of_Week': day_input,
                'Lecture_Number': lecture_number,
                'Start_Time': start_time,
                'End_Time': end_time,
                'Subject': subject,
                'Faculty_ID': faculty_id,
                'Semester': semester,
                'Branch': branch,
                'Section': section,
                'Classroom': classroom,
                'Total_Enrolled_Students': enrolled,
                'Practical_Theory': practical_theory,
                'Internal_Test_Week': test_week,
                'Assignment_Due': assignment,
                'Holiday_Before_After': holiday_prox,
                'Previous_Lecture_Attendance_Percentage': prev_attendance,
                'Gap_Since_Previous_Lecture_Hours': gap_hours,
                'Rolling_Average_Previous_3_Lectures': rolling_3,
                'Subject_Historical_Average': subj_avg
            }
            
            # Predict
            res = predict_lecture_attendance(lecture_dict, models_dir=models_dir)
            
            if res.get("success"):
                st.markdown("### **Prediction Results**")
                
                pres_count = res.get("predicted_present")
                pres_pct = res.get("predicted_percentage")
                band = res.get("predicted_band")
                risk = res.get("risk_level")
                
                c_o1, c_o2, c_o3, c_o4 = st.columns(4)
                
                with c_o1:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-lbl'>Predicted Present Count</div>
                        <div class='metric-val' style='color:#00f2fe;'>{pres_count} / {enrolled}</div>
                        <p style='font-size:0.8rem;color:#8fa0b5;margin-top:5px;'>Students expected to attend</p>
                    </div>
                    """, unsafe_allow_html=True)
                with c_o2:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-lbl'>Predicted Percentage</div>
                        <div class='metric-val' style='color:#00f2fe;'>{pres_pct:.2f}%</div>
                        <p style='font-size:0.8rem;color:#8fa0b5;margin-top:5px;'>Overall class fill rate</p>
                    </div>
                    """, unsafe_allow_html=True)
                with c_o3:
                    band_color = "#34d399" if band == 'High' else ("#fbbf24" if band == 'Medium' else "#f87171")
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-lbl'>Predicted Band</div>
                        <div class='metric-val' style='color:{band_color};'>{band}</div>
                        <p style='font-size:0.8rem;color:#8fa0b5;margin-top:5px;'>Low <50 | Med 50-75 | High >75</p>
                    </div>
                    """, unsafe_allow_html=True)
                with c_o4:
                    risk_color = "#f87171" if risk == "High Risk" else "#34d399"
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div class='metric-lbl'>Risk Status</div>
                        <div class='metric-val' style='color:{risk_color};'>{risk}</div>
                        <p style='font-size:0.8rem;color:#8fa0b5;margin-top:5px;'>Flagged for low attendance</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(res.get("message"))

# ================= TAB 3: ETHICS, LIMITATIONS & PROTOCOLS =================
with tabs[2]:
    st.markdown("### **Ethical Considerations & System Constraints**")
    
    st.markdown("""
    <div class='glass-card'>
        <div class='card-title'>Privacy by Design Rules</div>
        <p>This predictive system follows rigid anonymization boundaries to comply with institutional student rights:</p>
        <ul>
            <li><b>Zero Student PII:</b> The database does not and will never map student names, roll numbers, or emails.</li>
            <li><b>Lecture-Level Aggregates:</b> We process attendance only as session sums (e.g. 52 present out of 60). Individual checks are discarded.</li>
            <li><b>Encoders for Instructors:</b> Faculty identities are mapped to anonymous markers (F001, F002) to prevent professional targeting.</li>
        </ul>
    </div>
    
    <div class='glass-card'>
        <div class='card-title'>Trained Model Limitations</div>
        <ul>
            <li><b>Environmental Conditions:</b> Proximity of weather shifts, regional festivals, or campus workshops may introduce volatility not captured by standard timetable lags.</li>
            <li><b>First-Week Lags:</b> During the first week of the semester, lag-based indicators (e.g. previous lecture attendance) are unavailable and default to class historical baselines.</li>
            <li><b>Rescheduling Swaps:</b> Sudden manual adjustments to the timetable (swapped slots) might result in temporary prediction deviations if not logged.</li>
        </ul>
    </div>
    
    <div class='info-card'>
        <h4>📅 Administrative Notice</h4>
        <p>The prediction algorithms are intended as a scheduler aid to optimize resource distribution and prevent severe class empty rates. They are not intended for grading evaluation, discipline profiling, or individual assessment.</p>
    </div>
    """, unsafe_allow_html=True)
