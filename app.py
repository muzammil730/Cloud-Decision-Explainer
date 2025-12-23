import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from config import SERVICE_SCORES, get_initial_weights
from decision import (
    normalize_weights,
    apply_cost_preference,
    apply_ops_control_preference,
    apply_latency_scalability_preference,
    evaluate_services,
    get_best_service,
    get_decision_confidence,
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AWS Compute Decision Explainer",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("AWS Compute Decision Explainer")
st.caption("Explainable trade-offs between EC2, ECS, and Lambda")
st.divider()

# ---------------- RADAR CHART ----------------
def render_radar(service_a, service_b):
    labels = list(SERVICE_SCORES[service_a].keys())
    values_a = list(SERVICE_SCORES[service_a].values())
    values_b = list(SERVICE_SCORES[service_b].values())

    values_a += values_a[:1]
    values_b += values_b[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # 🔽 SMALLER & CLEAN SIZE
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

    ax.plot(angles, values_a, label=service_a, linewidth=2)
    ax.fill(angles, values_a, alpha=0.15)

    ax.plot(angles, values_b, label=service_b, linewidth=2)
    ax.fill(angles, values_b, alpha=0.15)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=9)
    ax.set_title("Capability Comparison", fontsize=12, pad=10)
    ax.legend(loc="upper right", fontsize=9)

    st.pyplot(fig, use_container_width=False)


# ---------------- LAYOUT ----------------
left, right = st.columns([1, 2])

# ---------------- INPUTS ----------------
with left:
    st.subheader("Your Requirements")

    traffic = st.radio(
        "Traffic Pattern",
        ["Bursty / Unpredictable", "Steady High Traffic"]
    )

    cost = st.radio(
        "Cost Sensitivity",
        ["Low", "Medium", "High"]
    )

    ops_control = st.radio(
        "Operations vs Control",
        ["Minimal Ops", "Balanced", "Full Control"]
    )

    priority = st.radio(
        "Primary Priority",
        ["Ultra-low latency", "Balanced", "Massive scalability"]
    )

    run = st.button("Evaluate Decision")

# ---------------- OUTPUT ----------------
with right:
    st.subheader("Decision Output")

    if not run:
        st.info("Select requirements and click **Evaluate Decision**")
    else:
        # ---- MAP INPUTS ----
        scenario = "steady_high_traffic" if traffic == "Steady High Traffic" else "bursty_low_cost"

        cost_choice = {"High": "1", "Medium": "2", "Low": "3"}[cost]
        ops_choice = {"Minimal Ops": "1", "Balanced": "2", "Full Control": "3"}[ops_control]
        latency_choice = {
            "Ultra-low latency": "1",
            "Balanced": "2",
            "Massive scalability": "3"
        }[priority]

        # ---- WEIGHTS ----
        weights = get_initial_weights(scenario)
        weights = apply_cost_preference(weights, cost_choice)
        weights = apply_ops_control_preference(weights, ops_choice)
        weights = apply_latency_scalability_preference(weights, latency_choice)
        weights = normalize_weights(weights)

        # ---- SCORES ----
        scores = evaluate_services(weights)
        best = get_best_service(scores)
        confidence = get_decision_confidence(scores)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # ---------------- TABS ----------------
        tab1, tab2 = st.tabs(
            ["✅ Decision & Reasoning", "📊 Comparison"]
        )

        # ================= TAB 1 =================
        with tab1:
            st.markdown(
                f"""
                <div style="
                    padding:18px;
                    border-radius:10px;
                    background:#020617;
                    border:1px solid #334155;
                ">
                    <h3>Recommended Service</h3>
                    <h1 style="color:#38bdf8;">{best}</h1>
                    <p><b>Confidence:</b> {confidence}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # WHY
            top_factors = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:2]
            f1, f2 = top_factors[0][0], top_factors[1][0]

            st.markdown("### Why this service?")
            st.write(
                f"{best} fits best because **{f1}** and **{f2}** "
                "were the strongest decision drivers based on your inputs."
            )

            # TRADE-OFFS
            st.markdown("### Alternatives & Trade-offs")
            st.write(f"⚠️ Alternative: **{ranked[1][0]}**")
            st.write(f"❌ Rejected: **{ranked[2][0]}**")

            # SCORES
            st.markdown("### Scores")
            for svc, score in ranked:
                mark = " ← recommended" if svc == best else ""
                st.write(f"{svc}: {score}{mark}")

            # COST
            st.markdown("### Cost Perspective (relative)")
            st.write("• Lambda → Low for bursty traffic, unpredictable at scale")
            st.write("• ECS → Medium, balanced ops & control")
            st.write("• EC2 → Higher baseline, predictable monthly spend")

            # LIMITATION
            st.markdown("### Limitations")
            st.warning(
                "This tool uses a rule-based scoring model. "
                "It does not consider real-time AWS pricing, "
                "region availability, or workload-specific tuning."
            )

        # ================= TAB 2 =================
        with tab2:
            st.markdown("### Service Comparison (Visual)")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                render_radar(ranked[0][0], ranked[1][0])
 
