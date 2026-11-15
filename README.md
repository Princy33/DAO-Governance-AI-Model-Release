# 🚀 DAO Governance for AI Model Release

<h3 align="center">🔗 Decentralized Governance | 🤖 Artificial Intelligence | 🔐 Blockchain Security</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" />
  <img src="https://img.shields.io/badge/Solidity-0.8.24-black?logo=solidity" />
  <img src="https://img.shields.io/badge/AI-Isolation%20Forest-green" />
  <img src="https://img.shields.io/badge/Blockchain-Remix%20VM-orange" />
  <img src="https://img.shields.io/badge/Status-Completed-success" />
</p>

---

## 🌟 Project Overview

**DAO Governance for AI Model Release** is a blockchain-based decentralized governance framework designed to manage and approve AI model releases through transparent and auditable voting.

The project combines an **off-chain AI anomaly detection pipeline** with an **on-chain DAO governance smart contract**.

🤖 The AI component performs synthetic data generation, preprocessing, anomaly detection, evaluation, and model manifest generation.

🔗 The blockchain component manages model release proposals, registered-member voting, quorum validation, and governance decisions.

🔐 SHA-256 manifest digests provide a cryptographic reference to the AI model metadata stored off-chain.

The project demonstrates how Artificial Intelligence and Blockchain can work together to establish a transparent and accountable AI model release approval process.

## 🎯 Project Objectives

- 🤖 Develop an AI-based anomaly detection pipeline.
- 📊 Generate reproducible synthetic evaluation data.
- 🔍 Detect anomalous records using Isolation Forest.
- 📄 Generate AI model manifests.
- 🔐 Generate SHA-256 cryptographic digests.
- ⛓️ Store model versions and manifest digests on-chain.
- 🗳️ Implement registered-member voting.
- 👥 Enforce one-member-one-vote.
- ⚖️ Implement quorum and majority validation.
- 🚫 Prevent duplicate proposals and voting.
- 📋 Maintain transparent proposal lifecycle records.

---

## 🏗️ System Architecture

The system follows a hybrid architecture consisting of two major components.

### 🤖 1. Off-Chain AI Pipeline

```text
       📊 Synthetic Dataset
                |
                v
       ⚙️ Data Preprocessing
                |
                v
        StandardScaler
                |
                v
       🌲 Isolation Forest
                |
                v
       🔍 Anomaly Detection
                |
                v
       📈 Evaluation Results
                |
                v
        📄 Model Manifest
                |
                v
        🔐 SHA-256 Digest
```

### 🔗 2. On-Chain DAO Governance

```text
    📄 Model Version + Manifest Hash
                    |
                    v
            📝 Create Proposal
                    |
                    v
              🗳️ Member Voting
                    |
                    v
              ⚖️ Quorum Check
                    |
                    v
             Majority Validation
                    |
           +--------+--------+
           |                 |
           v                 v
      ✅ Succeeded       ❌ Defeated
           |
           v
        📥 Queue
           |
           v
       🚀 Execute
```

### 🔄 Overall Workflow

1. Generate synthetic AI evaluation data.
2. Detect anomalies using the AI pipeline.
3. Generate model evaluation results.
4. Create model manifests.
5. Generate SHA-256 manifest digests.
6. Submit model version and digest as a DAO proposal.
7. Allow registered members to vote.
8. Validate quorum and majority conditions.
9. Finalize, queue, and execute successful proposals.

---

## 🛠️ Technologies Used

| Category | Technologies |
|---|---|
| 💻 Programming | Python |
| 📊 Data Processing | NumPy, Pandas |
| 🤖 Machine Learning | Scikit-learn |
| 🔍 Anomaly Detection | Isolation Forest |
| ⚙️ Preprocessing | StandardScaler |
| ⛓️ Blockchain | Remix VM (Cancun) |
| 📜 Smart Contract | Solidity |
| 🔐 Cryptography | SHA-256 |
| 🧰 Development | Visual Studio Code, Remix IDE |
| 🌐 Version Control | Git, GitHub |

---

## 📂 Project Structure

```text
DAO_Governance_AI_Model_Release/
│
├── 🤖 ai/
│   ├── 📁 data/
│   │   ├── anomaly_detection_results.csv
│   │   └── model_evaluation_data.csv
│   │
│   ├── anomaly_detection.py
│   ├── create_manifests.py
│   └── generate_data.py
│
├── ⛓️ contracts/
│   └── DAOGovernance.sol
│
├── 🔐 manifests/
│   ├── hashes.txt
│   ├── manifest_v2.json
│   └── manifest_v3.json
│
├── 📸 screenshots/
│   └── Remix deployment and testing evidence
│
├── 🖥️ app.py
├── 📦 requirements.txt
├── 🚫 .gitignore
└── 📖 README.md
```

---

## 🤖 AI-Based Anomaly Detection

The AI component uses a synthetic dataset to demonstrate anomaly detection in AI evaluation records.

### 📊 Dataset Configuration

| Parameter | Value |
|---|---:|
| Total Records | 200 |
| Injected Anomalies | 5 |
| Algorithm | Isolation Forest |
| Estimators | 200 |
| Contamination | 2.5% |
| Random State | 42 |
| Preprocessing | StandardScaler |

### 📈 Experimental Results

| Evaluation Metric | Result |
|---|---:|
| Accuracy | 1.0000 |
| Precision | 1.0000 |
| Recall | 1.0000 |
| F1 Score | 1.0000 |
| Injected Anomalies | 5 |
| Detected Anomalies | 5 |

<details>
<summary>🔍 View AI Pipeline Details</summary>

- Generate 200 synthetic evaluation records.
- Inject five intentional anomalies.
- Standardize numerical features.
- Apply Isolation Forest.
- Predict normal and anomalous records.
- Compare predictions against known synthetic labels.
- Generate evaluation results.

</details>

⚠️ **AI Limitation:** The dataset contains intentionally injected synthetic anomalies. The perfect experimental results demonstrate the pipeline's behaviour and do not establish perfect real-world anomaly detection.

---

## 🔐 Model Manifest & SHA-256 Verification

The project generates JSON manifests containing model-related governance metadata.

### 📄 Generated Manifests

- `manifest_v2.json`
- `manifest_v3.json`

Their SHA-256 digests are stored in `manifests/hashes.txt`.

### 🔑 Manifest Hashes

| Manifest | SHA-256 Digest |
|---|---|
| Version 2 | `98b687886a77f68e3dca2770839344087b7d4847cbfb31176517cf61d53c11bd` |
| Version 3 | `bb8f51225c948c837c5e9bc1087cbc131b121a177b2af3c1889849c990cbccbf` |

🔐 **Purpose:** The SHA-256 digest provides a cryptographic commitment to the referenced manifest contents and helps identify changes.

⚠️ A matching digest does not independently prove the correctness or truthfulness of the underlying AI evaluation information.

---

## ⛓️ DAO Governance Smart Contract

The governance mechanism is implemented using Solidity.

📁 **Contract Location:** `contracts/DAOGovernance.sol`

**Solidity Version:** `^0.8.24`

### ⚖️ Governance Rules

| Governance Rule | Description |
|---|---|
| 👥 Member Registration | Only registered members can vote. |
| 🗳️ Voting Restriction | One vote per member per proposal. |
| 📊 Quorum | Minimum 3 votes required. |
| ✅ Majority | YES votes must exceed NO votes. |
| ⚖️ Tie Handling | A tie results in a defeated proposal. |
| ⏳ Voting Period | Voting must close before finalization. |
| 📥 Proposal Queue | Successful proposals must be queued. |
| 🚀 Execution | Queued successful proposals can be executed. |
| 🚫 Duplicate Prevention | Duplicate model version and digest combinations are rejected. |
| 🛡️ Emergency Control | Emergency pause mechanism is provided. |

### ⚙️ Smart Contract Functions

**👥 Member Management**
- `registerMember()`
- `removeMember()`

**📝 Proposal Management**
- `createProposal()`
- `finalizeProposal()`
- `queueProposal()`
- `executeProposal()`
- `cancelProposal()`

**🗳️ Voting**
- `vote()`

**🛡️ Emergency Control**
- `setEmergencyPause()`

**📋 Information Functions**
- `getProposal()`
- `getProposalCount()`
- `getTotalVotes()`
- `quorumReached()`

---

## 🔄 Proposal Lifecycle

The smart contract supports seven proposal states:

| State | Description |
|---|---|
| ⏳ Pending | Proposal awaiting activation |
| 🟢 Active | Voting is in progress |
| ✅ Succeeded | Quorum and majority conditions satisfied |
| ❌ Defeated | Proposal failed governance requirements |
| 📥 Queued | Successful proposal added to execution queue |
| 🚀 Executed | Proposal execution completed |
| 🚫 Cancelled | Proposal cancelled |

### ✅ Successful Proposal

```text
🟢 Active
    |
    v
✅ Succeeded
    |
    v
📥 Queued
    |
    v
🚀 Executed
```

### ❌ Failed Proposal

```text
🟢 Active
    |
    v
❌ Defeated
```

---

## 🚀 Blockchain Deployment

The smart contract was compiled and deployed using **Remix IDE**.

| Configuration | Details |
|---|---|
| IDE | Remix IDE |
| Virtual Machine | Remix VM (Cancun) |
| Language | Solidity |
| Compiler | Solidity ^0.8.24 |
| Execution | Local Blockchain Environment |
| Real Ether | Not Required |

🔗 The deployment and testing process was performed in a local Remix VM environment.

---

## 🧪 Testing & Experimental Validation

The project includes successful governance scenarios and negative test cases.

### 🟢 1. Successful Proposal

Proposal 1 was created using model version `2.0` and the v2 manifest digest.

| Parameter | Result |
|---|---:|
| Proposal ID | 1 |
| Model Version | 2.0 |
| YES Votes | 4 |
| NO Votes | 1 |
| Total Votes | 5 |
| Required Quorum | 3 |
| Final Status | Executed |

**Observed Lifecycle:**

`✅ Succeeded → 📥 Queued → 🚀 Executed`

### 🔴 2. Quorum Failure

Proposal 3 recorded the following voting results:

| Parameter | Result |
|---|---:|
| YES Votes | 2 |
| NO Votes | 0 |
| Total Votes | 2 |
| Required Quorum | 3 |
| Final Status | Defeated |

❌ The proposal was defeated because the total votes did not meet the minimum quorum requirement.

### 🛡️ 3. Negative Test Cases

| Test Scenario | Expected Behaviour | Result |
|---|---|---|
| Duplicate Vote | Reject repeated voting | ✅ Passed |
| Unregistered Voter | Reject unauthorized voting | ✅ Passed |
| Early Finalization | Prevent premature finalization | ✅ Passed |
| Late Voting | Reject voting after deadline | ✅ Passed |
| Already Finalized Proposal | Prevent repeated finalization | ✅ Passed |
| Duplicate Proposal | Reject duplicate model version and digest | Tested |

### ⚠️ Error Messages Verified

| Scenario | Contract Response |
|---|---|
| Duplicate Vote | `Member has already voted` |
| Unregistered Voter | `Only registered members can vote` |
| Early Finalization | `Voting is still active` |
| Late Voting | `Voting has ended` |

---

## 📸 Screenshots & Demonstration Evidence

The `screenshots/` directory contains the project's deployment and testing evidence.

The screenshots demonstrate:

- ✅ Successful smart contract compilation.
- ⛓️ DAO smart contract deployment.
- 👥 Member count verification.
- ⏱️ Voting duration configuration.
- 📋 Proposal information retrieval.
- 🗳️ Active and completed voting.
- 🚫 Duplicate voting prevention.
- 🔒 Unregistered voter rejection.
- ⚖️ Proposal finalization and quorum behaviour.

---

## 🔒 Security & Privacy Considerations

The project separates AI computation from blockchain governance.

**Security Features**

- 🔐 SHA-256 manifest integrity checking.
- 👥 Registered-member voting restrictions.
- 🗳️ One-member-one-vote enforcement.
- ⚖️ Quorum and majority validation.
- 🚫 Duplicate proposal prevention.
- 🛡️ Emergency pause functionality.

**Potential Risks**

- Compromise of a registered member account.
- Collusion between members.
- Vote buying or external influence.
- Incorrect off-chain AI evaluation.
- Dependence on the administrator for membership management.

⚠️ The manifest digest provides integrity checking, not independent authentication of AI claims. The demonstration does not eliminate all governance or blockchain security risks.

---

## ⚠️ Project Limitations

- Synthetic AI evaluation dataset.
- Intentionally injected anomalies.
- Five local DAO members in the demonstration.
- AI computation performed off-chain.
- No complete protection against collusion or vote buying.
- Actual AI model deployment is outside the Solidity contract.
- Membership should remain fixed during an active demonstration ballot.

---

## 💻 Installation & Execution

### 📌 Prerequisites

- Python 3.x
- Git
- Remix IDE

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Princy33/DAO-Governance-AI-Model-Release.git
```

### 2️⃣ Navigate to Project

```bash
cd DAO-Governance-AI-Model-Release
```

### 3️⃣ Create Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Generate Synthetic Dataset

```bash
python ai/generate_data.py
```

### 6️⃣ Run Anomaly Detection

```bash
python ai/anomaly_detection.py
```

### 7️⃣ Generate Model Manifests

```bash
python ai/create_manifests.py
```

### 8️⃣ Launch Application

```bash
streamlit run app.py
```

### 9️⃣ Deploy Smart Contract

1. Open Remix IDE.
2. Load `contracts/DAOGovernance.sol`.
3. Select Solidity compiler version `0.8.24` or compatible.
4. Compile the contract.
5. Select Remix VM (Cancun).
6. Deploy the contract.
7. Register DAO members.
8. Create proposals and test voting.
9. Finalize, queue, and execute successful proposals.

📌 Run the Python scripts in the listed order when regenerating outputs. Deploy and test the smart contract separately in Remix IDE.

---

## 🔮 Future Enhancements

- 🌐 Integration with real-world AI evaluation datasets.
- 🤖 Advanced anomaly detection algorithms.
- 🔐 Decentralized identity and membership verification.
- 📦 IPFS-based decentralized manifest storage.
- ⚙️ Automated manifest verification.
- 👥 Role-based governance.
- ⛓️ Public blockchain testnet deployment.
- 🛡️ Automated smart contract security testing.
- 📊 Advanced AI governance analytics dashboard.

---

## 🏆 Conclusion

DAO Governance for AI Model Release demonstrates how decentralized governance can be applied to AI model release approval.

By combining off-chain AI anomaly detection, model manifest generation, SHA-256 integrity checking, and on-chain DAO voting, the project provides a practical demonstration of transparent and auditable governance.

The implementation covers registered-member voting, quorum enforcement, majority-based approval, duplicate-vote prevention, invalid-voter rejection, proposal finalization, queuing, and execution.

The project provides a foundation for exploring the integration of **Artificial Intelligence, Blockchain Technology, and Decentralized Decision-Making**.

---

## 👨‍💻 Author

**Princy Mishra**

🔗 **GitHub:** [@Princy33](https://github.com/Princy33)

📂 **Project Repository:** [DAO Governance for AI Model Release](https://github.com/Princy33/DAO-Governance-AI-Model-Release)

---

<p align="center">
  <h3 align="center">🚀 AI + 🔗 Blockchain + 🗳️ Decentralized Governance</h3>
  <p align="center">Building transparent and accountable AI release workflows.</p>
</p>
