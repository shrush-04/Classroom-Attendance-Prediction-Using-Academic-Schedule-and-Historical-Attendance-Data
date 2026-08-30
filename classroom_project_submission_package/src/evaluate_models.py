import pandas as pd
import numpy as np
import os
import sys
import joblib

def evaluate_models(features_path, models_dir=None, charts_dir=None):
    """
    Loads saved models, runs predictions on the test set, and calculates detailed evaluation metrics.
    Generates confusion matrix and actual-vs-predicted plots.
    """
    if models_dir is None:
        models_dir = os.path.join(os.path.dirname(os.path.dirname(features_path)), "models")
    if charts_dir is None:
        charts_dir = os.path.join(os.path.dirname(os.path.dirname(features_path)), "outputs", "charts")
        
    os.makedirs(charts_dir, exist_ok=True)

    reg_model_path = os.path.join(models_dir, "best_present_count_model.joblib")
    clf_model_path = os.path.join(models_dir, "best_attendance_band_model.joblib")

    if not os.path.exists(features_path):
        print(f"Warning: Features file not found at {features_path}. Evaluation skipped.")
        return False
    if not os.path.exists(reg_model_path) or not os.path.exists(clf_model_path):
        print("Warning: Trained model files not found. Run training first. Evaluation skipped.")
        return False

    # Load data
    df = pd.read_csv(features_path)
    if len(df) < 10:
        print("Warning: Insufficient data rows. Evaluation skipped.")
        return False

    # Standardize bands
    def get_attendance_band(pct):
        if pct < 50:
            return 'Low'
        elif pct <= 75:
            return 'Medium'
        else:
            return 'High'
    df['Attendance_Band'] = df['Attendance_Percentage'].apply(get_attendance_band)

    # Chronological Split (Train 80% / Test 20%)
    df = df.sort_values(by=['Date', 'Lecture_Number']).reset_index(drop=True)
    split_idx = int(len(df) * 0.8)
    test_df = df.iloc[split_idx:]

    # Load models
    reg_package = joblib.load(reg_model_path)
    clf_package = joblib.load(clf_model_path)

    reg_pipeline = reg_package['pipeline']
    reg_features = reg_package['features']

    clf_pipeline = clf_package['pipeline']
    clf_features = clf_package['features']

    X_test_reg = test_df[reg_features]
    y_test_reg = test_df['Students_Present']

    X_test_clf = test_df[clf_features]
    y_test_clf = test_df['Attendance_Band']

    print("Evaluating Regression Model...")
    reg_preds = reg_pipeline.predict(X_test_reg)
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    mae = mean_absolute_error(y_test_reg, reg_preds)
    rmse = np.sqrt(mean_squared_error(y_test_reg, reg_preds))
    r2 = r2_score(y_test_reg, reg_preds)
    mape = np.mean(np.abs((y_test_reg - reg_preds) / np.maximum(y_test_reg, 1))) * 100

    print("\n--- REGRESSION METRICS (Target: Students_Present) ---")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    print(f"R-squared Score (R2): {r2:.4f}")

    print("\nEvaluating Classification Model...")
    clf_preds = clf_pipeline.predict(X_test_clf)

    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
    acc = accuracy_score(y_test_clf, clf_preds)
    prec = precision_score(y_test_clf, clf_preds, average='weighted', zero_division=0)
    rec = recall_score(y_test_clf, clf_preds, average='weighted', zero_division=0)
    f1 = f1_score(y_test_clf, clf_preds, average='weighted', zero_division=0)

    print("\n--- CLASSIFICATION METRICS (Target: Attendance_Band) ---")
    print(f"Accuracy Score: {acc:.4f}")
    print(f"Weighted Precision: {prec:.4f}")
    print(f"Weighted Recall: {rec:.4f}")
    print(f"Weighted F1-score: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test_clf, clf_preds, zero_division=0))

    # Generate charts using Matplotlib / Seaborn
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # 1. Regression: Actual vs Predicted
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=y_test_reg, y=reg_preds, alpha=0.7, color='darkblue')
        plt.plot([y_test_reg.min(), y_test_reg.max()], [y_test_reg.min(), y_test_reg.max()], 'r--', lw=2)
        plt.xlabel('Actual Students Present')
        plt.ylabel('Predicted Students Present')
        plt.title('Regression Model: Actual vs Predicted Present Count')
        reg_chart_path = os.path.join(charts_dir, 'regression_actual_vs_predicted.png')
        plt.savefig(reg_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved regression chart to: {reg_chart_path}")

        # 2. Classification: Confusion Matrix
        labels = sorted(df['Attendance_Band'].unique().tolist())
        cm = confusion_matrix(y_test_clf, clf_preds, labels=labels)
        plt.figure(figsize=(7, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted Attendance Band')
        plt.ylabel('Actual Attendance Band')
        plt.title('Classification Model: Confusion Matrix Heatmap')
        cm_chart_path = os.path.join(charts_dir, 'classification_confusion_matrix.png')
        plt.savefig(cm_chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Saved confusion matrix heatmap to: {cm_chart_path}")

    except Exception as e:
        print(f"Could not generate charts because plotting library is unavailable or error occurred: {str(e)}")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python evaluate_models.py <path_to_engineered_features>")
        sys.exit(1)
    feat_path = sys.argv[1]
    evaluate_models(feat_path)
