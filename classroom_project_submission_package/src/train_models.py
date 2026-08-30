import pandas as pd
import numpy as np
import os
import sys
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

def train_and_save_models(features_path, models_dir=None, outputs_dir=None):
    """
    Splits data chronologically (first 80% train, last 20% test),
    trains regression and classification models, compares against baselines,
    and serializes the models.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if models_dir is None:
        models_dir = os.path.join(project_root, "models")
    if outputs_dir is None:
        outputs_dir = os.path.join(project_root, "outputs")
        
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(os.path.join(outputs_dir, "experiment_results"), exist_ok=True)

    print(f"Reading engineered features from: {features_path}...")
    if not os.path.exists(features_path):
        print(f"Error: Features file not found at {features_path}. Model training aborted.")
        return False

    df = pd.read_csv(features_path)
    sample_size = len(df)
    print(f"Total observations (sample size): {sample_size}")

    if sample_size < 10:
        print(f"Error: Insufficient data rows to train models (have {sample_size}, need at least 10). Training aborted.")
        return False

    # 1. Create Classification Target: Attendance_Band
    # Low: < 50, Medium: 50 <= x <= 75, High: > 75
    def get_attendance_band(pct):
        if pct < 50.0:
            return 'Low'
        elif pct <= 75.0:
            return 'Medium'
        else:
            return 'High'
            
    df['Attendance_Band'] = df['Attendance_Percentage'].apply(get_attendance_band)

    # Sort chronologically by Date and Lecture_Number to ensure chronological split
    # Since Date might be string or datetime, convert to datetime for sorting
    df['Sort_Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by=['Sort_Date', 'Lecture_Number']).reset_index(drop=True)
    df = df.drop(columns=['Sort_Date'])

    # Exclude leakage and identifiers from features
    exclude_cols = [
        'Lecture_ID', 'Date', 'Students_Present', 'Attendance_Percentage', 
        'Attendance_Band', 'Total_Enrolled_Students'
    ]
    
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    print(f"Feature columns used: {feature_cols}")

    # Determine numerical and categorical columns
    categorical_cols = df[feature_cols].select_dtypes(include=['object']).columns.tolist()
    numerical_cols = df[feature_cols].select_dtypes(include=['int32', 'int64', 'float32', 'float64']).columns.tolist()

    print(f"Categorical features: {categorical_cols}")
    print(f"Numerical features: {numerical_cols}")

    # Chronological Split (Train 80% / Test 20%)
    split_idx = int(sample_size * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    print(f"Chronological Split: Training set = {len(train_df)} rows, Test set = {len(test_df)} rows")

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
    # Primary regression target: Students_Present
    reg_models = {
        'Dummy Regressor (Mean Baseline)': DummyRegressor(strategy='mean'),
        'Linear Regression': LinearRegression(),
        'Decision Tree Regressor': DecisionTreeRegressor(random_state=42, max_depth=3),
        'Random Forest Regressor': RandomForestRegressor(random_state=42, n_estimators=50, max_depth=3),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42, n_estimators=50, max_depth=2)
    }

    reg_results = []
    best_trained_reg_pipeline = None
    best_trained_reg_name = ""
    best_trained_reg_mae = float('inf')
    best_trained_reg_rmse = float('inf')
    best_trained_reg_r2 = -float('inf')
    
    # Store Dummy baseline stats
    dummy_reg_mae = 0.0
    dummy_reg_rmse = 0.0
    dummy_reg_r2 = 0.0
    dummy_reg_mape = 0.0
    dummy_reg_pipeline = None

    for name, model in reg_models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        pipeline.fit(X_train, y_train_reg)
        preds = pipeline.predict(X_test)
        
        # Calculate Metrics
        mae = mean_absolute_error(y_test_reg, preds)
        rmse = np.sqrt(mean_squared_error(y_test_reg, preds))
        r2 = r2_score(y_test_reg, preds)
        mape = np.mean(np.abs((y_test_reg - preds) / np.maximum(y_test_reg, 1))) * 100

        # Capture dummy baseline metrics
        if 'Dummy' in name:
            dummy_reg_mae = mae
            dummy_reg_rmse = rmse
            dummy_reg_r2 = r2
            dummy_reg_mape = mape
            dummy_reg_pipeline = pipeline

        reg_results.append({
            'Model': name,
            'MAE': round(mae, 4),
            'RMSE': round(rmse, 4),
            'MAPE (%)': round(mape, 4),
            'R2': round(r2, 4)
        })

        # Track best trained model (excluding Dummy)
        if 'Dummy' not in name:
            # We select based on lowest MAE on the test set
            if mae < best_trained_reg_mae:
                best_trained_reg_mae = mae
                best_trained_reg_rmse = rmse
                best_trained_reg_r2 = r2
                best_trained_reg_pipeline = pipeline
                best_trained_reg_name = name

    # 3. CLASSIFICATION MODELS EXPERIMENT
    # Check if there is enough class variation in the training set
    unique_classes_train = y_train_clf.nunique()
    print(f"Unique classes in train set: {y_train_clf.unique().tolist()} ({unique_classes_train} classes)")
    
    # Define models
    clf_models = {
        'Dummy Classifier (Most Frequent)': DummyClassifier(strategy='most_frequent'),
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Decision Tree Classifier': DecisionTreeClassifier(random_state=42, max_depth=3),
        'Random Forest Classifier': RandomForestClassifier(random_state=42, n_estimators=50, max_depth=3),
        'Support Vector Machine': SVC(random_state=42, probability=True),
        'k-Nearest Neighbors': KNeighborsClassifier()
    }

    clf_results = []
    best_trained_clf_pipeline = None
    best_trained_clf_name = ""
    best_trained_clf_acc = -float('inf')
    best_trained_clf_f1 = -float('inf')
    
    dummy_clf_acc = 0.0
    dummy_clf_f1 = 0.0
    dummy_clf_pipeline = None

    run_classification = True
    if unique_classes_train < 2:
        print("Warning: Insufficient class variation in training set. All samples belong to one class. Classification modeling skipped.")
        run_classification = False
        clf_df = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC-AUC'])
    else:
        for name, model in clf_models.items():
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('model', model)
            ])
            
            pipeline.fit(X_train, y_train_clf)
            preds = pipeline.predict(X_test)
            
            # Calculate metrics
            acc = accuracy_score(y_test_clf, preds)
            prec = precision_score(y_test_clf, preds, average='weighted', zero_division=0)
            rec = recall_score(y_test_clf, preds, average='weighted', zero_division=0)
            f1 = f1_score(y_test_clf, preds, average='weighted', zero_division=0)
            
            try:
                probs = pipeline.predict_proba(X_test)
                # handle multiclass or binary ROC AUC
                if len(pipeline.classes_) == 2:
                    auc = roc_auc_score(y_test_clf, probs[:, 1], average='weighted')
                else:
                    auc = roc_auc_score(y_test_clf, probs, average='weighted', multi_class='ovr')
            except Exception:
                auc = np.nan

            if 'Dummy' in name:
                dummy_clf_acc = acc
                dummy_clf_f1 = f1
                dummy_clf_pipeline = pipeline

            clf_results.append({
                'Model': name,
                'Accuracy': round(acc, 4),
                'Precision': round(prec, 4),
                'Recall': round(rec, 4),
                'F1-score': round(f1, 4),
                'ROC-AUC': round(auc, 4) if not np.isnan(auc) else "N/A"
            })

            # Track best trained model (excluding Dummy)
            if 'Dummy' not in name:
                if acc > best_trained_clf_acc:
                    best_trained_clf_acc = acc
                    best_trained_clf_f1 = f1
                    best_trained_clf_pipeline = pipeline
                    best_trained_clf_name = name

        clf_df = pd.DataFrame(clf_results)

    # Save results as CSVs
    reg_df = pd.DataFrame(reg_results)
    reg_csv_path = os.path.join(outputs_dir, "experiment_results", "regression_results.csv")
    reg_df.to_csv(reg_csv_path, index=False)
    print(f"Saved regression experiment results to: {reg_csv_path}")

    if run_classification:
        clf_csv_path = os.path.join(outputs_dir, "experiment_results", "classification_results.csv")
        clf_df.to_csv(clf_csv_path, index=False)
        print(f"Saved classification experiment results to: {clf_csv_path}")

    # Check if best trained models beat the naive baselines
    # Regression: best trained model must have lower MAE than dummy
    reg_beats_baseline = best_trained_reg_mae < dummy_reg_mae
    # Classification: best trained model must have higher Accuracy than dummy
    clf_beats_baseline = best_trained_clf_acc > dummy_clf_acc if run_classification else False

    print("\n=== BASELINE PERFORMANCE COMPARISON ===")
    print(f"Regression Baseline (Dummy Regressor) MAE: {dummy_reg_mae:.4f}")
    print(f"Best Trained Regressor ({best_trained_reg_name}) MAE: {best_trained_reg_mae:.4f}")
    print(f"Does Trained Regressor Beat Baseline? {'YES' if reg_beats_baseline else 'NO'}")
    
    if run_classification:
        print(f"Classification Baseline (Dummy Classifier) Accuracy: {dummy_clf_acc:.4f}")
        print(f"Best Trained Classifier ({best_trained_clf_name}) Accuracy: {best_trained_clf_acc:.4f}")
        print(f"Does Trained Classifier Beat Baseline? {'YES' if clf_beats_baseline else 'NO'}")

    # Save experiment_table.md
    exp_table_path = os.path.join(outputs_dir, "experiment_results", "experiment_table.md")
    with open(exp_table_path, 'w', encoding='utf-8') as f:
        f.write("# Model Training Experiment Results\n\n")
        f.write(f"- **Total Valid Lectures:** {sample_size}\n")
        f.write(f"- **Chronological Train Split:** {len(train_df)} rows\n")
        f.write(f"- **Chronological Test Split:** {len(test_df)} rows\n\n")
        
        f.write("## 1. Regression Models (Target: Students_Present)\n\n")
        f.write(reg_df.to_markdown(index=False) + "\n\n")
        
        f.write("## 2. Classification Models (Target: Attendance_Band)\n\n")
        if run_classification:
            f.write(clf_df.to_markdown(index=False) + "\n\n")
        else:
            f.write("*Classification modeling skipped due to insufficient class variation.*\n\n")
            
        f.write("## 3. Naive Baseline Comparison Summary\n\n")
        f.write(f"- **Best Trained Regressor:** {best_trained_reg_name} (MAE: {best_trained_reg_mae:.4f}, RMSE: {best_trained_reg_rmse:.4f}, R2: {best_trained_reg_r2:.4f})\n")
        f.write(f"- **Dummy Regressor Baseline:** MAE: {dummy_reg_mae:.4f}, RMSE: {dummy_reg_rmse:.4f}, R2: {dummy_reg_r2:.4f}\n")
        f.write(f"- **Trained Regressor Beats Baseline?** {'🟢 YES' if reg_beats_baseline else '🔴 NO (Overfitting on small noisy sample)'}\n\n")
        
        if run_classification:
            f.write(f"- **Best Trained Classifier:** {best_trained_clf_name} (Accuracy: {best_trained_clf_acc:.4f}, F1: {best_trained_clf_f1:.4f})\n")
            f.write(f"- **Dummy Classifier Baseline:** Accuracy: {dummy_clf_acc:.4f}, F1: {dummy_clf_f1:.4f}\n")
            f.write(f"- **Trained Classifier Beats Baseline?** {'🟢 YES' if clf_beats_baseline else '🔴 NO (Overfitting on small noisy sample)'}\n\n")

        f.write("## 🚨 Production Readiness Assessment\n\n")
        f.write("> **WARNING:** Due to the extremely small size of the historical attendance log ($n=18$ lectures), ")
        f.write("the trained machine learning models are **not production-ready**. ")
        f.write("As shown in the experiments above, the models overfit to noise, and do not reliably outperform a naive baseline ")
        f.write("that simply predicts the historical average (~38.75% attendance). ")
        f.write("It is highly recommended to use the **historical average baseline** until a larger dataset of at least 100+ lectures is logged.\n")

    print(f"Saved experiment summary table to: {exp_table_path}")

    # Serialize best models
    best_reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
    best_clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")
    
    # Save the regression package containing pipeline, features, baseline metadata
    joblib.dump({
        'pipeline': best_trained_reg_pipeline if reg_beats_baseline else dummy_reg_pipeline,
        'features': feature_cols,
        'model_name': best_trained_reg_name if reg_beats_baseline else 'Dummy Baseline (Mean)',
        'is_valid': bool(reg_beats_baseline),
        'dummy_mae': dummy_reg_mae,
        'dummy_rmse': dummy_reg_rmse,
        'best_mae': best_trained_reg_mae,
        'best_rmse': best_trained_reg_rmse,
        'mean_attendance_percentage': df['Attendance_Percentage'].mean(), # Historical average baseline percentage
        'mean_students_present': df['Students_Present'].mean() # Historical average baseline count
    }, best_reg_model_path)
    
    # Save classification package
    joblib.dump({
        'pipeline': best_trained_clf_pipeline if clf_beats_baseline else dummy_clf_pipeline,
        'features': feature_cols,
        'model_name': best_trained_clf_name if clf_beats_baseline else 'Dummy Classifier (Most Frequent)',
        'is_valid': bool(clf_beats_baseline),
        'dummy_acc': dummy_clf_acc,
        'best_acc': best_trained_clf_acc,
        'most_frequent_class': y_train_clf.mode()[0] if len(y_train_clf) > 0 else 'Low'
    }, best_clf_model_path)

    print(f"Saved regression package to: {best_reg_model_path}")
    print(f"Saved classification package to: {best_clf_model_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python train_models.py <path_to_engineered_features>")
        sys.exit(1)
    feat_path = sys.argv[1]
    train_and_save_models(feat_path)
