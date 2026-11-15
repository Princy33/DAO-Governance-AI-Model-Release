# DAO Governance for AI Model Release

## Project Overview

This project implements a decentralized governance system for approving AI model releases using blockchain-based voting.

The system combines an off-chain AI anomaly detection component with an on-chain DAO governance smart contract. The AI computation is performed off-chain, while the blockchain stores the model version, SHA-256 manifest digest, proposal information, voting results, and governance outcome.

The project demonstrates how a DAO can be used to control the approval of AI model releases through transparent and auditable voting.

---

## Problem Statement

AI model releases require a controlled approval process to ensure that a model satisfies predefined quality, risk, and governance requirements.

A centralized approval process may make it difficult to provide transparent voting records and verifiable governance decisions.

This project addresses the problem by creating a DAO-based governance mechanism where registered members can vote on AI model release proposals.

---

## Objectives

The main objectives of the project are:

1. Develop an AI-based anomaly detection component.
2. Generate a reproducible synthetic evaluation dataset.
3. Detect anomalous records using Isolation Forest.
4. Generate AI model manifests containing governance metadata.
5. Generate SHA-256 digests for model manifests.
6. Store the model version and manifest digest on the blockchain.
7. Implement registered-member voting.
8. Enforce one-member-one-vote.
9. Enforce a minimum quorum.
10. Handle successful, failed, duplicate, and invalid voting scenarios.
11. Provide a transparent proposal lifecycle.
12. Maintain historical governance outcomes on-chain.

---

## Technologies Used

### AI / Machine Learning

- Python
- NumPy
- Pandas
- Scikit-learn
- Isolation Forest
- StandardScaler

### Blockchain

- Solidity
- Remix IDE
- Remix VM (Cancun)
- Ethereum-compatible local execution environment
- SHA-256 manifest digest

### Development

- Visual Studio Code
- Python Virtual Environment

---

## Project Structure

```text
DAO_Governance_AI_Model_Release/
│
├── ai/
│   ├── data/
│   │   ├── anomaly_detection_results.csv
│   │   └── model_evaluation_data.csv
│   ├── anomaly_detection.py
│   ├── create_manifests.py
│   └── generate_data.py
│
├── contracts/
│   └── DAOGovernance.sol
│
├── manifests/
│   ├── hashes.txt
│   ├── manifest_v2.json
│   └── manifest_v3.json
│
├── screenshots/
│   └── Remix testing screenshots
│
├── venv/
│
├── README.md
└── requirements.txt

---

# System Architecture

The project consists of two main components:

### 1. Off-Chain AI Component

The AI component performs anomaly detection and model evaluation outside the blockchain.

```text
Synthetic Data
      ↓
Preprocessing
      ↓
StandardScaler
      ↓
Isolation Forest
      ↓
Anomaly Detection
      ↓
Evaluation Results
      ↓
Model Manifest
      ↓
SHA-256 Digest

### 2. On-Chain DAO Governance

Model Version + Manifest Digest
              ↓
        Create Proposal
              ↓
          Member Voting
              ↓
        Quorum Check
              ↓
       Majority Check
              ↓
     Succeeded / Defeated
              ↓
            Queue
              ↓
           Execute



AI Component

The project uses a synthetic dataset for demonstrating AI-based anomaly detection.

A total of 200 records were generated, including 5 intentionally injected anomalies.

The preprocessing stage uses StandardScaler to standardize numerical features.

The anomaly detection algorithm used is Isolation Forest with:

Number of estimators: 200
Contamination: 2.5%
Random state: 42

The experiment detected all 5 injected anomalies.

Evaluation Results
Metric	Result
Accuracy	1.0000
Precision	1.0000
Recall	1.0000
F1 Score	1.0000
Injected anomalies	5
Detected anomalies	5
AI Limitation

The dataset is synthetic and the anomalies were intentionally injected. Therefore, the perfect evaluation results demonstrate the behaviour of the experimental pipeline and should not be interpreted as evidence of perfect real-world anomaly detection.

Model Manifest and SHA-256

The project contains two model manifests:

manifest_v2.json
manifest_v3.json

The corresponding SHA-256 digests are stored in:

manifests/hashes.txt
Manifest v2
98b687886a77f68e3dca2770839344087b7d4847cbfb31176517cf61d53c11bd
Manifest v3
bb8f51225c948c837c5e9bc1087cbc131b121a177b2af3c1889849c990cbccbf

The digest is used as a cryptographic commitment to the manifest contents. It does not independently prove that the underlying off-chain AI information is correct or truthful.

DAO Governance Rules

The DAO uses the following governance rules:

Only registered members can vote.
Each registered member can vote once per proposal.
Quorum is 3 votes.
A proposal succeeds only when YES votes are greater than NO votes.
A tie results in a defeated proposal.
Voting must close before finalization.
A successful proposal must be queued before execution.
Duplicate proposals using the same model version and manifest digest are rejected.
The administrator can register and remove members.
The administrator can cancel proposals.
An emergency pause mechanism is provided.
Proposal Lifecycle

The smart contract uses the following proposal states:

Pending
Active
Succeeded
Defeated
Queued
Executed
Cancelled

The normal successful lifecycle is:

Active
   ↓
Succeeded
   ↓
Queued
   ↓
Executed

If quorum is not reached or YES votes do not exceed NO votes:

Active
   ↓
Defeated
Smart Contract

The Solidity smart contract is located at:

contracts/DAOGovernance.sol

The contract is written using Solidity ^0.8.24.

Important functions include:

Member Management
registerMember()
removeMember()
Proposal Management
createProposal()
finalizeProposal()
queueProposal()
executeProposal()
cancelProposal()
Voting
vote()
Emergency Control
setEmergencyPause()
Information Functions
getProposal()
getProposalCount()
getTotalVotes()
quorumReached()
Blockchain Deployment

The smart contract was compiled and deployed using Remix IDE.

The project uses:

Remix VM (Cancun)

The demonstration does not use real Ether.

The deployment and testing evidence is available in the screenshots folder.

Testing

The project includes successful and negative test cases.

Successful Proposal

Proposal 1 was created using model version 2.0 and the v2 manifest digest.

The recorded voting result was:

YES = 4
NO  = 1
Total Votes = 5

The quorum requirement was 3 votes.

The proposal therefore reached quorum and satisfied the YES > NO rule.

Its lifecycle was:

Succeeded → Queued → Executed
Quorum Failure

Proposal 3 recorded:

YES = 2
NO  = 0
Total Votes = 2

Since the total number of votes was below the quorum requirement of 3, the proposal was defeated.

Negative Test Cases

The following invalid operations were tested:

Duplicate Vote

A member attempted to vote twice on the same proposal.

The transaction was rejected with:

Member has already voted
Unregistered Voter

An account that was not registered as a DAO member attempted to vote.

The transaction was rejected with:

Only registered members can vote
Early Finalization

An attempt was made to finalize a proposal while voting was active.

The transaction was rejected with:

Voting is still active
Late Voting

An attempt was made to vote after the voting period ended.

The transaction was rejected with:

Voting has ended
Already Finalized Proposal

An already finalized proposal cannot be finalized again.

Security and Privacy

The project does not store passwords, private keys, or sensitive personal records in the source code.

The AI computation is performed off-chain.

The blockchain stores governance information such as the model version, manifest digest, proposal state, and voting results.

Potential risks include:

Compromise of a registered member account.
Collusion between members.
Vote buying.
Incorrect or misleading off-chain AI evaluation.
Dependence on the administrator for member registration.

The manifest digest provides integrity checking for the referenced manifest but does not independently authenticate the underlying AI claims.

Limitations
The AI dataset is synthetic.
The anomaly detection experiment uses intentionally injected anomalies.
The DAO is demonstrated with five local members.
AI computation is performed off-chain.
The smart contract does not completely prevent collusion or vote buying.
Actual AI model deployment is outside the Solidity contract.
Membership should remain fixed during an active demonstration ballot.
Conclusion

This project demonstrates a DAO-based governance mechanism for AI model release decisions.

It combines an off-chain AI anomaly detection pipeline with an on-chain Solidity governance contract.

The system demonstrates model-manifest hashing, registered-member voting, quorum enforcement, majority-based proposal approval, duplicate-vote prevention, invalid-voter rejection, proposal finalization, queuing, and execution.

The project provides a local and reproducible demonstration of blockchain-based governance for AI model release decisions.


