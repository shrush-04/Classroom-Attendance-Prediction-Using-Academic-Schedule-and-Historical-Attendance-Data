"""
generate_classification_notebook.py
Programmatically generates and executes notebooks/03_classification_model.ipynb
"""

import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

BASE_DIR = r"d:\Data_Science_attendence_project"
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)
NOTEBOOK_PATH = os.path.join(NOTEBOOKS_DIR, "03_classification_model.ipynb")

# Initialize notebook structure
nb = nbformat.v4.new_notebook()

# Define cells
cells = []

# Cell 1: Header & Introduction
cells.append(nbformat.v4.new_markdown_cell(
    "# Phase 4: Early Warning System using Classification Models\n"
    "**Project:** Privacy-Preserving Synthetic Student Attendance Analysis and Prediction System\n\n"
    "This notebook trains and evaluates classification models to predict whether a student's attendance is **At Risk** (`Defaulter`, attendance < 75%) or **Safe** (`Regular`, attendance >= 75%).\n\n"
    "### ⚠️ Data Leakage Warning\n"
    "Just as in the regression module, we exclude `Attendance_Percentage`, `Classes_Attended`, `Total_Classes`, and `Attendance_Period` from the feature set. Because `Attendance_Status` is derived directly from `Attendance_Percentage`, keeping these variables would lead to direct data leakage, bypassing the model's ability to learn general student behavioral patterns.\n\n"
    "### 🎓 Ethical Early-Warning System Disclaimer\n"
    "This model is built as an **early-intervention support tool** to help identify students who may need additional academic counseling or resources. It is **not** intended for automatic punishment, grading penalties, or disciplinary action. The goal is to proactively flag students in danger of falling behind so educators can engage them with support and guidance."
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
    "from sklearn.linear_model import LogisticRegression\n"
    "from sklearn.tree import DecisionTreeClassifier\n"
    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
    "from sklearn.metrics import (\n"
    "    accuracy_score, precision_score, recall_score, f1_score,\n"
    "    roc_auc_score, confusion_matrix, ConfusionMatrixDisplay\n"
    ")\n\n"
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

# Cell 4: Target Mapping and Feature Setup
cells.append(nbformat.v4.new_code_cell(
    "target_col = 'Attendance_Status'\n"
    "# Map Defaulter (At Risk) to 1, Regular (Safe) to 0\n"
    "y = df[target_col].map({'Regular': 0, 'Defaulter': 1})\n\n"
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
    "X = df[all_predictors]\n\n"
    "print(f\"Predictors shape: {X.shape}\")\n"
    "print(f\"Target distribution:\\n{y.value_counts(normalize=True) * 100}\")"
))

# Cell 5: Train-Test Split with Stratify
cells.append(nbformat.v4.new_code_cell(
    "X_train, X_test, y_train, y_test = train_test_split(\n"
    "    X, y, test_size=0.2, random_state=42, stratify=y\n"
    ")\n"
    "print(f\"Train set shape: {X_train.shape} (Defaulter ratio: {y_train.mean():.4f})\")\n"
    "print(f\"Test set shape: {X_test.shape} (Defaulter ratio: {y_test.mean():.4f})\")"
))

# Cell 6: Preprocessing Pipelines
cells.append(nbformat.v4.new_code_cell(
    "cat_transformer = Pipeline(steps=[\n"
    "    ('imputer', SimpleImputer(strategy='most_frequent')),\n"
    "    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
    "])\n\n"
    "num_transformer = Pipeline(steps=[\n"
    "    ('imputer', SimpleImputer(strategy='median')),\n"
    "    ('scaler', StandardScaler())\n"
    "])\n\n"
    "preprocessor = ColumnTransformer(transformers=[\n"
    "    ('num', num_transformer, numeric_cols),\n"
    "    ('cat', cat_transformer, categorical_cols)\n"
    "])\n"
    "print(\"Preprocessing pipelines defined.\")"
))

# Cell 7: Model Definitions and Evaluation
cells.append(nbformat.v4.new_code_cell(
    "models = {\n"
    "    'LogisticRegression': LogisticRegression(random_state=42, max_iter=1000),\n"
    "    'DecisionTreeClassifier': DecisionTreeClassifier(random_state=42, max_depth=6),\n"
    "    'RandomForestClassifier': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=10),\n"
    "    'GradientBoostingClassifier': GradientBoostingClassifier(random_state=42, n_estimators=100, learning_rate=0.1)\n"
    "}\n\n"
    "results = []\n"
    "trained_pipelines = {}\n\n"
    "for name, model in models.items():\n"
    "    pipeline = Pipeline(steps=[\n"
    "        ('preprocessor', preprocessor),\n"
    "        ('classifier', model)\n"
    "    ])\n"
    "    # Train\n"
    "    pipeline.fit(X_train, y_train)\n"
    "    trained_pipelines[name] = pipeline\n"
    "    \n"
    "    # Predict\n"
    "    y_pred = pipeline.predict(X_test)\n"
    "    y_prob = pipeline.predict_proba(X_test)[:, 1]\n"
    "    \n"
    "    # Evaluate\n"
    "    acc = accuracy_score(y_test, y_pred)\n"
    "    prec = precision_score(y_test, y_pred)\n"
    "    rec = recall_score(y_test, y_pred)\n"
    "    f1 = f1_score(y_test, y_pred)\n"
    "    auc = roc_auc_score(y_test, y_prob)\n"
    "    \n"
    "    print(f\"{name:28} -> Acc: {acc:.4f}, Prec: {prec:.4f}, Rec: {rec:.4f}, F1: {f1:.4f}, AUC: {auc:.4f}\")\n"
    "    results.append({\n"
    "        'Model': name,\n"
    "        'Accuracy': acc,\n"
    "        'Precision': prec,\n"
    "        'Recall': rec,\n"
    "        'F1-score': f1,\n"
    "        'ROC-AUC': auc\n"
    "    })"
))

# Cell 8: Save Metrics Table
cells.append(nbformat.v4.new_code_cell(
    "results_df = pd.DataFrame(results)\n"
    "results_csv_path = os.path.join(OUTPUTS_DIR, 'classification_model_results.csv')\n"
    "results_df.to_csv(results_csv_path, index=False)\n"
    "print(\"Saved results table.\")\n"
    "results_df"
))

# Cell 9: Select Best Classifier & Save
cells.append(nbformat.v4.new_code_cell(
    "# Sort by F1-score first, then Recall\n"
    "best_model_idx = results_df.sort_values(by=['F1-score', 'Recall'], ascending=False).index[0]\n"
    "best_model_name = results_df.loc[best_model_idx, 'Model']\n"
    "best_f1 = results_df.loc[best_model_idx, 'F1-score']\n"
    "best_recall = results_df.loc[best_model_idx, 'Recall']\n"
    "best_acc = results_df.loc[best_model_idx, 'Accuracy']\n\n"
    "print(f\"Best Classifier: {best_model_name} with Accuracy={best_acc:.4f}, F1={best_f1:.4f}, Recall={best_recall:.4f}\")\n\n"
    "best_pipeline = trained_pipelines[best_model_name]\n"
    "best_model_path = os.path.join(MODELS_DIR, 'best_classification_model.joblib')\n"
    "joblib.dump(best_pipeline, best_model_path)\n"
    "print(f\"Saved pipeline to {best_model_path}\")"
))

# Cell 10: Plot Confusion Matrix
cells.append(nbformat.v4.new_code_cell(
    "best_preds = best_pipeline.predict(X_test)\n"
    "cm = confusion_matrix(y_test, best_preds)\n\n"
    "plt.figure(figsize=(8, 7))\n"
    "disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Regular', 'Defaulter'])\n"
    "disp.plot(cmap='Blues', values_format='d')\n"
    "plt.title(f\"Confusion Matrix - Best Classifier ({best_model_name})\")\n"
    "plt.grid(False)\n\n"
    "chart_path = os.path.join(CHARTS_DIR, 'best_classifier_confusion_matrix.png')\n"
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
