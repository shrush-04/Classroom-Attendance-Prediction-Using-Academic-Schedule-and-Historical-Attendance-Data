"""
train_classification.py
Script to train, evaluate, and save classification models for student attendance status early warning.
Excludes leakage columns. Selects best model based on F1-score and Recall.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = r"d:\Data_Science_attendence_project"
DATA_FILE = os.path.join(BASE_DIR, "data", "student_attendance_205_students.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
CHARTS_DIR = os.path.join(OUTPUTS_DIR, "charts")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# 1. Load Data
# ══════════════════════════════════════════════════════════════════════════════
print("Loading dataset...")
df = pd.read_csv(DATA_FILE)
print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

# Target
target_col = "Attendance_Status"

# Encode Target: Defaulter (At Risk) = 1, Regular (Safe) = 0
y = df[target_col].map({"Regular": 0, "Defaulter": 1})

# Define predictors
categorical_cols = ["Gender", "Department", "Year", "Semester", "Subject"]
numeric_cols = [
    "Age",
    "Previous_Attendance_Percentage",
    "Assignment_Score",
    "Internal_Marks",
    "Study_Hours_Per_Week",
    "Medical_Leave_Days",
    "Travel_Distance_KM",
    "Previous_Exam_Score",
    "Late_Count",
    "Online_Class_Attendance"
]

all_predictors = categorical_cols + numeric_cols
X = df[all_predictors]

# Verify all columns exist
missing_cols = [c for c in all_predictors if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# ══════════════════════════════════════════════════════════════════════════════
# 2. Train-Test Split
# ══════════════════════════════════════════════════════════════════════════════
# Split with stratify to preserve class distribution
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTrain set shape: {X_train.shape} (Defaulter ratio: {y_train.mean():.4f})")
print(f"Test set shape: {X_test.shape} (Defaulter ratio: {y_test.mean():.4f})")

# ══════════════════════════════════════════════════════════════════════════════
# 3. Preprocessing Pipelines
# ══════════════════════════════════════════════════════════════════════════════
cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", num_transformer, numeric_cols),
        ("cat", cat_transformer, categorical_cols)
    ]
)

# ══════════════════════════════════════════════════════════════════════════════
# 4. Model Training & Evaluation
# ══════════════════════════════════════════════════════════════════════════════
models = {
    "LogisticRegression": LogisticRegression(random_state=42, max_iter=1000),
    "DecisionTreeClassifier": DecisionTreeClassifier(random_state=42, max_depth=6),
    "RandomForestClassifier": RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10),
    "GradientBoostingClassifier": GradientBoostingClassifier(random_state=42, n_estimators=100, learning_rate=0.1)
}

results = []
trained_pipelines = {}

print("\nTraining and evaluating models...")
for name, model in models.items():
    # Build complete pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    trained_pipelines[name] = pipeline
    
    # Predict labels & probabilities
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1]
    
    # Evaluate metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    
    print(f"  {name:28} -> Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}")
    
    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-score": f1,
        "ROC-AUC": auc
    })

# Save results to CSV
results_df = pd.DataFrame(results)
results_csv_path = os.path.join(OUTPUTS_DIR, "classification_model_results.csv")
results_df.to_csv(results_csv_path, index=False)
print(f"\nSaved classification results to: {results_csv_path}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. Select Best Model & Save
# ══════════════════════════════════════════════════════════════════════════════
# Selection: best model based on F1-score first, then Recall
# (Early warning system prioritizes identifying defaulters correctly while balancing precision)
best_model_row = results_df.sort_values(by=["F1-score", "Recall"], ascending=False).iloc[0]
best_model_name = best_model_row["Model"]
best_f1 = best_model_row["F1-score"]
best_recall = best_model_row["Recall"]
best_acc = best_model_row["Accuracy"]

print(f"\nBest Model selected: {best_model_name}")
print(f"  Test Accuracy: {best_acc:.4f}")
print(f"  Test F1-score: {best_f1:.4f}")
print(f"  Test Recall  : {best_recall:.4f}")

# Save the best pipeline
best_pipeline = trained_pipelines[best_model_name]
best_model_path = os.path.join(MODELS_DIR, "best_classification_model.joblib")
joblib.dump(best_pipeline, best_model_path)
print(f"Saved best model pipeline to: {best_model_path}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. Generate Confusion Matrix Plot
# ══════════════════════════════════════════════════════════════════════════════
best_preds = best_pipeline.predict(X_test)
cm = confusion_matrix(y_test, best_preds)

plt.figure(figsize=(8, 7))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Regular", "Defaulter"])
disp.plot(cmap="Blues", values_format="d")
plt.title(f"Confusion Matrix - Best Classifier ({best_model_name})")
plt.grid(False) # Turn off grid lines for matrix visibility

chart_path = os.path.join(CHARTS_DIR, "best_classifier_confusion_matrix.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved Confusion Matrix plot to: {chart_path}")
print("\nClassification training script finished successfully.")
