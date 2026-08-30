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

def main():
    base_dir = r"d:\Data_Science_attendence_project"
    data_path = os.path.join(base_dir, "data", "student_attendance_205_students.csv")
    model_save_path = os.path.join(base_dir, "classroom_project_submission_package", "models", "student_attendance_model.joblib")
    
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    
    # Target column
    target = 'Attendance_Status'
    
    # Feature columns (exclude direct leakage columns like Classes_Attended, Total_Classes, Attendance_Percentage)
    categorical_features = ['Gender', 'Department', 'Year', 'Semester', 'Subject', 'Attendance_Period']
    numeric_features = [
        'Age', 'Previous_Attendance_Percentage', 'Assignment_Score', 
        'Internal_Marks', 'Study_Hours_Per_Week', 'Medical_Leave_Days', 
        'Travel_Distance_KM', 'Previous_Exam_Score', 'Late_Count', 
        'Online_Class_Attendance'
    ]
    
    X = df[categorical_features + numeric_features]
    y = df[target]
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training shapes: {X_train.shape}, Test shapes: {X_test.shape}")
    
    # Create the preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numeric_features)
        ]
    )
    
    # Complete model pipeline
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])
    
    # Train the model
    print("Training Random Forest Classifier...")
    clf.fit(X_train, y_train)
    
    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model package
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump({
        'pipeline': clf,
        'features': {
            'categorical': categorical_features,
            'numeric': numeric_features
        },
        'accuracy': accuracy,
        'classes': clf.classes_.tolist()
    }, model_save_path)
    print(f"Model saved successfully to: {model_save_path}")

if __name__ == '__main__':
    main()
