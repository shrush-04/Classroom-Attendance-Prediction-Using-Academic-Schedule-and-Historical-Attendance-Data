import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

def train_and_save_models(features_path, models_dir=None, outputs_dir=None):
    """
    Splits data chronologically, trains multiple regression and classification models,
    selects the best models, and serializes them.
    """
    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(os.path.dirname(features_path)), "models")
    if outputs_dir is None:
        outputs_dir = os.path.join(os.path.dirname(os.path.dirname(features_path)), "outputs")
        
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(os.path.join(outputs_dir, "experiment_results"), exist_ok=True)

    print(f"Reading engineered features from: {features_path}...")
    if not os.path.exists(features_path):
        print(f"Warning: Features file not found at {features_path}. Model training skipped.")
        return False

    df = pd.read_csv(features_path)
    if len(df) < 10:
        print("Warning: Insufficient data rows to train models (need at least 10 rows). Training skipped.")
        return False

    # Define targets and features
    # Primary regression target: Students_Present
    # Classification target: Attendance_Band
    # Secondary regression target: Attendance_Percentage (trained as secondary model if needed, but primary is Students_Present)
    
    # 1. Create Classification Target: Attendance_Band
    # Low: < 50, Medium: 50 <= x <= 75, High: > 75
    def get_attendance_band(pct):
        if pct < 50:
            return 'Low'
        elif pct <= 75:
            return 'Medium'
        else:
            return 'High'
            
    df['Attendance_Band'] = df['Attendance_Percentage'].apply(get_attendance_band)

    # Sort chronologically by Date and Lecture_Number to ensure chronological split
    df = df.sort_values(by=['Date', 'Lecture_Number']).reset_index(drop=True)

    # Exclude leakage and identifiers from features
    exclude_cols = [
        'Lecture_ID', 'Date', 'Students_Present', 'Attendance_Percentage', 
        'Attendance_Band', 'Total_Enrolled_Students' # Total enrolled is used in target calculations, but can it be an input? 
        # Wait, Total_Enrolled_Students is needed in features to predict Students_Present, but let's keep it if we want.
        # Actually, let's keep Total_Enrolled_Students because a model needs to know the class capacity to predict how many are present!
        # The prompt says: "Exclude from model input: Students_Present, Attendance_Percentage, Attendance_Band, Lecture_ID, Any feature calculated from current attendance, Any future information."
        # Total_Enrolled_Students is an administrative schedule property known beforehand, so we can keep it as an input!
    ]
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    print(f"Feature columns: {feature_cols}")

    # Determine numerical and categorical columns
    categorical_cols = df[feature_cols].select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df[feature_cols].select_dtypes(include=['int32', 'int64', 'float32', 'float64']).columns.tolist()

    print(f"Categorical features: {categorical_cols}")
    print(f"Numerical features: {numerical_cols}")

    # Chronological Split (Train 80% / Test 20%)
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    X_train = train_df[feature_cols]
    y_train_reg = train_df['Students_Present']
    y_train_clf = train_df['Attendance_Band']

    X_test = test_df[feature_cols]
    y_test_reg = test_df['Students_Present']
    y_test_clf = test_df['Attendance_Band']

    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='Not_Collected')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # 2. REGRESSION MODELS EXPERIMENT
    reg_models = {
        'Linear Regression': LinearRegression(),
        'Decision Tree Regressor': DecisionTreeRegressor(random_state=42, max_depth=5),
        'Random Forest Regressor': RandomForestRegressor(random_state=42, n_estimators=100, max_depth=8),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42, n_estimators=100, max_depth=4)
    }

    reg_results = []
    best_reg_score = -float('inf')
    best_reg_pipeline = None
    best_reg_name = ""

    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    for name, model in reg_models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train_reg)
        
        # Predict
        preds = pipeline.predict(X_test)
        
        # Evaluate
        mae = mean_absolute_error(y_test_reg, preds)
        rmse = np.sqrt(mean_squared_error(y_test_reg, preds))
        r2 = r2_score(y_test_reg, preds)
        
        # Calculate MAPE (handling division by zero just in case)
        mape = np.mean(np.abs((y_test_reg - preds) / np.maximum(y_test_reg, 1))) * 100

        reg_results.append({
            'Model': name,
            'MAE': round(mae, 4),
            'RMSE': round(rmse, 4),
            'MAPE (%)': round(mape, 4),
            'R2': round(r2, 4)
        })

        # Track best model by R2 (or MAE)
        if r2 > best_reg_score:
            best_reg_score = r2
            best_reg_pipeline = pipeline
            best_reg_name = name

    # 3. CLASSIFICATION MODELS EXPERIMENT
    clf_models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree Classifier': DecisionTreeClassifier(random_state=42, max_depth=5),
        'Random Forest Classifier': RandomForestClassifier(random_state=42, n_estimators=100, max_depth=8),
        'Support Vector Machine': SVC(random_state=42, probability=True),
        'k-Nearest Neighbors': KNeighborsClassifier()
    }

    clf_results = []
    best_clf_score = -float('inf')
    best_clf_pipeline = None
    best_clf_name = ""

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

    for name, model in clf_models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        # Train
        pipeline.fit(X_train, y_train_clf)
        
        # Predict
        preds = pipeline.predict(X_test)
        
        # Evaluate metrics
        acc = accuracy_score(y_test_clf, preds)
        
        # Handle multiclass metrics
        prec = precision_score(y_test_clf, preds, average='weighted', zero_division=0)
        rec = recall_score(y_test_clf, preds, average='weighted', zero_division=0)
        f1 = f1_score(y_test_clf, preds, average='weighted', zero_division=0)
        
        try:
            # Predict probabilities
            probs = pipeline.predict_proba(X_test)
            auc = roc_auc_score(y_test_clf, probs, average='weighted', multi_class='ovr')
        except Exception:
            auc = np.nan

        clf_results.append({
            'Model': name,
            'Accuracy': round(acc, 4),
            'Precision': round(prec, 4),
            'Recall': round(rec, 4),
            'F1-score': round(f1, 4),
            'ROC-AUC': round(auc, 4) if not np.isnan(auc) else "N/A"
        })

        if acc > best_clf_score:
            best_clf_score = acc
            best_clf_pipeline = pipeline
            best_clf_name = name

    # Save results as CSVs
    reg_df = pd.DataFrame(reg_results)
    clf_df = pd.DataFrame(clf_results)
    
    reg_csv_path = os.path.join(outputs_dir, "experiment_results", "regression_results.csv")
    clf_csv_path = os.path.join(outputs_dir, "experiment_results", "classification_results.csv")
    reg_df.to_csv(reg_csv_path, index=False)
    clf_df.to_csv(clf_csv_path, index=False)

    print(f"Saved regression experiment results to: {reg_csv_path}")
    print(f"Saved classification experiment results to: {clf_csv_path}")

    # Generate experiment_table.md
    exp_table_path = os.path.join(outputs_dir, "experiment_results", "experiment_table.md")
    with open(exp_table_path, 'w', encoding='utf-8') as f:
        f.write("# Model Training Experiment Results\n\n")
        f.write("This table summarizes the performance of multiple machine learning models trained on the classroom attendance dataset.\n\n")
        f.write("## 1. Regression Models (Target: Students_Present)\n\n")
        f.write(reg_df.to_markdown(index=False) + "\n\n")
        f.write("## 2. Classification Models (Target: Attendance_Band)\n\n")
        f.write(clf_df.to_markdown(index=False) + "\n\n")
        f.write(f"**Best Regression Model:** {best_reg_name} (R2: {best_reg_score:.4f})\n\n")
        f.write(f"**Best Classification Model:** {best_clf_name} (Accuracy: {best_clf_score:.4f})\n")

    print(f"Saved experiment summary table to: {exp_table_path}")

    # Save best models
    best_reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
    best_clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")
    
    # Save the pipeline object which contains column transformers and the model
    # Pack feature column names as metadata inside the model dictionary or save pipeline directly
    joblib.dump({
        'pipeline': best_reg_pipeline,
        'features': feature_cols,
        'model_name': best_reg_name
    }, best_reg_model_path)
    
    joblib.dump({
        'pipeline': best_clf_pipeline,
        'features': feature_cols,
        'model_name': best_clf_name
    }, best_clf_model_path)

    print(f"Saved best regression model to: {best_reg_model_path}")
    print(f"Saved best classification model to: {best_clf_model_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python train_models.py <path_to_engineered_features>")
        sys.exit(1)
    feat_path = sys.argv[1]
    train_and_save_models(feat_path)
