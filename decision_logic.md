# Decision Logic – AWS Compute Decision Explainer

## Problem Statement
Choosing between EC2, ECS, and Lambda is not straightforward.
Each service fits different workloads depending on traffic pattern,
cost sensitivity, operational effort, and control requirements.

This tool explains **why** a service is recommended, not just **what**.

---

## Inputs Considered
- Traffic Pattern (Bursty / Steady)
- Cost Sensitivity
- Operations vs Control
- Primary Priority (Latency / Balanced / Scalability)

---

## Scoring Model
Each service is scored across the following factors:
- traffic
- cost
- scalability
- ops
- control
- latency

Scores are predefined based on AWS service characteristics.

---

## Weight Adjustment
User inputs increase or decrease factor weights.
After adjustments, weights are normalized so the total equals 1.

This ensures fair comparison across services.

---

## Decision Rule
Final score = sum of (factor score × weight)

The service with the highest final score is recommended.

---

## Decision Confidence
Confidence is based on the score gap:
- Gap < 0.5 → Low (Close trade-off)
- Gap 0.5–1.5 → Medium
- Gap > 1.5 → High

---

## Trade-offs
The tool also highlights:
- Alternative service
- Rejected service
- Key factors that influenced the decision

---

## Limitations
- Static scoring model
- No real-time AWS pricing
- No region-specific or workload-specific tuning

This tool is intended for **decision guidance**, not exact cost estimation.
