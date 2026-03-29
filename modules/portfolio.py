def allocate(risk, future_prices):
    scores = {}

    # -------------------------
    # Step 1: Risk-adjusted scoring
    # -------------------------
    for coin in risk:
        risk_value = risk[coin]["value"]
        predicted = future_prices[coin]

        # Risk-adjusted return
        score = predicted / (risk_value + 1e-5)

        scores[coin] = score

    # -------------------------
    # Step 2: Normalize
    # -------------------------
    total_score = sum(scores.values())

    allocation = {
        coin: (scores[coin] / total_score) * 100
        for coin in scores
    }

    # -------------------------
    # Step 3: Apply REAL portfolio rules
    # -------------------------
    for coin in allocation:
        if risk[coin]["level"] == "LOW":
            # safe coins (core)
            allocation[coin] = min(allocation[coin], 50)

        elif risk[coin]["level"] == "MEDIUM":
            # growth coins
            allocation[coin] = min(allocation[coin], 35)

        else:
            # high risk coins
            allocation[coin] = min(allocation[coin], 15)

    # -------------------------
    # Step 4: Ensure minimum diversification
    # -------------------------
    for coin in allocation:
        if allocation[coin] < 10:
            allocation[coin] = 10

    # -------------------------
    # Step 5: Normalize again (IMPORTANT)
    # -------------------------
    total = sum(allocation.values())

    for coin in allocation:
        allocation[coin] = round((allocation[coin] / total) * 100, 2)

    return allocation