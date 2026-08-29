"""
create_submission_package.py
Creates the submission_package directory and copies only the safe, final deliverables.
Ensures private_original_data and raw spreadsheets are strictly excluded.
Logs the copy process and outputs the list of package files.
"""
import os
import shutil

BASE_DIR = r"d:\Data_Science_attendence_project"
SUB_DIR  = os.path.join(BASE_DIR, "submission_package")

# Files to copy (relative source -> relative destination)
FILES_TO_COPY = [
    # Data
    ("data/student_attendance_205_students.csv", "data/student_attendance_205_students.csv"),
    ("data/DATASET_DICTIONARY.md", "data/DATASET_DICTIONARY.md"),
    ("data/SYNTHETIC_DATA_NOTICE.md", "data/SYNTHETIC_DATA_NOTICE.md"),
    
    # Notebooks
    ("notebooks/01_exploratory_data_analysis.ipynb", "notebooks/01_exploratory_data_analysis.ipynb"),
    ("notebooks/02_regression_model.ipynb", "notebooks/02_regression_model.ipynb"),
    ("notebooks/03_classification_model.ipynb", "notebooks/03_classification_model.ipynb"),
    ("notebooks/05_summary_report.ipynb", "notebooks/05_summary_report.ipynb"),
    
    # Models
    ("models/best_regression_model.joblib", "models/best_regression_model.joblib"),
    ("models/best_classification_model.joblib", "models/best_classification_model.joblib"),
    
    # Outputs
    ("outputs/final_project_summary.md", "outputs/final_project_summary.md"),
    ("outputs/final_model_comparison.csv", "outputs/final_model_comparison.csv"),
    
    # Report & Presentation
    ("report/project_report.pdf", "report/project_report.pdf"),
    ("presentation/project_presentation.pptx", "presentation/project_presentation.pptx"),
    ("presentation/presentation_content.md", "presentation/presentation_content.md"),
    ("presentation/viva_questions.md", "presentation/viva_questions.md"),
    
    # Root Files
    ("README.md", "README.md"),
    ("requirements.txt", "requirements.txt"),
]

# Dir to copy completely
DIRS_TO_COPY = [
    ("outputs/charts", "outputs/charts"),
]


def main():
    print("=" * 60)
    print("  CREATING SUBMISSION PACKAGE")
    print("=" * 60)
    
    # Clean recreate target directory
    if os.path.exists(SUB_DIR):
        print(f"Cleaning existing directory: {SUB_DIR}")
        shutil.rmtree(SUB_DIR)
    
    os.makedirs(SUB_DIR, exist_ok=True)
    
    copied_count = 0
    
    # Copy files
    for src_rel, dest_rel in FILES_TO_COPY:
        src_path = os.path.join(BASE_DIR, src_rel)
        dest_path = os.path.join(SUB_DIR, dest_rel)
        
        if os.path.isfile(src_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(src_path, dest_path)
            print(f"  [COPY] {src_rel} -> submission_package/{dest_rel}")
            copied_count += 1
        else:
            print(f"  [MISSING] {src_rel} (Skipped)")

    # Copy directories
    for src_rel, dest_rel in DIRS_TO_COPY:
        src_path = os.path.join(BASE_DIR, src_rel)
        dest_path = os.path.join(SUB_DIR, dest_rel)
        
        if os.path.isdir(src_path):
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(src_path, dest_path)
            print(f"  [COPY DIR] {src_rel} -> submission_package/{dest_rel}")
            # Count files copied inside dir
            for root, _, files in os.walk(dest_path):
                copied_count += len(files)
        else:
            print(f"  [MISSING DIR] {src_rel} (Skipped)")

    print("-" * 60)
    print(f"Package creation finished. Total files copied: {copied_count}")
    print(f"Location: {SUB_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
