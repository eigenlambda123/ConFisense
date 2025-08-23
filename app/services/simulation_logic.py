def simulate_budget_optimization(
    scenario_type,
    user_type,
    projection_months,
    income,
    expenses,
    savings_goals,
    what_if_factors=None
):
    # Unpack income
    monthly_gross_income = income.get("monthly_gross_income", 0)
    other_monthly_income = income.get("other_monthly_income", 0)
    total_income = monthly_gross_income + other_monthly_income

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

    # Apply default what-if factors if none are provided
    if what_if_factors is None:
        what_if_factors = {}
    
    # Unpack what-if factors with default values of 0
    income_growth_rate = what_if_factors.get("income_growth_rate", 0)
    wants_reduction_rate = what_if_factors.get("wants_reduction_rate", 0)
    savings_increase_rate = what_if_factors.get("savings_increase_rate", 0)

    # Initialize dynamic variables for the loop
    current_monthly_income = total_income
    current_wants_total = wants_total
    current_target_savings = target_monthly_savings

    # Prepare chart data for each month
    chart_data = []
    cumulative_savings = 0
    cumulative_deficit = 0
    for month in range(1, projection_months + 1):
        # Apply recurring what-if factors from the second month onwards
        if month > 1:
            current_monthly_income *= (1 + income_growth_rate)
            current_wants_total *= (1 - wants_reduction_rate)
            current_target_savings *= (1 + savings_increase_rate)

        total_expenses = fixed_total + variable_total + current_wants_total
        net_cash_flow = current_monthly_income - total_expenses - current_target_savings

        if net_cash_flow >= 0:
            cumulative_savings += net_cash_flow
        else:
            cumulative_deficit += abs(net_cash_flow)

        chart_data.append({
            "month": month,
            "total_income": current_monthly_income,
            "fixed_expenses": fixed_total,
            "variable_expenses": variable_total,
            "wants_expenses": current_wants_total,
            "net_cash_flow": net_cash_flow,
            "cumulative_savings": cumulative_savings,
            "cumulative_deficit": cumulative_deficit
        })

    # Key metrics
    avg_net_cash_flow = sum([m["net_cash_flow"] for m in chart_data]) / projection_months if projection_months else 0
    
    # Use the initial values for the first month for an accurate metric
    discretionary_spending_percent = wants_total / total_income if total_income else 0
    highest_discretionary_category = max(wants, key=wants.get) if wants else None
    projected_emergency_fund_months = (
        emergency_fund_target / current_target_savings if current_target_savings > 0 else float('inf')
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
        f"By applying your what-if scenarios, you're projected to have an average monthly "
        f"{'deficit' if avg_net_cash_flow < 0 else 'surplus'} of ₱{abs(avg_net_cash_flow):,.2f}. "
        f"Our analysis shows that if you maintain this new habit, your financial trajectory "
        f"significantly shifts, and you are on track to fully fund your emergency fund goal of "
        f"₱{emergency_fund_target:,.2f} within {projected_emergency_fund_months:.1f} months. "
        f"The chart shows how these adjustments change your financial future."
    )

    # Show my math
    show_my_math = [
        "Total Monthly Income (TMI) = Monthly Net Income + Other Monthly Income",
        "Total Monthly Expenses (TME) = Sum of all fixed, variable, and discretionary expenses",
        "Net Cash Flow (NCF) = TMI - TME - Target Monthly Savings",
        "Projected Cumulative Savings/Deficit = Previous Month's Cumulative + Current Month's NCF",
        "What-If Factors: Monthly Income, Savings, and Discretionary Spending are adjusted by your chosen percentages each month to simulate long-term changes."
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
                "savings_goals": savings_goals,
                "what_if_factors": what_if_factors
            },
            "chart_data": chart_data,
            "key_metrics": key_metrics,
            "insight": insight,
            "show_my_math": show_my_math
        }
    }

    return response



def simulate_debt_management(
    scenario_type,
    user_type,
    projection_period,
    loans,
    business_financials,
    growth_needs,
    proposed_financing,
    reinvestment_rate
):
    # Unpack business financials
    avg_monthly_revenue = business_financials.get("avg_monthly_revenue", 0)
    avg_monthly_operating_expenses = business_financials.get("avg_monthly_operating_expenses", 0)
    starting_cash = business_financials.get("current_cash_reserves", 0)

    # Unpack growth needs
    capital_required = growth_needs.get("capital_required", 0)
    expected_roi = growth_needs.get("expected_roi", 0)

    # Unpack proposed financing
    proposed_loan_amount = proposed_financing.get("proposed_loan_amount", 0)
    proposed_interest_rate = proposed_financing.get("proposed_annual_interest_rate", 0)
    proposed_loan_term = proposed_financing.get("proposed_loan_term", 0)

    # Prepare loan breakdowns
    loan_payments = []
    for loan in loans:
        principal = loan.get("principal_amount", 0)
        outstanding = loan.get("outstanding_balance", 0)
        annual_rate = loan.get("annual_interest_rate", 0)
        monthly_rate = annual_rate / 12 / 100
        term = loan.get("remaining_term_months", 1)
        # Amortization formula
        if monthly_rate > 0 and term > 0:
            payment = principal * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
        else:
            payment = outstanding / term if term else 0
        loan_payments.append({
            "loan_name": loan.get("loan_name", "Loan"),
            "monthly_payment": payment,
            "monthly_interest": outstanding * monthly_rate,
            "monthly_principal": payment - (outstanding * monthly_rate)
        })

    # Proposed loan breakdown
    if proposed_loan_amount and proposed_loan_term:
        monthly_rate = proposed_interest_rate / 12 / 100
        if monthly_rate > 0 and proposed_loan_term > 0:
            proposed_payment = proposed_loan_amount * (monthly_rate * (1 + monthly_rate) ** proposed_loan_term) / ((1 + monthly_rate) ** proposed_loan_term - 1)
        else:
            proposed_payment = proposed_loan_amount / proposed_loan_term if proposed_loan_term else 0
        loan_payments.append({
            "loan_name": "Proposed Loan",
            "monthly_payment": proposed_payment,
            "monthly_interest": proposed_loan_amount * monthly_rate,
            "monthly_principal": proposed_payment - (proposed_loan_amount * monthly_rate)
        })

    # Waterfall chart data
    chart_data = []
    cash_balance = starting_cash
    for period in range(1, projection_period + 1):
        # Calculate total loan payments for this period
        total_loan_interest = sum(lp["monthly_interest"] for lp in loan_payments)
        total_loan_principal = sum(lp["monthly_principal"] for lp in loan_payments)
        total_loan_payment = sum(lp["monthly_payment"] for lp in loan_payments)

        # Cash flows
        cash_inflow = avg_monthly_revenue
        cash_outflow = avg_monthly_operating_expenses + total_loan_interest
        net_operating_cash_flow = cash_inflow - cash_outflow
        net_cash_position = cash_balance + net_operating_cash_flow - total_loan_principal

        chart_data.append({
            "period": period,
            "starting_cash": cash_balance,
            "revenue": cash_inflow,
            "operating_expenses": avg_monthly_operating_expenses,
            "loan_interest_payments": total_loan_interest,
            "loan_principal_payments": total_loan_principal,
            "net_operating_cash_flow": net_operating_cash_flow,
            "net_cash_position": net_cash_position
        })

        # Update cash balance for next period
        cash_balance = net_cash_position
        # Optionally add reinvestment logic here

    # Key metrics
    total_interest_paid = sum([c["loan_interest_payments"] for c in chart_data])
    total_principal_paid = sum([c["loan_principal_payments"] for c in chart_data])
    ending_cash = chart_data[-1]["net_cash_position"] if chart_data else starting_cash

    key_metrics = {
        "total_interest_paid": total_interest_paid,
        "total_principal_paid": total_principal_paid,
        "ending_cash_position": ending_cash,
        "capital_required": capital_required,
        "expected_roi": expected_roi
    }

    insight = (
        f"Over the projected period, your MSME's cash position will change based on operating cash flows and debt repayments. "
        f"Total interest paid: ₱{total_interest_paid:,.2f}. Total principal repaid: ₱{total_principal_paid:,.2f}. "
        f"Ending cash position: ₱{ending_cash:,.2f}. Consider optimizing loan terms or reinvestment rates to improve liquidity."
    )

    show_my_math = [
        "Total Cash Inflow = Monthly Revenue",
        "Total Cash Outflow = Operating Expenses + Loan Interest Payments",
        "Net Operating Cash Flow = Inflow - Outflow",
        "Loan Principal Payment per Period = Amortization formula",
        "Net Cash Position = Starting Cash + Net Operating Cash Flow - Total Loan Principal Payments"
    ]

    response = {
        "status": "success",
        "data": {
            "inputs_received": {
                "scenario_type": scenario_type,
                "user_type": user_type,
                "projection_period": projection_period,
                "loans": loans,
                "business_financials": business_financials,
                "growth_needs": growth_needs,
                "proposed_financing": proposed_financing,
                "reinvestment_rate": reinvestment_rate
            },
            "chart_data": chart_data,
            "key_metrics": key_metrics,
            "insight": insight,
            "show_my_math": show_my_math
        }
    }

    return response



def simulate_wealth_building(
    goal_name,
    current_age,
    target_age,
    target_amount,
    current_savings,
    monthly_contribution,
    annual_contribution_increase=0,
    expected_annual_return=0.07,
    inflation_rate=0.035,
    risk_profile="Moderate",
    advisor_fee_percent=0
):
    years_to_goal = target_age - current_age
    months_to_goal = years_to_goal * 12
    monthly_return = (expected_annual_return - advisor_fee_percent / 100) / 12
    inflation_adjustment = (1 + inflation_rate) ** years_to_goal

    # Future Value of Initial Savings
    FV_initial = current_savings * ((1 + monthly_return) ** months_to_goal)

    # Future Value of Contributions (growing annuity if annual increase)
    FV_contributions = 0
    current_monthly_contribution = monthly_contribution
    for year in range(years_to_goal):
        for month in range(12):
            months_remaining = months_to_goal - (year * 12 + month)
            FV_contributions += current_monthly_contribution * ((1 + monthly_return) ** months_remaining)
        current_monthly_contribution *= (1 + annual_contribution_increase)

    total_projected_value_nominal = FV_initial + FV_contributions
    projected_final_value_real = total_projected_value_nominal / inflation_adjustment
    inflation_adjusted_target = target_amount / inflation_adjustment
    total_shortfall_real = inflation_adjusted_target - projected_final_value_real

    # Calculate required monthly contribution to hit the goal
    try:
        r = monthly_return
        n = months_to_goal
        FV_goal = inflation_adjusted_target
        required_monthly_contribution = (
            (FV_goal - FV_initial) * r / ((1 + r) ** n - 1)
        ) if r > 0 and n > 0 else FV_goal / n if n > 0 else FV_goal
    except Exception:
        required_monthly_contribution = None

    # Calculate required annual return to hit the goal (simple estimate)
    try:
        required_annual_return = (
            ((FV_goal / (current_savings + monthly_contribution * n)) ** (1 / years_to_goal)) - 1
        ) if years_to_goal > 0 else expected_annual_return
    except Exception:
        required_annual_return = expected_annual_return

    # Chart Data (stacked area)
    chart_data = []
    cumulative_contributions = 0
    cumulative_investment_growth = 0
    current_monthly_contribution = monthly_contribution
    total_value = current_savings
    for year in range(years_to_goal + 1):
        for month in range(12):
            if year * 12 + month > months_to_goal:
                break
            cumulative_contributions += current_monthly_contribution
            total_value = total_value * (1 + monthly_return) + current_monthly_contribution
            cumulative_investment_growth = total_value - cumulative_contributions
        chart_data.append({
            "year": current_age + year,
            "cumulative_contributions": round(cumulative_contributions, 2),
            "cumulative_investment_growth": round(cumulative_investment_growth, 2),
            "total_value": round(total_value, 2),
            "inflation_adjusted_target": round(inflation_adjusted_target, 2)
        })
        current_monthly_contribution *= (1 + annual_contribution_increase)

    # Rule-based insight
    percent_achieved = (projected_final_value_real / inflation_adjusted_target * 100) if inflation_adjusted_target else 0
    rule_based_insight = (
        f"Your current savings and contributions are projected to fall short of your {goal_name.lower()} goal by ₱{total_shortfall_real:,.2f} in real terms. "
        f"The current strategy is on track to achieve only {percent_achieved:.0f}% of the goal."
    )

    show_my_math = [
        "Future Value of Initial Savings (FV_initial) = Initial Savings * (1 + Expected Return)^Years",
        "Future Value of Contributions (FV_contributions) = PMT * [((1 + r)^n - 1) / r]",
        "Total Projected Value = FV_initial + FV_contributions",
        "Inflation-Adjusted Target = Nominal Target / (1 + Inflation Rate)^Years",
        "Shortfall = Inflation-Adjusted Target - Total Projected Value"
    ]

    response = {
        "status": "success",
        "data": {
            "inputs_received": {
                "scenario_type": "wealth_building",
                "user_type": "financial_advisor",
                "client_goal": {
                    "goal_name": goal_name,
                    "target_age": target_age,
                    "target_amount": target_amount
                },
                "contributions": {
                    "current_monthly_contribution": monthly_contribution,
                    "annual_contribution_increase_percent": annual_contribution_increase
                },
                "investment_details": {
                    "expected_annual_return_percent": expected_annual_return,
                    "inflation_rate_percent": inflation_rate
                }
            },
            "chart_data": chart_data,
            "key_metrics": {
                "projected_final_value_nominal": round(total_projected_value_nominal, 2),
                "projected_final_value_real": round(projected_final_value_real, 2),
                "total_shortfall_real": round(total_shortfall_real, 2),
                "required_monthly_contribution": round(required_monthly_contribution, 2) if required_monthly_contribution else None,
                "required_annual_return": round(required_annual_return, 4) if required_annual_return else None
            },
            "insight": rule_based_insight,
            "show_my_math": show_my_math
        }
    }

    return response