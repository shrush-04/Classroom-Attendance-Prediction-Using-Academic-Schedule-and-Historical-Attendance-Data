# Privacy and Ethical Guidelines

This project is built from the ground up using **Privacy by Design** principles. Student attendance analysis is crucial for academic planning, but tracking individuals poses privacy risks. This policy sets out the rules governing this project.

## 1. Zero Student-Level Records
- **No Personal Identifiers:** Student names, university roll numbers, mobile numbers, and email IDs must **never** be collected, imported, or stored in any project database, template, or code.
- **No Individual Mapping:** Under no circumstances should a mapping table be created that links student names to any internal ID.
- **Biometrics and Photos:** Photographic records, facial recognition databases, fingerprint logs, or other biometric metadata are strictly prohibited.

## 2. Aggregate Data Model
- The unit of analysis is the **Lecture Session** (not the student).
- Each record represents the state of a single class hour/session.
- Data features are limited to calendar markers, timetable properties, weather, assignment status, and the **aggregate sum** of present students (`Students_Present`).
- By predicting attendance at the lecture level, we protect the privacy of individual students while still providing valuable scheduling insights to the department.

## 3. Faculty Privacy
- Faculty names must not be logged.
- Every instructor is assigned an encoded string, e.g. `F001`, `F002`, to allow the model to capture instructor-specific attendance variances without identifying individual faculty members.

## 4. Academic Integrity
- **No Data Fabrication:** We will not generate fake attendance entries to pad the dataset.
- **No Fictional Metrics:** Performance indicators (R2, MAE, Accuracy) will only be computed and reported when physically verified original lecture records are placed in the dataset directory.
