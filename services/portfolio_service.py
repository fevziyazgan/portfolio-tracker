def calculate_total_value(
    portfolio
):
    total = 0
    for asset in portfolio.values():
        if (
            isinstance(asset, dict)
            and "current_value"
            in asset
        ):
            total += (
                asset["current_value"]
            )
    return total
