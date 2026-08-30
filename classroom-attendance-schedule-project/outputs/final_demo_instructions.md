# Final Streamlit Dashboard Demo Instructions

This document provides step-by-step guidance on how to run, inspect, and demonstrate the Streamlit user interface to academic evaluators.

---

## 🚀 1. Starting the Dashboard Server

To start the dashboard local server, execute the following command in PowerShell:

```powershell
cd d:\Data_Science_attendence_project
python -m streamlit run classroom-attendance-schedule-project/app/streamlit_app.py
```

Once started, the application will be accessible at:
- **Local URL:** `http://localhost:8501`

---

## 📊 2. Tab-by-Tab Demo Flow

### Tab 1: Historical Analysis & Data Status (Dataset: 18 Lectures)
1. **Explain the Dataset:** Clearly point out the data summary section showing **18 valid lecture observations** logged. 
2. **Review Historical Visualizations:**
   - **Timeline Trend:** Shows volatile patterns ranging from 10.0% to 75.0% attendance.
   - **Day-of-Week & Time-Slot Charts:** Highlight that attendance is higher in mid-week morning slots and lower on weekends and afternoons.
3. **Point Out Safety Checks:** Mention the sidebar status indicator showing that validation checks have completed successfully.

### Tab 2: Predictive Model Inference
1. **Explain the Orange Validity Banner:**
   - *"Insufficient validated history for reliable machine-learning prediction. Use the historical-average baseline until more lecture records are collected."*
2. **Point Out Regression Model Warning:**
   - *"Regression results are exploratory because only 18 valid lecture observations are available."* (Random Forest MAE = 14.02 vs Dummy Baseline = 14.50. Evaluated on a 4-row test set).
3. **Point Out Classification Model Warning:**
   - *"Classification is not recommended for operational decisions because it did not outperform the baseline."* (Tied dummy classifier at 0.50 accuracy).
4. **Demonstrate Fallback Performance:**
   - Enter future lecture details (e.g. Wednesday, Slot 2, Theory lecture for MAD, Enrolled: 80).
   - Click **Generate Prediction Insights**.
   - Notice that the **Historical Average Baseline** (38.75% attendance / ~31 students) is shown as the primary reference.
   - The ML count regression is shown with a clear "Exploratory / Limited Data Warning" banner.
   - The **Attendance Band is blocked and flagged as unavailable**; no confident recommendation of Low/Medium/High is rendered.
   - Historical risk status defaults to "High Risk" because the mean (38.75%) is below the 50% threshold.

### Tab 3: Collection Protocols & Ethics
1. **PII Isolation:** Show that no roll numbers, names, or email IDs are stored in the system.
2. **Faculty Code Mapping:** Mention that teachers are represented anonymously (F_01, F_02).
3. **Model Guidelines:** Emphasize that models are intended for scheduling support, not student punitive profiling.
