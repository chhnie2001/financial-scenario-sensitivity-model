def project_financials(last_revenue, growth_rate, gross_margin):
    revenue = last_revenue * (1 + growth_rate)
    gross_profit = revenue * gross_margin
    cost = revenue - gross_profit

    return {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "cost": cost,
        "gross_margin": gross_margin
    }


def calculate_break_even_revenue(fixed_cost_pool, gross_margin):
    if gross_margin <= 0:
        return None
    return fixed_cost_pool / gross_margin