"""
DAO Governance for AI Model Release
------------------------------------
File: generate_data.py

Purpose:
Generate a reproducible synthetic dataset containing
AI model evaluation and governance-related metrics.

No real or sensitive data is used.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

RANDOM_SEED = 42
NUMBER_OF_RECORDS = 200

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "ai" / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "model_evaluation_data.csv"


# ---------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------

rng = np.random.default_rng(RANDOM_SEED)


# ---------------------------------------------------------
# Generate normal model-evaluation records
# ---------------------------------------------------------

accuracy = np.clip(
    rng.normal(0.91, 0.025, NUMBER_OF_RECORDS),
    0.80,
    0.99
)

precision = np.clip(
    rng.normal(0.90, 0.03, NUMBER_OF_RECORDS),
    0.78,
    0.99
)

recall = np.clip(
    rng.normal(0.89, 0.035, NUMBER_OF_RECORDS),
    0.75,
    0.99
)

f1_score = 2 * (precision * recall) / (precision + recall)

latency_ms = np.clip(
    rng.normal(45, 8, NUMBER_OF_RECORDS),
    20,
    80
)

fairness_gap = np.clip(
    rng.normal(0.045, 0.015, NUMBER_OF_RECORDS),
    0.01,
    0.10
)

risk_score = np.clip(
    rng.normal(0.18, 0.06, NUMBER_OF_RECORDS),
    0.02,
    0.40
)


# ---------------------------------------------------------
# Create DataFrame
# ---------------------------------------------------------

data = pd.DataFrame({
    "record_id": range(1, NUMBER_OF_RECORDS + 1),
    "accuracy": accuracy,
    "precision": precision,
    "recall": recall,
    "f1_score": f1_score,
    "latency_ms": latency_ms,
    "fairness_gap": fairness_gap,
    "risk_score": risk_score
})


# ---------------------------------------------------------
# Add controlled anomalous records
# ---------------------------------------------------------

# These records represent unusual model evaluations.
anomaly_indices = [10, 35, 70, 120, 160]

data.loc[anomaly_indices, "accuracy"] = [
    0.61, 0.67, 0.58, 0.64, 0.69
]

data.loc[anomaly_indices, "precision"] = [
    0.60, 0.65, 0.57, 0.62, 0.66
]

data.loc[anomaly_indices, "recall"] = [
    0.55, 0.63, 0.52, 0.59, 0.61
]

data.loc[anomaly_indices, "latency_ms"] = [
    125, 140, 155, 132, 148
]

data.loc[anomaly_indices, "fairness_gap"] = [
    0.18, 0.21, 0.24, 0.19, 0.22
]

data.loc[anomaly_indices, "risk_score"] = [
    0.72, 0.81, 0.88, 0.76, 0.84
]


# Recalculate F1 after modifying precision and recall.
data["f1_score"] = (
    2 * data["precision"] * data["recall"]
    / (data["precision"] + data["recall"])
)


# ---------------------------------------------------------
# Round numerical values
# ---------------------------------------------------------

numeric_columns = [
    "accuracy",
    "precision",
    "recall",
    "f1_score",
    "latency_ms",
    "fairness_gap",
    "risk_score"
]

data[numeric_columns] = data[numeric_columns].round(4)


# ---------------------------------------------------------
# Save dataset
# ---------------------------------------------------------

data.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Display information
# ---------------------------------------------------------

print("=" * 60)
print("Synthetic AI Model Evaluation Dataset")
print("=" * 60)

print(f"Random seed       : {RANDOM_SEED}")
print(f"Total records     : {len(data)}")
print(f"Injected anomalies: {len(anomaly_indices)}")
print(f"Output file       : {OUTPUT_FILE}")

print("\nFirst 10 records:")
print(data.head(10).to_string(index=False))

print("\nDataset statistics:")
print(data[numeric_columns].describe().round(4))

print("\nDataset generation completed successfully.")