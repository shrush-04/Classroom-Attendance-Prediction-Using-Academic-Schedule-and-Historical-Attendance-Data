"""
train_regression.py
Script to train, evaluate, and save regression models for predicting student attendance.
Excludes leakage features Classes_Attended and Total_Classes.
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
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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
target_col = "Attendance_Percentage"

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
print("\nPredictors being used:")
print(f"Categorical ({len(categorical_cols)}): {categorical_cols}")
print(f"Numeric ({len(numeric_cols)}): {numeric_cols}")

# Verify all columns exist
missing_cols = [c for c in all_predictors if c not in df.columns]
if missing_cols:
    raise ValueError(f"Missing columns in dataset: {missing_cols}")

# Extract features and target
X = df[all_predictors]
y = df[target_col]

# ══════════════════════════════════════════════════════════════════════════════
# 2. Train-Test Split
# ══════════════════════════════════════════════════════════════════════════════
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTrain set shape: {X_train.shape}")
print(f"Test set shape: {X_test.shape}")

# ══════════════════════════════════════════════════════════════════════════════
# 3. Preprocessing Pipelines
# ══════════════════════════════════════════════════════════════════════════════
# Categorical pipeline
cat_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
])

# Numeric pipeline (scaling included for linear models, standardizing numeric columns)
num_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

# Combine into ColumnTransformer
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
    "LinearRegression": LinearRegression(),
    "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42, max_depth=8),
    "RandomForestRegressor": RandomForestRegressor(random_state=42, n_estimators=100, max_depth=12),
    "GradientBoostingRegressor": GradientBoostingRegressor(random_state=42, n_estimators=100, learning_rate=0.1)
}

results = []
trained_pipelines = {}

print("\nTraining and evaluating models...")
for name, model in models.items():
    # Build complete pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", model)
    ])
    
    # Train
    pipeline.fit(X_train, y_train)
    trained_pipelines[name] = pipeline
    
    # Predict
    y_pred = pipeline.predict(X_test)
    
    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"  {name:25} -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
    
    results.append({
        "Model": name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    })

# Save results to CSV
results_df = pd.DataFrame(results)
results_csv_path = os.path.join(OUTPUTS_DIR, "regression_model_results.csv")
results_df.to_csv(results_csv_path, index=False)
print(f"\nSaved regression results to: {results_csv_path}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. Select Best Model & Save
# ══════════════════════════════════════════════════════════════════════════════
# Select best model based on lowest RMSE
best_model_row = results_df.loc[results_df["RMSE"].idxmin()]
best_model_name = best_model_row["Model"]
best_rmse = best_model_row["RMSE"]
best_r2 = best_model_row["R2"]

print(f"\nBest Model selected: {best_model_name}")
print(f"  Test RMSE: {best_rmse:.4f}")
print(f"  Test R2  : {best_r2:.4f}")

# Save the best pipeline
best_pipeline = trained_pipelines[best_model_name]
best_model_path = os.path.join(MODELS_DIR, "best_regression_model.joblib")
joblib.dump(best_pipeline, best_model_path)
print(f"Saved best model pipeline to: {best_model_path}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. Generate Actual vs Predicted Plot
# ══════════════════════════════════════════════════════════════════════════════
# Make predictions on test set with best model
best_preds = best_pipeline.predict(X_test)

plt.figure(figsize=(10, 8))
sns.scatterplot(x=y_test, y=best_preds, alpha=0.5, color="teal", label="Predictions")
# Plot perfect prediction diagonal line
min_val = min(y_test.min(), best_preds.min())
max_val = max(y_test.max(), best_preds.max())
plt.plot([min_val, max_val], [min_val, max_val], color="red", linestyle="--", linewidth=2, label="Perfect Fit")

plt.title(f"Actual vs Predicted Attendance ({best_model_name})")
plt.xlabel("Actual Attendance Percentage (%)")
plt.ylabel("Predicted Attendance Percentage (%)")
plt.legend()

chart_path = os.path.join(CHARTS_DIR, "regression_actual_vs_predicted.png")
plt.tight_layout()
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved Actual vs Predicted plot to: {chart_path}")
print("\nRegression training script finished successfully.")
