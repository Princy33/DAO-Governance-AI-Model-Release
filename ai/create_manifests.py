"""
DAO Governance for AI Model Release
------------------------------------
File: create_manifests.py

Purpose:
Create reproducible off-chain release manifests from the
AI anomaly-detection results.

The complete manifest remains OFF-CHAIN.
Only its cryptographic digest will later be submitted
to the Solidity governance contract.
"""

from pathlib import Path
import json
import hashlib
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    BASE_DIR
    / "ai"
    / "data"
    / "anomaly_detection_results.csv"
)

MANIFEST_DIR = BASE_DIR / "manifests"

MANIFEST_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Load AI results
# ---------------------------------------------------------

data = pd.read_csv(RESULTS_FILE)

total_records = len(data)

actual_anomalies = int(
    data["actual_anomaly"].sum()
)

detected_anomalies = int(
    data["predicted_anomaly"].sum()
)

normal_records = total_records - detected_anomalies


# ---------------------------------------------------------
# Calculate AI evaluation metrics
# ---------------------------------------------------------

true_positive = int(
    (
        (data["actual_anomaly"] == 1)
        & (data["predicted_anomaly"] == 1)
    ).sum()
)

true_negative = int(
    (
        (data["actual_anomaly"] == 0)
        & (data["predicted_anomaly"] == 0)
    ).sum()
)

false_positive = int(
    (
        (data["actual_anomaly"] == 0)
        & (data["predicted_anomaly"] == 1)
    ).sum()
)

false_negative = int(
    (
        (data["actual_anomaly"] == 1)
        & (data["predicted_anomaly"] == 0)
    ).sum()
)


accuracy = (
    (true_positive + true_negative)
    / total_records
)

precision = (
    true_positive
    / (true_positive + false_positive)
    if (true_positive + false_positive) > 0
    else 0
)

recall = (
    true_positive
    / (true_positive + false_negative)
    if (true_positive + false_negative) > 0
    else 0
)

f1_score = (
    2 * precision * recall / (precision + recall)
    if (precision + recall) > 0
    else 0
)


# ---------------------------------------------------------
# Common evaluation information
# ---------------------------------------------------------

evaluation = {
    "dataset_type": "synthetic",
    "total_records": total_records,
    "actual_anomalies": actual_anomalies,
    "detected_anomalies": detected_anomalies,
    "normal_records": normal_records,
    "accuracy": round(accuracy, 4),
    "precision": round(precision, 4),
    "recall": round(recall, 4),
    "f1_score": round(f1_score, 4),
    "true_positive": true_positive,
    "true_negative": true_negative,
    "false_positive": false_positive,
    "false_negative": false_negative
}


# ---------------------------------------------------------
# Common AI method information
# ---------------------------------------------------------

ai_method = {
    "algorithm": "Isolation Forest",
    "n_estimators": 200,
    "contamination": 0.025,
    "random_seed": 42,
    "preprocessing": [
        "Numerical feature selection",
        "StandardScaler normalization"
    ],
    "features": [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "latency_ms",
        "fairness_gap",
        "risk_score"
    ]
}


# ---------------------------------------------------------
# Manifest 1 - Model v2.0
# ---------------------------------------------------------

manifest_v2 = {
    "manifest_format": "DAO-AI-Release-Manifest-v1",
    "model_name": "SyntheticAIClassifier",
    "model_version": "2.0",
    "model_identifier": "synthetic-ai-classifier-v2",

    "evaluation": evaluation,

    "ai_method": ai_method,

    "risk_assessment": {
        "risk_level": "LOW",
        "risk_score": 0.12,
        "fairness_gap": 0.04,
        "security_review": "completed",
        "privacy_review": "completed"
    },

    "release_policy": {
        "minimum_f1_score": 0.80,
        "maximum_fairness_gap": 0.10,
        "anomaly_review_required": True
    },

    "review": {
        "reviewer_role": "AI Safety Reviewer",
        "review_status": "READY_FOR_DAO_VOTE"
    },

    "release_note": (
        "Model v2.0 satisfies the defined synthetic evaluation "
        "criteria and is submitted for DAO governance review."
    ),

    "limitation": (
        "Evaluation uses synthetic data with intentionally injected "
        "anomalies. Results should not be interpreted as proof of "
        "real-world model performance."
    )
}


# ---------------------------------------------------------
# Manifest 2 - Model v3.0
# ---------------------------------------------------------

manifest_v3 = {
    "manifest_format": "DAO-AI-Release-Manifest-v1",
    "model_name": "SyntheticAIClassifier",
    "model_version": "3.0",
    "model_identifier": "synthetic-ai-classifier-v3",

    "evaluation": evaluation,

    "ai_method": ai_method,

    "risk_assessment": {
        "risk_level": "MEDIUM",
        "risk_score": 0.28,
        "fairness_gap": 0.08,
        "security_review": "completed",
        "privacy_review": "completed"
    },

    "release_policy": {
        "minimum_f1_score": 0.80,
        "maximum_fairness_gap": 0.10,
        "anomaly_review_required": True
    },

    "review": {
        "reviewer_role": "AI Safety Reviewer",
        "review_status": "READY_FOR_DAO_VOTE"
    },

    "release_note": (
        "Model v3.0 is submitted as a second governance proposal "
        "for demonstrating an insufficient-quorum outcome."
    ),

    "limitation": (
        "Evaluation uses synthetic data with intentionally injected "
        "anomalies. Results should not be interpreted as proof of "
        "real-world model performance."
    )
}


# ---------------------------------------------------------
# Write JSON manifests
# ---------------------------------------------------------

manifest_v2_file = MANIFEST_DIR / "manifest_v2.json"
manifest_v3_file = MANIFEST_DIR / "manifest_v3.json"

with open(
    manifest_v2_file,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        manifest_v2,
        file,
        indent=4
    )


with open(
    manifest_v3_file,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        manifest_v3,
        file,
        indent=4
    )


# ---------------------------------------------------------
# SHA-256 digest function
# ---------------------------------------------------------

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(
            lambda: file.read(4096),
            b""
        ):
            sha256.update(block)

    return sha256.hexdigest()


digest_v2 = calculate_sha256(
    manifest_v2_file
)

digest_v3 = calculate_sha256(
    manifest_v3_file
)


# ---------------------------------------------------------
# Save digest information
# ---------------------------------------------------------

hash_file = MANIFEST_DIR / "hashes.txt"

with open(
    hash_file,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "DAO Governance for AI Model Release\n"
    )

    file.write(
        "Manifest SHA-256 Digests\n"
    )

    file.write(
        "=" * 60 + "\n\n"
    )

    file.write(
        f"manifest_v2.json\n{digest_v2}\n\n"
    )

    file.write(
        f"manifest_v3.json\n{digest_v3}\n\n"
    )


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("=" * 65)
print("AI RELEASE MANIFEST GENERATION")
print("=" * 65)

print("\nAI evaluation summary:")
print(f"Total records       : {total_records}")
print(f"Actual anomalies    : {actual_anomalies}")
print(f"Detected anomalies  : {detected_anomalies}")
print(f"Accuracy             : {accuracy:.4f}")
print(f"Precision            : {precision:.4f}")
print(f"Recall               : {recall:.4f}")
print(f"F1 Score             : {f1_score:.4f}")

print("\nManifest files:")

print(
    f"manifest_v2.json -> {manifest_v2_file}"
)

print(
    f"manifest_v3.json -> {manifest_v3_file}"
)

print("\nSHA-256 digests:")

print(
    f"v2: {digest_v2}"
)

print(
    f"v3: {digest_v3}"
)

print("\nDigest file:")
print(hash_file)

print("\nManifest generation completed successfully.")