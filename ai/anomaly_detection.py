"""
DAO Governance for AI Model Release
------------------------------------
File: anomaly_detection.py

Purpose:
Detect unusual AI model evaluation records using
Isolation Forest and evaluate the detected anomalies.

The AI computation is performed OFF-CHAIN.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "ai"
    / "data"
    / "model_evaluation_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "ai"
    / "data"
    / "anomaly_detection_results.csv"
)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

data = pd.read_csv(INPUT_FILE)

print("=" * 65)
print("AI MODEL EVALUATION - ANOMALY DETECTION")
print("=" * 65)

print(f"\nInput file: {INPUT_FILE}")
print(f"Total records: {len(data)}")


# ---------------------------------------------------------
# Reconstruct ground-truth anomaly labels
# ---------------------------------------------------------
# The synthetic dataset intentionally injected anomalies
# at these record IDs.

known_anomaly_ids = {11, 36, 71, 121, 161}

data["actual_anomaly"] = data["record_id"].isin(
    known_anomaly_ids
).astype(int)


# ---------------------------------------------------------
# Select AI evaluation features
# ---------------------------------------------------------

features = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "latency_ms",
    "fairness_gap",
    "risk_score"
]

X = data[features].copy()


# ---------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------
# Standardization puts features on comparable scales.
# This is useful because latency is measured in milliseconds,
# while accuracy, fairness gap, and risk score are smaller values.

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ---------------------------------------------------------
# Isolation Forest
# ---------------------------------------------------------

model = IsolationForest(
    n_estimators=200,
    contamination=0.025,
    random_state=42
)

model.fit(X_scaled)


# ---------------------------------------------------------
# Predict anomalies
# ---------------------------------------------------------
# Isolation Forest:
#     1  = normal
#    -1  = anomaly

raw_predictions = model.predict(X_scaled)

data["predicted_anomaly"] = np.where(
    raw_predictions == -1,
    1,
    0
)


# ---------------------------------------------------------
# Anomaly score
# ---------------------------------------------------------

data["anomaly_score"] = -model.decision_function(X_scaled)

data["anomaly_score"] = data["anomaly_score"].round(6)


# ---------------------------------------------------------
# Evaluation metrics
# ---------------------------------------------------------

y_true = data["actual_anomaly"]
y_pred = data["predicted_anomaly"]

accuracy = accuracy_score(y_true, y_pred)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

cm = confusion_matrix(y_true, y_pred)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

data.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nPreprocessing:")
print("- Selected 7 numerical evaluation features")
print("- Applied StandardScaler")
print("- No sensitive or real-world personal data used")

print("\nIsolation Forest:")
print("- Number of trees : 200")
print("- Contamination   : 2.5%")
print("- Random seed     : 42")

print("\nGround-truth anomalies :", int(y_true.sum()))
print("Detected anomalies     :", int(y_pred.sum()))

print("\nEvaluation Metrics")
print("-" * 40)
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nConfusion Matrix")
print(cm)

print("\nDetected anomalous records:")

detected = data[data["predicted_anomaly"] == 1]

print(
    detected[
        [
            "record_id",
            "accuracy",
            "f1_score",
            "latency_ms",
            "fairness_gap",
            "risk_score",
            "anomaly_score"
        ]
    ].to_string(index=False)
)

print("\nResults saved to:")
print(OUTPUT_FILE)

print("\nAnomaly detection completed successfully.")