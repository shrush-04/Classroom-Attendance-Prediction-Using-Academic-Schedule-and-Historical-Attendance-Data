# Streamlit Predictive Dashboard

This directory contains the interactive dashboard for the Classroom Attendance Prediction project.

## Running the Dashboard

To run the Streamlit application:

1. **Verify dependencies are installed:**
   Ensure you have installed all libraries from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Streamlit:**
   Execute the following command from the project root directory:
   ```bash
   streamlit run classroom-attendance-schedule-project/app/streamlit_app.py
   ```

3. **Browse:**
   The dashboard will automatically open in your default browser at `http://localhost:8501`.

## Dashboard Tabs

- **📊 Historical Analysis & Data Status:** Displays key metrics of the loaded dataset and renders trends, subject-wise, day-of-week, and time-slot attendance charts. (Visible only when cleaned data exists).
- **🔮 Predictive Model Inference:** Provides an interactive lecture parameters input form to run real-time predictions of present counts, percentages, attendance bands, and risk flags. (Active only when model pipelines are trained).
- **📜 Collection Protocols & Ethics:** Outlines the Privacy by Design parameters, source record checklists, and mathematical model limitations.
