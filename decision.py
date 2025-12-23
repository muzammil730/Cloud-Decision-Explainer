from config import SERVICE_SCORES, get_initial_weights


# ---------- WEIGHT HELPERS ----------

def normalize_weights(weights):
    # Clamp negative values
    for k in weights:
        if weights[k] < 0:
            weights[k] = 0

    total = sum(weights.values())

    # Safety check
    if total == 0:
        return weights

    for k in weights:
        weights[k] = round(weights[k] / total, 3)

    return weights


def apply_cost_preference(weights, cost_choice):
    if cost_choice == "1":  # Very important
        weights["cost"] += 0.10
        weights["control"] -= 0.05
        weights["latency"] -= 0.05

    elif cost_choice == "2":  # Moderate
        weights["cost"] += 0.05
        weights["control"] -= 0.02

    elif cost_choice == "3":  # Not important
        weights["cost"] -= 0.10
        weights["control"] += 0.05
        weights["latency"] += 0.05

    return weights


def apply_ops_control_preference(weights, choice):
    if choice == "1":  # minimal ops
        weights["ops"] += 0.20
        weights["control"] -= 0.15

    elif choice == "2":  # balanced
        weights["ops"] += 0.05
        weights["control"] += 0.05

    elif choice == "3":  # full control
        weights["control"] += 0.25
        weights["ops"] -= 0.20

    return weights


def apply_latency_scalability_preference(weights, choice):
    if choice == "1":  # latency critical
        weights["latency"] += 0.25
        weights["scalability"] -= 0.20

    elif choice == "2":  # balanced
        weights["latency"] += 0.05
        weights["scalability"] += 0.05

    elif choice == "3":  # scalability critical
        weights["scalability"] += 0.25
        weights["latency"] -= 0.20

    return weights


# ---------- SCORING ----------

def calculate_score(service_name, weights):
    return round(
        sum(SERVICE_SCORES[service_name][factor] * weight
            for factor, weight in weights.items()),
        2
    )


def evaluate_services(weights):
    return {
        service: calculate_score(service, weights)
        for service in SERVICE_SCORES
    }


def get_best_service(scores):
    return max(scores, key=scores.get)


def get_decision_confidence(scores):
    values = sorted(scores.values(), reverse=True)

    if len(values) < 2:
        return "High"

    gap = round(values[0] - values[1], 2)

    if gap < 0.5:
        return "Low (Close trade-off)"
    elif gap < 1.5:
        return "Medium"
    else:
        return "High"


# ---------- EXPLANATION ENGINE ----------

def generate_explanations(best_service, scores, weights):
    # Top 2 decision drivers
    top_factors = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:2]
    top_factor_names = [f[0] for f in top_factors]

    explanations = {}

    explanations["why_best"] = (
        f"{best_service} aligns best with your priorities because "
        f"{top_factor_names[0]} and {top_factor_names[1]} "
        f"had the strongest influence on the decision."
    )

    why_not = {}
    for service in scores:
        if service != best_service:
            weakest_factor = min(
                SERVICE_SCORES[service],
                key=lambda f: SERVICE_SCORES[service][f]
            )
            why_not[service] = (
                f"Weaker performance in {weakest_factor} compared to {best_service}."
            )

    explanations["why_not"] = why_not
    return explanations


def get_recommendation_bundle(scores):
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "recommended": ranked[0][0],
        "alternative": ranked[1][0],
        "rejected": ranked[2][0]
    }


# ---------- CLI DRIVER (OPTIONAL) ----------

if __name__ == "__main__":

    print("Select traffic pattern:")
    print("1. Bursty / Unpredictable")
    print("2. Steady High Traffic")

    choice = input("Enter choice (1 or 2): ")
    scenario = "steady_high_traffic" if choice == "2" else "bursty_low_cost"

    print("\nHow important is cost control?")
    print("1. Very important")
    print("2. Moderate")
    print("3. Not important")
    cost_choice = input("Enter choice (1/2/3): ")

    print("\nCan you manage servers yourself?")
    print("1. No, minimal ops")
    print("2. Some ops ok")
    print("3. Yes, full control needed")
    ops_choice = input("Enter choice (1/2/3): ")

    print("\nWhat matters more?")
    print("1. Ultra-low latency")
    print("2. Balanced")
    print("3. Massive scalability")
    latency_choice = input("Enter choice (1/2/3): ")

    weights = get_initial_weights(scenario)
    weights = apply_cost_preference(weights, cost_choice)
    weights = apply_ops_control_preference(weights, ops_choice)
    weights = apply_latency_scalability_preference(weights, latency_choice)
    weights = normalize_weights(weights)

    scores = evaluate_services(weights)
    best_service = get_best_service(scores)
    confidence = get_decision_confidence(scores)
    explanations = generate_explanations(best_service, scores, weights)

    print("\n================ DECISION RESULT ================")
    print("Scenario:", scenario)
    print("Recommended Service:", best_service)
    print("Decision Confidence:", confidence)
    print("Scores:", scores)

    print("\nWhy this service?")
    print(explanations["why_best"])

    print("\nWhy not the others?")
    for svc, reason in explanations["why_not"].items():
        print(f"- {svc}: {reason}")
