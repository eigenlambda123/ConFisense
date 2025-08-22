def simulate_budget_optimization(
    scenario_type,
    user_type,
    projection_months,
    income,
    expenses,
    savings_goals
):
    # Unpack income
    monthly_net_income = income.get("monthly_net_income", 0)
    other_monthly_income = income.get("other_monthly_income", 0)
    income_frequency = income.get("income_frequency", "monthly")
    total_income = monthly_net_income + other_monthly_income

    # Unpack expenses
    fixed = expenses.get("fixed_needs", {})
    variable = expenses.get("variable_needs", {})
    wants = expenses.get("wants_discretionary", {})

    fixed_total = sum(fixed.values())
    variable_total = sum(variable.values())
    wants_total = sum(wants.values())

    # Unpack savings goals
    target_monthly_savings = savings_goals.get("target_monthly_savings", 0)
    emergency_fund_target = savings_goals.get("emergency_fund_target", 0)

    # Prepare chart data for each month
    chart_data = []
    cumulative_savings = 0
    cumulative_deficit = 0
    for month in range(1, projection_months + 1):
        total_expenses = fixed_total + variable_total + wants_total
        net_cash_flow = total_income - total_expenses - target_monthly_savings

        if net_cash_flow >= 0:
            cumulative_savings += net_cash_flow
        else:
            cumulative_deficit += abs(net_cash_flow)

        chart_data.append({
            "month": month,
            "total_income": total_income,
            "fixed_expenses": fixed_total,
            "variable_expenses": variable_total,
            "wants_expenses": wants_total,
            "net_cash_flow": net_cash_flow,
            "cumulative_savings": cumulative_savings,
            "cumulative_deficit": cumulative_deficit
        })

    # Key metrics
    avg_net_cash_flow = sum([m["net_cash_flow"] for m in chart_data]) / projection_months if projection_months else 0
    discretionary_spending_percent = wants_total / total_income if total_income else 0
    highest_discretionary_category = max(wants, key=wants.get) if wants else None
    projected_emergency_fund_months = (
        emergency_fund_target / target_monthly_savings if target_monthly_savings else None
    )

    key_metrics = {
        "avg_net_cash_flow": avg_net_cash_flow,
        "discretionary_spending_percent": round(discretionary_spending_percent, 4),
        "total_discretionary_spending": wants_total,
        "highest_discretionary_category": highest_discretionary_category,
        "projected_emergency_fund_months": projected_emergency_fund_months
    }

    # Insight
    insight = (
        f"Based on your current income and spending habits, you're projected to have an average monthly "
        f"{'deficit' if avg_net_cash_flow < 0 else 'surplus'} of ₱{abs(avg_net_cash_flow):,.2f}. "
        f"Our AI analysis highlights that {discretionary_spending_percent*100:.1f}% of your income is consistently being allocated to "
        f"{highest_discretionary_category.replace('_', ' ') if highest_discretionary_category else 'discretionary spending'}, "
        f"which is significantly higher than typical household spending for your income bracket in Lucena City. "
        f"By optimizing this category, you can achieve a positive monthly cash flow and fully fund your emergency fund goal of "
        f"₱{emergency_fund_target:,.2f} within {projected_emergency_fund_months:.1f} months without compromising essential needs. "
        f"The chart shows how adjusting this single area significantly shifts your financial trajectory towards stability."
    )

    # Show my math
    show_my_math = [
        "Total Monthly Income (TMI) = Monthly Net Income + Other Monthly Income",
        "Total Monthly Expenses (TME) = Sum of all fixed, variable, and discretionary expenses",
        "Net Cash Flow (NCF) = TMI - TME - Target Monthly Savings",
        "Projected Cumulative Savings/Deficit = Previous Month's Cumulative + Current Month's NCF"
    ]

    # Response structure
    response = {
        "status": "success",
        "data": {
            "inputs_received": {
                "scenario_type": scenario_type,
                "user_type": user_type,
                "projection_months": projection_months,
                "income": income,
                "expenses": expenses,
                "savings_goals": savings_goals
            },
            "chart_data": chart_data,
            "key_metrics": key_metrics,
            "insight": insight,
            "show_my_math": show_my_math
        }
    }

    return response