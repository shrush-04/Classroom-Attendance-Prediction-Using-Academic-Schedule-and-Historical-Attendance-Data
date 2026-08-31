# Model Training Experiment Results

- **Total Valid Lectures:** 81
- **Chronological Train Split:** 64 rows
- **Chronological Test Split:** 17 rows

## 1. Regression Models (Target: Students_Present)

| Model                           |     MAE |    RMSE |   MAPE (%) |      R2 |
|:--------------------------------|--------:|--------:|-----------:|--------:|
| Dummy Regressor (Mean Baseline) | 16.4945 | 19.2494 |    56.848  | -0.2442 |
| Linear Regression               | 14.0127 | 18.6003 |    58.0679 | -0.1617 |
| Decision Tree Regressor         | 11.6471 | 16.2682 |    54.5551 |  0.1114 |
| Random Forest Regressor         | 10.0499 | 12.0697 |    46.8818 |  0.5109 |
| Gradient Boosting Regressor     |  8.0334 | 10.7368 |    43.0666 |  0.6129 |

## 2. Classification Models (Target: Attendance_Band)

| Model                            |   Accuracy |   Precision |   Recall |   F1-score | ROC-AUC   |
|:---------------------------------|-----------:|------------:|---------:|-----------:|:----------|
| Dummy Classifier (Most Frequent) |     0.4706 |      0.2215 |   0.4706 |     0.3012 | N/A       |
| Logistic Regression              |     0.7647 |      0.7344 |   0.7647 |     0.7324 | N/A       |
| Decision Tree Classifier         |     0.7647 |      0.7843 |   0.7647 |     0.7385 | N/A       |
| Random Forest Classifier         |     0.6471 |      0.6425 |   0.6471 |     0.5938 | N/A       |
| Support Vector Machine           |     0.5882 |      0.5826 |   0.5882 |     0.5134 | N/A       |
| k-Nearest Neighbors              |     0.5294 |      0.4863 |   0.5294 |     0.4215 | N/A       |

## 3. Naive Baseline Comparison Summary

- **Best Trained Regressor:** Gradient Boosting Regressor (MAE: 8.0334, RMSE: 10.7368, R2: 0.6129)
- **Dummy Regressor Baseline:** MAE: 16.4945, RMSE: 19.2494, R2: -0.2442
- **Trained Regressor Beats Baseline?** 🟢 YES

- **Best Trained Classifier:** Logistic Regression (Accuracy: 0.7647, F1: 0.7324)
- **Dummy Classifier Baseline:** Accuracy: 0.4706, F1: 0.3012
- **Trained Classifier Beats Baseline?** 🟢 YES

## 🚨 Production Readiness Assessment

> **WARNING:** Due to the extremely small size of the historical attendance log ($n=18$ lectures), the trained machine learning models are **not production-ready**. As shown in the experiments above, the models overfit to noise, and do not reliably outperform a naive baseline that simply predicts the historical average (~38.75% attendance). It is highly recommended to use the **historical average baseline** until a larger dataset of at least 100+ lectures is logged.
