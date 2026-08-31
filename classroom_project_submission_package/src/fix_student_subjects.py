"""
Fix student dataset: replace generic placeholder subjects with real MCA Sem III
subjects from the actual timetable (timetable_structured.csv).
Then retrain the student attendance model with the corrected subjects.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = r"d:\Data_Science_attendence_project"
STUDENT_CSV  = os.path.join(BASE_DIR, "data", "student_attendance_205_students.csv")
FIXED_CSV    = os.path.join(BASE_DIR, "classroom_project_submission_package",
                             "data", "processed", "student_attendance_205_students.csv")
MODEL_PATH   = os.path.join(BASE_DIR, "classroom_project_submission_package",
                             "models", "student_attendance_model.joblib")

# ── Real subjects from timetable_structured.csv (theory subjects only) ─────────
SUBJECT_MAP = {
    "Computer Networks":              "Mobile Application Development",
    "Data Structures & Algorithms":   "Data Science and Machine Learning",
    "Database Management Systems":    "Software Testing and Quality Assurance",
    "Software Engineering":           "Principles of Cloud Management and Security",
    "Theory of Computation":          "Innovation and Entrepreneurship Development",
}

# ── Step 1: Load and fix subject names ────────────────────────────────────────
print(f"Loading student CSV from: {STUDENT_CSV}")
df = pd.read_csv(STUDENT_CSV)
print(f"  Shape: {df.shape}")
print(f"  Original subjects: {df['Subject'].unique().tolist()}")

df["Subject"] = df["Subject"].map(SUBJECT_MAP).fillna(df["Subject"])
print(f"  Fixed subjects: {df['Subject'].unique().tolist()}")

# ── Step 2: Save fixed CSV ────────────────────────────────────────────────────
os.makedirs(os.path.dirname(FIXED_CSV), exist_ok=True)
df.to_csv(FIXED_CSV, index=False)
print(f"\nFixed CSV saved to: {FIXED_CSV}")

# ── Step 3: Retrain student model ─────────────────────────────────────────────
target = "Attendance_Status"
categorical_features = ["Gender", "Department", "Year", "Semester", "Subject", "Attendance_Period"]
numeric_features = [
    "Age", "Previous_Attendance_Percentage", "Assignment_Score",
    "Internal_Marks", "Study_Hours_Per_Week", "Medical_Leave_Days",
    "Travel_Distance_KM", "Previous_Exam_Score", "Late_Count",
    "Online_Class_Attendance"
]

X = df[categorical_features + numeric_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTraining: {X_train.shape}  |  Test: {X_test.shape}")

preprocessor = ColumnTransformer(transformers=[
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ("num", StandardScaler(), numeric_features),
])

clf = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")),
])

print("Training Random Forest Classifier...")
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump({
    "pipeline":  clf,
    "features":  {"categorical": categorical_features, "numeric": numeric_features},
    "accuracy":  accuracy,
    "classes":   clf.classes_.tolist(),
}, MODEL_PATH, compress=9)
print(f"\nModel saved to: {MODEL_PATH}")
print("\nDone! Restart the Streamlit app to see the correct subjects.")
