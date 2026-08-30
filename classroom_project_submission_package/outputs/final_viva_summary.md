# Final Viva Presentation & Defense Summary

This sheet contains questions and concise, scientifically rigorous answers tailored for the Semester III Final Project Viva.

---

## 🔬 Core Metrics (Fact-Based)

- **Total Dataset Size:** 18 valid lecture observations (2026-06-25 to 2026-08-07)
- **Train/Test Partition:** 14 Train (80%) / 4 Test (20%) — chronological split
- **Regression (Students_Present):**
  - Dummy Baseline MAE: **14.5000**
  * Random Forest MAE: **14.0192** (exploratory, marginally beat baseline on 4 rows)
  * RMSE: **15.1268**
  * R²: **0.1174**
  * MAPE: **43.05%**
- **Classification (Attendance_Band):**
  * Dummy Baseline Accuracy: **0.5000**
  * Best Classifier Accuracy: **0.5000** (Logistic Regression, exact tie)
  * Weighted F1-score: **0.3333**
- **Fallback Attendance Average:** **38.75%** (~31 present out of 80)

---

## 🙋 Expected Viva Questions & Answers

### Q1: Why is your dataset so small (n=18)? Is this enough for ML?
> **Answer:** "No, 18 lectures are statistically insufficient for generalizable machine learning, which is a major project limitation we explicitly disclose. This sample represents the initial month of physically verified lecture logs. Rather than generating fake synthetic rows or interpolating missing data, we maintained scientific honesty by running the pipeline on the true sample size. The current ML models are cataloged as exploratory only. The system is designed to fallback automatically to the historical average baseline."

### Q2: Why did you choose a chronological split instead of random cross-validation?
> **Answer:** "Attendance data has a temporal component where features like rolling averages and lagged attendance depend on preceding lectures. A random split would leak future information into past training samples, artificially inflating test accuracy. A chronological 80/20 split mimics real-world conditions where the model must predict future attendance based only on past history."

### Q3: Why is the classification model invalid?
> **Answer:** "The classification model tied the dummy baseline at 0.50 accuracy. Additionally, the 'High' attendance band (>75%) was never observed in any of the 18 lectures. The maximum logged attendance was exactly 75%. Because of this unobserved class and the lack of improvement over the baseline, the classifier is invalid for operational use. The dashboard suppresses automated band decisions."

### Q4: How does your system protect student privacy?
> **Answer:** "By design. We collect only aggregate lecture-level counts (e.g. 35 students present). We do not record, store, or process student names, roll numbers, or college emails, eliminating individual PII risk. Furthermore, instructor identities are anonymized to codes like F_01 or F_02."

### Q5: How do you handle new semester cold-starts?
> **Answer:** "During the first week of a semester when lag values are missing, the feature engineering pipeline automatically imputes lags with the historical subject average. Once history accumulates, the system transitions to dynamic rolling averages."
