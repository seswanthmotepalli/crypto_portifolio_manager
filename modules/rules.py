def apply_rules(allocation):
    for coin in allocation:
        if allocation[coin] > 50:
            allocation[coin] = 50
        elif allocation[coin] < 5:
            allocation[coin] = 5

    return allocation