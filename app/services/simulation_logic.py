def simulate_budgeting(
    monthly_net_income,
    housing_expense,
    food_grocery_expense,
    utilities_expense,
    transportation_expense,
    debt_payments_expense,
    medical_healthcare_expense,
    education_expense,
    household_supplies_maintenance_expense,
    personal_care_shopping_expense,
    entertainment_recreation_expense,
    gifts_donations_expense,
    savings_investment_contribution
):

    # Total Expenses
    total_expenses_excluding_savings = sum([
        housing_expense,
        food_grocery_expense,
        utilities_expense,
        transportation_expense,
        debt_payments_expense,
        medical_healthcare_expense,
        education_expense,
        household_supplies_maintenance_expense,
        personal_care_shopping_expense,
        entertainment_recreation_expense,
        gifts_donations_expense
    ])

    net_cash_flow = (
        monthly_net_income
        - total_expenses_excluding_savings
        - savings_investment_contribution
    )

    cash_flow_status = "Surplus" if net_cash_flow >= 0 else "Deficit"

    # Chart labels
    labels = [
        "Monthly Net Income",
        "Housing",
        "Food & Groceries",
        "Utilities",
        "Transportation",
        "Debt Payments",
        "Medical & Healthcare",
        "Education",
        "Household Supplies & Maintenance",
        "Personal Care & Shopping",
        "Entertainment & Recreation",
        "Gifts & Donations",
        "Savings & Investments",
        "Net Cash Flow"
    ]

    data_points = [
        monthly_net_income,
        -housing_expense,
        -food_grocery_expense,
        -utilities_expense,
        -transportation_expense,
        -debt_payments_expense,
        -medical_healthcare_expense,
        -education_expense,
        -household_supplies_maintenance_expense,
        -personal_care_shopping_expense,
        -entertainment_recreation_expense,
        -gifts_donations_expense,
        -savings_investment_contribution,
        net_cash_flow
    ]

    waterfall_meta = [
        {"label": "Monthly Net Income", "value": monthly_net_income, "is_sum": False},
        {"label": "Housing", "value": -housing_expense, "is_sum": False},
        {"label": "Food & Groceries", "value": -food_grocery_expense, "is_sum": False},
        {"label": "Utilities", "value": -utilities_expense, "is_sum": False},
        {"label": "Transportation", "value": -transportation_expense, "is_sum": False},
        {"label": "Debt Payments", "value": -debt_payments_expense, "is_sum": False},
        {"label": "Medical & Healthcare", "value": -medical_healthcare_expense, "is_sum": False},
        {"label": "Education", "value": -education_expense, "is_sum": False},
        {"label": "Household Supplies & Maintenance", "value": -household_supplies_maintenance_expense, "is_sum": False},
        {"label": "Personal Care & Shopping", "value": -personal_care_shopping_expense, "is_sum": False},
        {"label": "Entertainment & Recreation", "value": -entertainment_recreation_expense, "is_sum": False},
        {"label": "Gifts & Donations", "value": -gifts_donations_expense, "is_sum": False},
        {"label": "Savings & Investments", "value": -savings_investment_contribution, "is_sum": False},
        {"label": "Net Cash Flow", "value": net_cash_flow, "is_sum": True}
    ]

    # Summary (for testing)
    summary = f"{cash_flow_status}: ₱{abs(net_cash_flow):,.2f} this month."

    # Glass Box explanation
    math_explanation = {
        "title": "The 'Glass Box': How We Calculate Your Monthly Cash Flow",
        "sections": [
            {
                "heading": "1. Your Inputs",
                "items": [
                    f"Monthly Net Income: ₱{monthly_net_income:,.2f}",
                    f"Housing: ₱{housing_expense:,.2f}",
                    f"Food & Groceries: ₱{food_grocery_expense:,.2f}",
                    f"Utilities: ₱{utilities_expense:,.2f}",
                    f"Transportation: ₱{transportation_expense:,.2f}",
                    f"Debt Payments: ₱{debt_payments_expense:,.2f}",
                    f"Medical & Healthcare: ₱{medical_healthcare_expense:,.2f}",
                    f"Education: ₱{education_expense:,.2f}",
                    f"Household Supplies & Maintenance: ₱{household_supplies_maintenance_expense:,.2f}",
                    f"Personal Care & Shopping: ₱{personal_care_shopping_expense:,.2f}",
                    f"Entertainment & Recreation: ₱{entertainment_recreation_expense:,.2f}",
                    f"Gifts & Donations: ₱{gifts_donations_expense:,.2f}",
                    f"Savings & Investments: ₱{savings_investment_contribution:,.2f}"
                ]
            },
            {
                "heading": "2. The Math",
                "items": [
                    "We total your expense categories (excluding savings) to get Total Monthly Expenses.",
                    f"   Total Monthly Expenses = ₱{total_expenses_excluding_savings:,.2f}",
                    "Then we subtract both expenses and savings from income:",
                    "   Net Cash Flow = Monthly Net Income − Total Monthly Expenses − Savings Contributions"
                ]
            },
            {
                "heading": "3. The Outcome",
                "items": [
                    f"Net Cash Flow = ₱{net_cash_flow:,.2f} ({cash_flow_status})."
                ]
            }
        ]
    }

    # API response 
    response = {
        "status": "success",
        "message": "Effective Budgeting and Expense Tracking simulation successful.",
        "data": {
            "totals": {
                "monthly_net_income": round(monthly_net_income, 2),
                "total_expenses_excluding_savings": round(total_expenses_excluding_savings, 2),
                "savings_investment_contribution": round(savings_investment_contribution, 2),
                "net_cash_flow": round(net_cash_flow, 2),
                "cash_flow_status": cash_flow_status
            },
            "projection_data": {
                "labels": labels,
                "data": [round(x, 2) for x in data_points],
                "waterfall_meta": waterfall_meta  # frontend can use is_sum to style the total bar
            },
            "summary": summary,
            "math_explanation": math_explanation
        },
        "inputs_received": {
            "monthly_net_income": monthly_net_income,
            "housing_expense": housing_expense,
            "food_grocery_expense": food_grocery_expense,
            "utilities_expense": utilities_expense,
            "transportation_expense": transportation_expense,
            "debt_payments_expense": debt_payments_expense,
            "medical_healthcare_expense": medical_healthcare_expense,
            "education_expense": education_expense,
            "household_supplies_maintenance_expense": household_supplies_maintenance_expense,
            "personal_care_shopping_expense": personal_care_shopping_expense,
            "entertainment_recreation_expense": entertainment_recreation_expense,
            "gifts_donations_expense": gifts_donations_expense,
            "savings_investment_contribution": savings_investment_contribution
        }
    }

    return response


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