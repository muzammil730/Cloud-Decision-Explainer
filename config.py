SCENARIOS = {
    "bursty_low_cost": {
        "description": "Bursty traffic, cost sensitive, beginner team"
    },
    "steady_high_traffic": {
        "description": "Steady high traffic, performance focused"
    }
}


def get_initial_weights(scenario):
    if scenario == "bursty_low_cost":
        return {
            "traffic": 0.30,
            "cost": 0.25,
            "scalability": 0.20,
            "ops": 0.15,
            "control": 0.05,
            "latency": 0.05
        }

    if scenario == "steady_high_traffic":
        return {
            "traffic": 0.20,
            "cost": 0.15,
            "scalability": 0.25,
            "ops": 0.10,
            "control": 0.20,
            "latency": 0.10
        }


# Service scores for each factor (1–10 scale)
SERVICE_SCORES = {
    "Lambda": {
        "traffic": 9,
        "cost": 8,
        "scalability": 9,
        "ops": 9,
        "control": 4,
        "latency": 6
    },
    "ECS": {
        "traffic": 7,
        "cost": 6,
        "scalability": 8,
        "ops": 6,
        "control": 7,
        "latency": 8
    },
    "EC2": {
        "traffic": 6,
        "cost": 4,
        "scalability": 6,
        "ops": 3,
        "control": 9,
        "latency": 9
    }
}
