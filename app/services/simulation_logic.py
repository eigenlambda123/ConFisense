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
