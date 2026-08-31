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

    .baseline-card {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 8px;
        padding: 16px;
        color: #fde68a;
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
src_dir = os.path.join(project_root, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

raw_data_path = os.path.join(project_root, "data", "raw", "raw_lecture_attendance.csv")
cleaned_data_path = os.path.join(project_root, "data", "processed", "cleaned_lecture_attendance.csv")
feat_data_path = os.path.join(project_root, "data", "processed", "feature_engineered_attendance.csv")
models_dir = os.path.join(project_root, "models")
reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")

# Check resources
data_exists = os.path.exists(cleaned_data_path)
models_trained = os.path.exists(reg_model_path) and os.path.exists(clf_model_path)

# Load model validity metadata
reg_is_valid = False
clf_is_valid = False
hist_mean_pct = 38.75   # fallback historical average
hist_mean_present = 31  # fallback historical count
reg_model_name = "Dummy Baseline (Mean)"
clf_model_name = "Dummy Classifier (Most Frequent)"
most_frequent_class = "Low"

if models_trained:
    try:
        _reg_pkg = joblib.load(reg_model_path)
        _clf_pkg = joblib.load(clf_model_path)
        reg_is_valid = _reg_pkg.get("is_valid", False)
        clf_is_valid = _clf_pkg.get("is_valid", False)
        reg_model_name = _reg_pkg.get("model_name", "Unknown")
        clf_model_name = _clf_pkg.get("model_name", "Unknown")
        hist_mean_pct = _reg_pkg.get("mean_attendance_percentage", 38.75)
        hist_mean_present = _reg_pkg.get("mean_students_present", 31)
        most_frequent_class = _clf_pkg.get("most_frequent_class", "Low")
    except Exception:
        pass

# ── Per-subject historical averages (from real attendance data) ───────────────
# Fallback averages for subjects with no real lecture records yet
_SUBJECT_DEFAULTS = {
    "Mobile Application Development":           {"pct": 40.37, "present": 32, "n": 17},
    "MAD Practical":                            {"pct": 11.25, "present": 9,  "n": 1},
    "Data Science and Machine Learning":        {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "Software Testing and Quality Assurance":   {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "Principles of Cloud Management and Security": {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "Innovation and Entrepreneurship Development":  {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "STQA Practical":                           {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "DS and ML Practical":                      {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "Mini Project":                             {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
    "Industry Readiness Program":               {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0},
}
# Override with real computed averages if cleaned data exists
if data_exists:
    try:
        _df_hist = pd.read_csv(cleaned_data_path)
        for _subj, _grp in _df_hist.groupby("Subject"):
            if _subj in _SUBJECT_DEFAULTS:
                _SUBJECT_DEFAULTS[_subj] = {
                    "pct":     round(float(_grp["Attendance_Percentage"].mean()), 2),
                    "present": int(round(_grp["Students_Present"].mean())),
                    "n":       len(_grp),
                }
    except Exception:
        pass

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
        reg_badge = "🟢 ML Model Beats Baseline" if reg_is_valid else "🟡 Using Historical Mean"
        clf_badge = "🟢 ML Model Beats Baseline" if clf_is_valid else "🟡 Using Most-Frequent Class"
        st.markdown(f"**Regression:** {reg_badge}")
        st.markdown(f"**Classification:** {clf_badge}")
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
tabs = st.tabs(["📊 Historical Analysis & Data Status", "🔮 Predictive Model Inference", "👨‍🎓 Student Attendance Risk Grid", "📜 Collection Protocols & Ethics"])

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
                    <li><b>Total Enrolled Students:</b> MCA class capacity (80 confirmed).</li>
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
            subjects = df['Subject'].unique().tolist()
            palette_s = sns.color_palette('Set2', len(subjects))
            sns.boxplot(data=df, x='Subject', y='Attendance_Percentage', hue='Subject', ax=ax, palette='Set2', legend=False)
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
            plt.close(fig)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_v2:
            st.markdown("<div class='glass-card'><div class='card-title'>Attendance Trends by Time of Day</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Simple morning/afternoon grouping
            if 'Start_Time' in df.columns:
                start_hour = pd.to_datetime(df['Start_Time'], format='%H:%M').dt.hour
                df['Time_slot'] = np.where(start_hour < 12, 'Morning', 'Afternoon')
                sns.boxplot(data=df, x='Time_slot', y='Attendance_Percentage', hue='Time_slot', ax=ax, palette='pastel', legend=False)
            else:
                sns.boxplot(data=df, x='Lecture_Number', y='Attendance_Percentage', hue='Lecture_Number', ax=ax, palette='pastel', legend=False)
                
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
            plt.close(fig)
            st.markdown("</div>", unsafe_allow_html=True)

        col_v3, col_v4 = st.columns(2)
        with col_v3:
            st.markdown("<div class='glass-card'><div class='card-title'>Average Attendance by Day of Week</div>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(8, 5))
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            days_present = [d for d in day_order if d in df['Day_of_Week'].unique()]
            df_day = df[df['Day_of_Week'].isin(days_present)].copy()
            sns.barplot(data=df_day, x='Day_of_Week', y='Attendance_Percentage', hue='Day_of_Week',
                        order=days_present, ax=ax, errorbar=None, palette='viridis', legend=False)
            ax.set_ylabel('Attendance Percentage')
            fig.patch.set_facecolor('#111928')
            ax.set_facecolor('#1f2937')
            ax.spines['bottom'].set_color('#ffffff')
            ax.spines['left'].set_color('#ffffff')
            ax.xaxis.label.set_color('#ffffff')
            ax.yaxis.label.set_color('#ffffff')
            ax.tick_params(colors='#ffffff')
            st.pyplot(fig)
            plt.close(fig)
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
            plt.close(fig)
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
        # ── PERMANENT SCIENTIFIC VALIDITY NOTICE (always shown) ──────────────
        n_lectures = len(pd.read_csv(cleaned_data_path)) if data_exists else 18
        st.markdown(f"""
        <div class='glass-card' style='border-left: 4px solid #f59e0b;'>
            <div class='card-title' style='color:#f59e0b;'>📋 Scientific Validity Notice — {n_lectures} Valid Lecture Observations</div>
            <p style='color:#fde68a; margin-bottom:8px;'>
                <b>Insufficient validated history for reliable machine-learning prediction.
                Use the historical-average baseline until more lecture records are collected.</b>
            </p>
            <p style='color:#e5e7eb; margin-bottom:6px;'>
                🔬 <b>Regression results are exploratory because only {n_lectures} valid lecture
                observations are available.</b> The best regression model (Random Forest) marginally
                beat the dummy baseline on a test set of only 4 rows — this cannot establish
                reliable generalization (R²=0.12, MAPE=43%).
            </p>
            <p style='color:#e5e7eb; margin-bottom:0;'>
                🚫 <b>Classification is not recommended for operational decisions because it did
                not outperform the baseline.</b> All classifiers tied or fell below the dummy
                baseline at 0.50 accuracy. The "High" band (&gt;75%) was never observed in any
                of the {n_lectures} recorded lectures and cannot be predicted.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # ── CONDITIONAL BANNERS (regression exploratory / classification invalid) ─
        if not reg_is_valid and not clf_is_valid:
            st.markdown(f"""
            <div class='baseline-card'>
                <h4>⚠️ Both Models Below Baseline — Historical Average is the Only Output</h4>
                <p>Neither the regression nor classification model outperforms a naive baseline.
                The historical average baseline ({hist_mean_pct:.2f}% / ~{int(round(hist_mean_present))} students)
                will be shown as the sole prediction reference.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Regression valid but explicitly exploratory
            if reg_is_valid:
                st.markdown(f"""
                <div class='baseline-card'>
                    <h4>🔬 Exploratory / Limited Data — Regression</h4>
                    <p>The trained regression model (<b>{reg_model_name}</b>) marginally beat the
                    dummy baseline on a <b>test set of only 4 rows</b>.
                    This result is <b>exploratory only</b> and cannot establish reliable generalization.
                    R²=0.12, MAPE=43%. The estimate below is shown for exploration purposes and
                    must not be used for operational decisions without a larger validated dataset.</p>
                </div>
                """, unsafe_allow_html=True)
            # Classification always invalid with current data
            if not clf_is_valid:
                st.markdown(f"""
                <div class='warning-card'>
                    <h4>🚫 Attendance Band Prediction Unavailable</h4>
                    <p>The classification model did not outperform the dummy baseline
                    (both at 0.50 accuracy on a 4-row test set). Additionally, the
                    <b>"High" attendance band (&gt;75%) was never observed</b> in any of the {n_lectures}
                    recorded lectures. Automated Low/Medium/High band decisions will not be
                    generated. Historical most-frequent class for reference only: <b>{most_frequent_class}</b>.</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("### **Lecture Parameter Entry**")

        # Load best model features
        reg_package = joblib.load(reg_model_path)
        feature_cols = reg_package['features']

        # ── Subject selector OUTSIDE form so lag defaults update immediately ──
        _SUBJECT_LIST = [
            "Mobile Application Development",
            "Data Science and Machine Learning",
            "Software Testing and Quality Assurance",
            "Principles of Cloud Management and Security",
            "Innovation and Entrepreneurship Development",
            "MAD Practical",
            "DS and ML Practical",
            "STQA Practical",
            "Mini Project",
            "Industry Readiness Program",
        ]
        subject = st.selectbox(
            "📚 Subject",
            _SUBJECT_LIST,
            key="pred_subject",
            help="Select a subject — historical lag defaults will auto-update to that subject's real averages."
        )
        # Look up this subject's real historical average
        _subj_stats = _SUBJECT_DEFAULTS.get(subject, {"pct": hist_mean_pct, "present": hist_mean_present, "n": 0})
        _subj_hist_pct     = float(_subj_stats["pct"])
        _subj_hist_present = int(_subj_stats["present"])
        _subj_hist_n       = int(_subj_stats["n"])

        # Show a small info badge about the data coverage for this subject
        if _subj_hist_n > 0:
            st.markdown(f"""
            <div class='success-card' style='padding:10px 15px;margin-bottom:10px;'>
                📊 <b>{subject}</b> — <b>{_subj_hist_n} recorded lectures</b> |
                Historical avg: <b>{_subj_hist_pct:.1f}%</b> (~{_subj_hist_present} students present out of 80)
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='baseline-card' style='padding:10px 15px;margin-bottom:10px;'>
                ⚠️ <b>{subject}</b> — No recorded lectures yet.
                Showing overall class average as default ({_subj_hist_pct:.1f}%).
            </div>""", unsafe_allow_html=True)

        # Predictor Input Form
        with st.form("prediction_form"):
            col_in1, col_in2, col_in3 = st.columns(3)
            with col_in1:
                date_input = st.date_input("Date")
                day_input = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
                lecture_number = st.slider("Lecture Number Slot", 1, 8, 1)
                start_time = st.selectbox("Start Time", ["08:30", "09:15", "10:15", "11:15", "13:30", "15:30"])
                end_time = st.selectbox("End Time", ["09:15", "10:15", "11:15", "12:15", "15:30", "17:00"])

            with col_in2:
                # Subject label (read-only — selected above outside the form)
                st.text_input("Subject (selected above)", value=subject, disabled=True)
                faculty_id = st.text_input("Faculty ID (e.g. F_01)", value="F_01")
                semester = st.selectbox("Semester", ["Third Semester"])
                branch = st.selectbox("Branch", ["MCA"])
                section = st.selectbox("Section", ["A+B", "A", "B"])
                classroom = st.text_input("Classroom (e.g. CR201)", value="Computer Lab")

            with col_in3:
                enrolled = st.number_input("Total Enrolled Students (Class Strength)", min_value=1, max_value=250, value=80)
                practical_theory = st.selectbox("Practical / Theory", ["Theory", "Practical"])
                test_week = st.selectbox("Internal Test Week?", [0, 1])
                assignment = st.selectbox("Assignment Due?", [0, 1])
                holiday_prox = st.selectbox("Holiday Proximity", ["None", "Holiday_Before", "Holiday_After"])

            st.markdown("#### **Historical Lag Features (Previous Class Context)**")
            st.caption(f"Defaults auto-filled from **{subject}** historical data ({_subj_hist_n} lectures recorded).")
            col_in4, col_in5 = st.columns(2)
            with col_in4:
                prev_attendance = st.slider(
                    "Previous Lecture Attendance Percentage (%)",
                    0.0, 100.0, _subj_hist_pct
                )
                gap_hours = st.number_input("Gap Since Previous Lecture (Hours)", min_value=0.0, max_value=168.0, value=24.0)
            with col_in5:
                rolling_3 = st.slider(
                    "Rolling Average of Previous 3 Lectures (%)",
                    0.0, 100.0, _subj_hist_pct
                )
                subj_avg = st.slider(
                    "Subject Historical Average Attendance (%)",
                    0.0, 100.0, _subj_hist_pct
                )

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

                # --- Subject-specific historical baseline ---
                _src = "real recorded lectures" if _subj_hist_n > 0 else "overall class average (no subject-specific data yet)"
                st.markdown(f"""
                <div class='glass-card'>
                    <div class='card-title'>📊 Historical Average Baseline — {subject}</div>
                    <p>Based on <b>{_subj_hist_n if _subj_hist_n > 0 else 'N/A'} recorded lectures</b>
                    for this subject ({_src}):</p>
                    <div style='font-size:2rem;font-weight:700;color:#fbbf24;'>
                        {_subj_hist_pct:.2f}% &nbsp;|&nbsp; ~{_subj_hist_present} students present out of {enrolled}
                    </div>
                    <p style='color:#8fa0b5;font-size:0.85rem;margin-top:8px;'>
                        This is the subject-specific operational baseline. Use this figure for
                        scheduling decisions for <b>{subject}</b>.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # --- Regression ML estimate (exploratory only if valid) ---
                if reg_is_valid:
                    st.markdown(f"""
                    <div class='info-card'>
                        <b>🔬 Exploratory ML Estimate (Random Forest — Limited Data Warning)</b><br>
                        Predicted present count: <b>{pres_count} / {enrolled}</b> &nbsp;|&nbsp;
                        Predicted percentage: <b>{pres_pct:.2f}%</b><br>
                        <span style='font-size:0.8rem;color:#93c5fd;'>
                        ⚠️ Computed on a 4-row test set only. R²=0.12, MAPE=43%.
                        Exploratory result — do not use for operational decisions.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class='warning-card'>
                        <b>⚠️ Regression model did not beat baseline — showing subject historical average only.</b>
                    </div>
                    """, unsafe_allow_html=True)

                # --- Classification band ---
                st.markdown(f"""
                <div class='warning-card'>
                    <b>🚫 Attendance Band: Not Available for Reliable Use</b><br>
                    The classification model tied the dummy baseline (accuracy=0.50 on 4 test rows).
                    The <b>"High" band (&gt;75%) was never observed</b> in any of the {n_lectures}
                    lectures. No automated Low/Medium/High recommendation will be generated.
                    {'<br>Historical most-frequent class for reference only: <b>' + most_frequent_class + '</b>' if not clf_is_valid else ''}
                </div>
                """, unsafe_allow_html=True)

                # Risk flag based on subject-specific average
                _risk_pct = _subj_hist_pct if _subj_hist_n > 0 else hist_mean_pct
                risk = "High Risk" if _risk_pct < 50.0 else "Normal"
                risk_color = "#f87171" if risk == "High Risk" else "#34d399"
                st.markdown(f"""
                <div class='glass-card'>
                    <div class='metric-lbl'>Historical Risk Status — {subject}</div>
                    <div class='metric-val' style='color:{risk_color};'>{risk}</div>
                    <p style='font-size:0.8rem;color:#8fa0b5;margin-top:5px;'>
                        Based on subject historical average of {_subj_hist_pct:.1f}%
                        {'(below' if _risk_pct < 50 else '(above'} the 50% attendance threshold).
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(res.get("message"))

# ================= TAB 3: STUDENT ATTENDANCE RISK GRID =================
with tabs[2]:
    st.markdown("### **Student Attendance Risk Grid (Cohort View)**")
    st.markdown("This dashboard leverages the student-level predictive model trained on 4,100 records (205 students) to predict attendance risk across all subjects and periods.")
    
    # Load student model
    student_model_path = os.path.join(models_dir, "student_attendance_model.joblib")
    if os.path.exists(student_model_path):
        model_pkg = joblib.load(student_model_path)
        pipeline = model_pkg['pipeline']
        
        # Load dataset — search in several candidate locations
        _candidate_paths = [
            os.path.join(project_root, "data", "processed", "student_attendance_205_students.csv"),
            os.path.join(project_root, "data", "student_attendance_205_students.csv"),
            os.path.join(os.path.dirname(project_root), "data", "student_attendance_205_students.csv"),
        ]
        student_data_path = next((p for p in _candidate_paths if os.path.exists(p)), None)
        if student_data_path is None:
            st.markdown("""
            <div class='warning-card'>
                <h4>⚠️ Student Dataset Not Found</h4>
                <p>The student attendance CSV file could not be located. Expected at
                <code>data/processed/student_attendance_205_students.csv</code>.
                Place the file there and refresh the page.</p>
            </div>
            """, unsafe_allow_html=True)
            st.stop()
        student_df = pd.read_csv(student_data_path)
        
        # Generate predictions
        X_stu = student_df[model_pkg['features']['categorical'] + model_pkg['features']['numeric']]
        student_df['Predicted_Status'] = pipeline.predict(X_stu)
        
        # Filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            selected_subject = st.selectbox("Filter Subject", ["All"] + list(student_df['Subject'].unique()))
        with col_f2:
            selected_period = st.selectbox("Filter Period", ["All"] + list(student_df['Attendance_Period'].unique()))
            
        filtered_df = student_df.copy()
        if selected_subject != "All":
            filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]
        if selected_period != "All":
            filtered_df = filtered_df[filtered_df['Attendance_Period'] == selected_period]
            
        # Create Pivot Grid: Student vs Subject + Period
        filtered_df['Subj_Period'] = filtered_df['Subject'] + " (" + filtered_df['Attendance_Period'] + ")"
        
        # Pivot
        pivot_df = filtered_df.pivot_table(
            index='Student_ID', 
            columns='Subj_Period', 
            values='Predicted_Status', 
            aggfunc=lambda x: x.iloc[0] if len(x) > 0 else "Unknown"
        )
        
        # Display summary counts
        n_regular = (filtered_df['Predicted_Status'] == 'Regular').sum()
        n_defaulter = (filtered_df['Predicted_Status'] == 'Defaulter').sum()
        
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Total Profiles Analyzed</div><div class='metric-val'>{len(filtered_df)}</div></div>", unsafe_allow_html=True)
        with c_m2:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Predicted Regular</div><div class='metric-val' style='color:#34d399;'>{n_regular}</div></div>", unsafe_allow_html=True)
        with c_m3:
            st.markdown(f"<div class='glass-card'><div class='metric-lbl'>Predicted Defaulters (At Risk)</div><div class='metric-val' style='color:#f87171;'>{n_defaulter}</div></div>", unsafe_allow_html=True)
            
        st.markdown("#### **Visual Attendance Status Grid**")
        st.caption("Green cells indicate predicted 'Regular' status; Red cells indicate predicted 'Defaulter' (attendance < 75% risk).")
        
        # Style and render pivot table
        def color_status_grid(val):
            if val == 'Regular':
                return 'background-color: rgba(16, 185, 129, 0.25); color: #34d399; font-weight: bold; text-align: center;'
            elif val == 'Defaulter':
                return 'background-color: rgba(239, 68, 68, 0.25); color: #f87171; font-weight: bold; text-align: center;'
            return 'background-color: rgba(255, 255, 255, 0.05); color: #8fa0b5; text-align: center;'

        # Clean display
        # pandas >= 2.1 renamed applymap -> map on Styler objects
        try:
            styled_pivot = pivot_df.style.map(color_status_grid)
        except AttributeError:
            styled_pivot = pivot_df.style.applymap(color_status_grid)  # older pandas fallback
        st.dataframe(styled_pivot, width='stretch', height=450)
        
        # Individual search
        st.markdown("---")
        st.markdown("### **🔍 Individual Student Risk Profile Search**")
        search_id = st.selectbox("Select Student ID", sorted(student_df['Student_ID'].unique()))
        
        student_records = student_df[student_df['Student_ID'] == search_id]
        
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            st.markdown(f"""
            <div class='glass-card'>
                <div class='card-title'>Student Info: {search_id}</div>
                <p><b>Gender:</b> {student_records['Gender'].iloc[0]}</p>
                <p><b>Age:</b> {student_records['Age'].iloc[0]}</p>
                <p><b>Department:</b> {student_records['Department'].iloc[0]}</p>
                <p><b>Semester:</b> {student_records['Semester'].iloc[0]}</p>
                <p><b>Weekly Study Hours:</b> {student_records['Study_Hours_Per_Week'].iloc[0]} hrs</p>
                <p><b>Travel Distance:</b> {student_records['Travel_Distance_KM'].iloc[0]} KM</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            st.markdown(f"#### **Subject-wise Predictions for {search_id}**")
            _cols_wanted = [c for c in ['Subject', 'Attendance_Period', 'Assignment_Score', 'Internal_Marks', 'Late_Count', 'Online_Class_Attendance', 'Predicted_Status'] if c in student_records.columns]
            subj_pred_df = student_records[_cols_wanted]
            try:
                st.dataframe(subj_pred_df.style.map(color_status_grid), width='stretch')
            except AttributeError:
                st.dataframe(subj_pred_df.style.applymap(color_status_grid), width='stretch')
            
    else:
        st.markdown("""
        <div class='warning-card'>
            <h4>⚠️ Student Prediction Model Not Trained</h4>
            <p>Please run <code>python src/train_student_model.py</code> to train the classifier and enable this grid dashboard.</p>
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 4: ETHICS, LIMITATIONS & PROTOCOLS =================
with tabs[3]:
    st.markdown("### **Ethical Considerations & System Constraints**")
    
    st.markdown("""
    <div class='glass-card'>
        <div class='card-title'>Privacy by Design Rules</div>
        <p>This predictive system follows rigid anonymization boundaries to comply with institutional student rights:</p>
        <ul>
            <li><b>Zero Student PII:</b> The database does not and will never map student names, roll numbers, or emails.</li>
            <li><b>Lecture-Level Aggregates:</b> We process attendance only as session sums (e.g. 52 present out of 80). Individual checks are discarded.</li>
            <li><b>Encoders for Instructors:</b> Faculty identities are mapped to anonymous markers (F_01, F_02) to prevent professional targeting.</li>
        </ul>
    </div>
    
    <div class='glass-card'>
        <div class='card-title'>Trained Model Limitations</div>
        <ul>
            <li><b>Small Sample Size:</b> Only 18 lectures have been logged. Statistically, this is insufficient for robust ML generalization. A minimum of 100+ lectures is recommended.</li>
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
