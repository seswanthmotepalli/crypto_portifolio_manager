def rank_coins(risk, future_prices):
    scores = {}

    for coin in risk:
        risk_val = risk[coin]["value"]
        predicted = future_prices[coin]

        # Score logic (low risk + high price = better)
        score = (predicted / (risk_val + 1e-5))

        scores[coin] = score

    # Sort descending
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return ranked


def recommend_action(risk, future_prices):
    recommendations = {}

    for coin in risk:
        risk_level = risk[coin]["level"]
        predicted = future_prices[coin]

        if risk_level == "LOW":
            action = "BUY"
        elif risk_level == "MEDIUM":
            action = "HOLD"
        else:
            action = "AVOID"

        recommendations[coin] = action

    return recommendations