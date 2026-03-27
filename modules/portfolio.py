def allocate(risk, trend):
    scores = {}

    for coin in risk:
        risk_value = risk[coin]["value"]

        scores[coin] = (1 / (risk_value + 1e-5)) + trend.get(coin, 0)

    total = sum(scores.values())

    allocation = {c: round((scores[c] / total) * 100, 2) for c in scores}
    return allocation