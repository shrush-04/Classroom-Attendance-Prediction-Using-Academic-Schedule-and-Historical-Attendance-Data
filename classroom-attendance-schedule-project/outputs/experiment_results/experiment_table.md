# Model Training Experiment Results

- **Total Valid Lectures:** 18
- **Chronological Train Split:** 14 rows
- **Chronological Test Split:** 4 rows

## 1. Regression Models (Target: Students_Present)

| Model                           |     MAE |    RMSE |   MAPE (%) |      R2 |
|:--------------------------------|--------:|--------:|-----------:|--------:|
| Dummy Regressor (Mean Baseline) | 14.5    | 17.1092 |    49.2835 | -0.1291 |
| Linear Regression               | 37.2796 | 42.4341 |   140.353  | -5.9456 |
| Decision Tree Regressor         | 22.2    | 23.6587 |    67.4598 | -1.1591 |
| Random Forest Regressor         | 14.0192 | 15.1268 |    43.0452 |  0.1174 |
| Gradient Boosting Regressor     | 22.4673 | 27.2761 |    53.3059 | -1.8698 |

## 2. Classification Models (Target: Attendance_Band)

| Model                            |   Accuracy |   Precision |   Recall |   F1-score | ROC-AUC   |
|:---------------------------------|-----------:|------------:|---------:|-----------:|:----------|
| Dummy Classifier (Most Frequent) |       0.5  |      0.25   |     0.5  |     0.3333 | N/A       |
| Logistic Regression              |       0.5  |      0.25   |     0.5  |     0.3333 | N/A       |
| Decision Tree Classifier         |       0.5  |      0.25   |     0.5  |     0.3333 | N/A       |
| Random Forest Classifier         |       0.25 |      0.1667 |     0.25 |     0.2    | N/A       |
| Support Vector Machine           |       0.5  |      0.5    |     0.5  |     0.5    | N/A       |
| k-Nearest Neighbors              |       0.5  |      0.5    |     0.5  |     0.5    | N/A       |

## 3. Naive Baseline Comparison Summary

- **Best Trained Regressor:** Random Forest Regressor (MAE: 14.0192, RMSE: 15.1268, R2: 0.1174)
- **Dummy Regressor Baseline:** MAE: 14.5000, RMSE: 17.1092, R2: -0.1291
- **Trained Regressor Beats Baseline?** 🟢 YES

- **Best Trained Classifier:** Logistic Regression (Accuracy: 0.5000, F1: 0.3333)
- **Dummy Classifier Baseline:** Accuracy: 0.5000, F1: 0.3333
- **Trained Classifier Beats Baseline?** 🔴 NO (Overfitting on small noisy sample)

## 🚨 Production Readiness Assessment

> **WARNING:** Due to the extremely small size of the historical attendance log ($n=18$ lectures), the trained machine learning models are **not production-ready**. As shown in the experiments above, the models overfit to noise, and do not reliably outperform a naive baseline that simply predicts the historical average (~38.75% attendance). It is highly recommended to use the **historical average baseline** until a larger dataset of at least 100+ lectures is logged.
