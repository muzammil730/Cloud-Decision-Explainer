# AWS Compute Decision Explainer

An explainable decision-support tool that helps users choose between
AWS EC2, ECS, and Lambda based on workload requirements.

## Why this project?
Most tools tell you *what* service to use.
This tool explains *why* a service fits your use case.

---

## Features
- Rule-based decision engine
- Transparent scoring & weighting
- Decision confidence indicator
- Trade-offs and alternatives
- Radar chart comparison

---

## How it works
1. User selects workload requirements
2. Weights are adjusted based on priorities
3. Services are scored using weighted factors
4. Best service + explanation is shown

---

## Tech Stack
- Python
- Streamlit
- Matplotlib

---

## Screenshots
(Add 1–2 screenshots only)

---

## Limitations
- No real-time AWS pricing
- Static capability scores
- Not region-aware

---

## Future Improvements
- Dynamic pricing integration
- More AWS services
- Preset industry scenarios
