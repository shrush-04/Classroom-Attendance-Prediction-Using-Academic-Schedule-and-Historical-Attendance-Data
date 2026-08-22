"""
generate_regression_notebook.py
Programmatically generates and executes notebooks/02_regression_model.ipynb
"""

import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

BASE_DIR = r"d:\Data_Science_attendence_project"
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)
NOTEBOOK_PATH = os.path.join(NOTEBOOKS_DIR, "02_regression_model.ipynb")

# Initialize notebook structure
nb = nbformat.v4.new_notebook()

# Define cells
cells = []

# Cell 1: Header & Introduction
cells.append(nbformat.v4.new_markdown_cell(
    "# Phase 3: Attendance Prediction using Regression Models\n"
    "**Project:** Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System\n\n"
    "This notebook trains and evaluates regression models to predict student attendance percentage based on academic, personal, and behavioral factors.\n\n"
    "### ⚠️ Data Leakage Warning\n"
    "We must exclude `Classes_Attended` and `Total_Classes` from our predictor list. Because `Attendance_Percentage` is calculated directly using the formula:\n"
    "$$\\text{Attendance\\_Percentage} = \\frac{\\text{Classes\\_Attended}}{\\text{Total\\_Classes}} \\times 100$$\n"
    "including these variables would lead to direct data leakage, resulting in an artificial R2 score of 1.0. Our goal is to predict attendance using underlying student traits (like age, study hours, internal scores) to model student behavior rather than reproducing simple division arithmetic."
))

# Cell 2: Imports
cells.append(nbformat.v4.new_code_cell(
    "import os\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "import joblib\n\n"
    "from sklearn.model_selection import train_test_split\n"
    "from sklearn.impute import SimpleImputer\n"
    "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n"
    "from sklearn.compose import ColumnTransformer\n"
    "from sklearn.pipeline import Pipeline\n"
    "from sklearn.linear_model import LinearRegression\n"
    "from sklearn.tree import DecisionTreeRegressor\n"
    "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n"
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n\n"
    "# Set style\n"
    "sns.set_theme(style=\"whitegrid\")\n"
    "print(\"Libraries imported successfully.\")"
))

# Cell 3: Load Data
cells.append(nbformat.v4.new_code_cell(
    "BASE_DIR = r\"d:\\Data_Science_attendence_project\"\n"
    "DATA_FILE = os.path.join(BASE_DIR, \"data\", \"student_attendance_205_students.csv\")\n"
    "MODELS_DIR = os.path.join(BASE_DIR, \"models\")\n"
    "OUTPUTS_DIR = os.path.join(BASE_DIR, \"outputs\")\n"
    "CHARTS_DIR = os.path.join(OUTPUTS_DIR, \"charts\")\n\n"
    "os.makedirs(MODELS_DIR, exist_ok=True)\n"
    "os.makedirs(CHARTS_DIR, exist_ok=True)\n\n"
    "df = pd.read_csv(DATA_FILE)\n"
    "print(f\"Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.\")"
))

# Cell 4: Define Features and Target
cells.append(nbformat.v4.new_code_cell(
    "target_col = 'Attendance_Percentage'\n\n"
    "# Predictors we want to include\n"
    "categorical_cols = ['Gender', 'Department', 'Year', 'Semester', 'Subject']\n"
    "numeric_cols = [\n"
    "    'Age',\n"
    "    'Previous_Attendance_Percentage',\n"
    "    'Assignment_Score',\n"
    "    'Internal_Marks',\n"
    "    'Study_Hours_Per_Week',\n"
    "    'Medical_Leave_Days',\n"
    "    'Travel_Distance_KM',\n"
    "    'Previous_Exam_Score',\n"
    "    'Late_Count',\n"
    "    'Online_Class_Attendance'\n"
    "]\n\n"
    "all_predictors = categorical_cols + numeric_cols\n"
    "X = df[all_predictors]\n"
    "y = df[target_col]\n\n"
    "print(f\"Features (X) shape: {X.shape}\")\n"
    "print(f\"Target (y) shape: {y.shape}\")"
))

# Cell 5: Train-Test Split
cells.append(nbformat.v4.new_code_cell(
    "X_train, X_test, y_train, y_test = train_test_split(\n"
    "    X, y, test_size=0.2, random_state=42\n"
    ")\n"
    "print(f\"Train size: {X_train.shape[0]}\")\n"
    "print(f\"Test size: {X_test.shape[0]}\")"
))

# Cell 6: Preprocessing Pipeline
cells.append(nbformat.v4.new_code_cell(
    "# Pipeline for categorical features\n"
    "cat_transformer = Pipeline(steps=[\n"
    "    ('imputer', SimpleImputer(strategy='most_frequent')),\n"
    "    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
    "])\n\n"
    "# Pipeline for numeric features\n"
    "num_transformer = Pipeline(steps=[\n"
    "    ('imputer', SimpleImputer(strategy='median')),\n"
    "    ('scaler', StandardScaler())\n"
    "])\n\n"
    "# Column transformer mapping columns to pipelines\n"
    "preprocessor = ColumnTransformer(transformers=[\n"
    "    ('num', num_transformer, numeric_cols),\n"
    "    ('cat', cat_transformer, categorical_cols)\n"
    "])\n"
    "print(\"Preprocessor built successfully.\")"
))

# Cell 7: Model Definition and Training
cells.append(nbformat.v4.new_code_cell(
    "models = {\n"
    "    'LinearRegression': LinearRegression(),\n"
    "    'DecisionTreeRegressor': DecisionTreeRegressor(random_state=42, max_depth=8),\n"
    "    'RandomForestRegressor': RandomForestRegressor(random_state=42, n_estimators=100, max_depth=12),\n"
    "    'GradientBoostingRegressor': GradientBoostingRegressor(random_state=42, n_estimators=100, learning_rate=0.1)\n"
    "}\n\n"
    "results = []\n"
    "trained_pipelines = {}\n\n"
    "for name, model in models.items():\n"
    "    # Create complete pipeline with preprocessing and model\n"
    "    pipeline = Pipeline(steps=[\n"
    "        ('preprocessor', preprocessor),\n"
    "        ('regressor', model)\n"
    "    ])\n"
    "    # Train model\n"
    "    pipeline.fit(X_train, y_train)\n"
    "    trained_pipelines[name] = pipeline\n"
    "    \n"
    "    # Predict\n"
    "    y_pred = pipeline.predict(X_test)\n"
    "    \n"
    "    # Evaluate\n"
    "    mae = mean_absolute_error(y_test, y_pred)\n"
    "    mse = mean_squared_error(y_test, y_pred)\n"
    "    rmse = np.sqrt(mse)\n"
    "    r2 = r2_score(y_test, y_pred)\n"
    "    \n"
    "    print(f\"{name:25} -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}\")\n"
    "    results.append({\n"
    "        'Model': name,\n"
    "        'MAE': mae,\n"
    "        'MSE': mse,\n"
    "        'RMSE': rmse,\n"
    "        'R2': r2\n"
    "    })"
))

# Cell 8: Save Metrics Table
cells.append(nbformat.v4.new_code_cell(
    "results_df = pd.DataFrame(results)\n"
    "results_csv_path = os.path.join(OUTPUTS_DIR, 'regression_model_results.csv')\n"
    "results_df.to_csv(results_csv_path, index=False)\n"
    "print(\"Saved results table.\")\n"
    "results_df"
))

# Cell 9: Select & Save Best Model
cells.append(nbformat.v4.new_code_cell(
    "best_model_idx = results_df['RMSE'].idxmin()\n"
    "best_model_name = results_df.loc[best_model_idx, 'Model']\n"
    "best_rmse = results_df.loc[best_model_idx, 'RMSE']\n"
    "best_r2 = results_df.loc[best_model_idx, 'R2']\n\n"
    "print(f\"Best Model: {best_model_name} with RMSE of {best_rmse:.4f} and R2 of {best_r2:.4f}\")\n\n"
    "best_pipeline = trained_pipelines[best_model_name]\n"
    "best_model_path = os.path.join(MODELS_DIR, 'best_regression_model.joblib')\n"
    "joblib.dump(best_pipeline, best_model_path)\n"
    "print(f\"Saved pipeline to {best_model_path}\")"
))

# Cell 10: Plot Actual vs Predicted
cells.append(nbformat.v4.new_code_cell(
    "best_preds = best_pipeline.predict(X_test)\n\n"
    "plt.figure(figsize=(10, 8))\n"
    "sns.scatterplot(x=y_test, y=best_preds, alpha=0.5, color='teal', label='Predictions')\n"
    "min_val = min(y_test.min(), best_preds.min())\n"
    "max_val = max(y_test.max(), best_preds.max())\n"
    "plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--', linewidth=2, label='Perfect Fit')\n\n"
    "plt.title(f\"Actual vs Predicted Attendance ({best_model_name})\")\n"
    "plt.xlabel(\"Actual Attendance Percentage (%)\")\n"
    "plt.ylabel(\"Predicted Attendance Percentage (%)\")\n"
    "plt.legend()\n\n"
    "chart_path = os.path.join(CHARTS_DIR, 'regression_actual_vs_predicted.png')\n"
    "plt.tight_layout()\n"
    "plt.savefig(chart_path, dpi=150, bbox_inches='tight')\n"
    "plt.show()"
))

# Populate notebook
nb['cells'] = cells

# Execute notebook programmatically
print("Executing notebook programmatically...")
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
ep.preprocess(nb, {'metadata': {'path': NOTEBOOKS_DIR}})

# Save notebook
with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"Notebook generated, executed, and saved successfully at: {NOTEBOOK_PATH}")
