def simulate_emergency_fund(
    monthly_expenses,
    months_of_expenses,
    current_emergency_savings,
    monthly_savings,
    annual_interest_rate_percent
):
    """
    Simulate the growth of an emergency fund over time with compounding interest and monthly contributions.
    """

    # 1. Calculate independent values
    target_amount = monthly_expenses * months_of_expenses
    remaining_target = max(target_amount - current_emergency_savings, 0)
    monthly_interest_rate = (annual_interest_rate_percent / 100) / 12

    # 2. Initialize loop variables
    current_balance = current_emergency_savings
    current_month = 0
    balance_history = [round(current_balance, 2)]
    MAX_MONTHS_TO_SIMULATE = 600
    time_to_reach_target = None

    # 3. Simulation loop
    if current_balance >= target_amount:
        time_to_reach_target = 0
    else:
        while current_balance < target_amount and current_month < MAX_MONTHS_TO_SIMULATE:
            current_month += 1
            # Interest earned this month (for explanation, not used directly)
            interest_earned = current_balance * monthly_interest_rate
            # Update balance
            current_balance = current_balance * (1 + monthly_interest_rate) + monthly_savings
            # Prevent overshooting the target in the graph
            balance_history.append(round(min(current_balance, target_amount), 2))
        if current_balance >= target_amount:
            time_to_reach_target = current_month
        else:
            time_to_reach_target = None  # Unreachable

    # 4. Prepare API response
    months_labels = list(range(len(balance_history)))
    summary = (
        f"Goal reached in {time_to_reach_target} months."
        if time_to_reach_target is not None
        else "Goal is unreachable within 600 months."
    )

    response = {
        "status": "success",
        "message": "Emergency Fund simulation successful.",
        "data": {
            "target_amount": round(target_amount, 2),
            "time_to_reach_target_months": time_to_reach_target,
            "projection_data": {
                "months_labels": months_labels,
                "balance_history": balance_history
            },
            "summary": summary,
            "math_explanation": {
                "title": "The 'Glass Box': How We Calculate Your Emergency Fund",
                "sections": [
                    {
                        "heading": "1. Your Inputs & Goal",
                        "items": [
                            f"Your Monthly Expenses: ₱{monthly_expenses:,}",
                            f"Desired Months Covered: {months_of_expenses} months",
                            f"--> Calculated Target Emergency Fund: ₱{target_amount:,}",
                            f"Your Current Savings: ₱{current_emergency_savings:,}",
                            f"Your Monthly Contribution: ₱{monthly_savings:,}",
                            f"Expected Annual Interest Rate: {annual_interest_rate_percent}%"
                        ]
                    },
                    {
                        "heading": "2. The Simulation Process",
                        "items": [
                            "We simulate your fund's growth month-by-month.",
                            "Each month, two things happen:",
                            "   a. **Interest is Earned:** Your current balance grows by your monthly interest rate "
                            f"({monthly_interest_rate:.6f} for {annual_interest_rate_percent}% annually).",
                            f"   b. **Your Contribution is Added:** Your ₱{monthly_savings:,} monthly contribution is added to the balance.",
                            "This process calculates interest on your growing total, showing the power of compounding.",
                            "Formula used each month: `New Balance = (Previous Balance × (1 + Monthly Interest Rate)) + Monthly Contribution`"
                        ]
                    },
                    {
                        "heading": "3. The Outcome",
                        "items": [
                            (
                                f"Based on this simulation, your fund is projected to reach ₱{target_amount:,.0f} "
                                f"in {time_to_reach_target} months."
                                if time_to_reach_target is not None
                                else "Based on this simulation, your fund will not reach the target within 600 months."
                            )
                        ]
                    }
                ]
            }
        },
        "inputs_received": {
            "monthly_expenses": monthly_expenses,
            "months_of_expenses": months_of_expenses,
            "current_emergency_savings": current_emergency_savings,
            "monthly_savings": monthly_savings,
            "annual_interest_rate_percent": annual_interest_rate_percent
        }
    }
    return response



def simulate_budgeting(income, fixed_expenses, discretionary_pct, target_savings):
    """
    Simulate a monthly budget based on income, fixed expenses, discretionary percentage, and target savings
    """

    # calculate discretionary spending and potential savings
    # discretionary_pct is a percentage, so we divide by 100
    # total expenses is the sum of fixed expenses and discretionary spending
    # potential savings is income minus total expenses
    discretionary = income * (discretionary_pct / 100)
    total_expenses = fixed_expenses + discretionary
    potential_savings = income - total_expenses

    return {
        "data": {
            "Fixed Expenses": fixed_expenses,
            "Discretionary": discretionary,
            "Potential Savings": potential_savings
        },
        "summary": f"You can potentially save ₱{potential_savings:,.0f} per month.",
        "math_explanation": {
            "title": "The 'Glass Box': How We Calculate",
            "sections": [
                {
                    "heading": "1. Income Breakdown",
                    "items": [
                        f"Monthly Income: ₱{income:,}",
                        f"Fixed Expenses: ₱{fixed_expenses:,}",
                        f"Discretionary (%): {discretionary_pct}%",
                        f"Target Monthly Savings: ₱{target_savings:,}"
                    ]
                },
                {
                    "heading": "2. Formula",
                    "items": [
                        "Discretionary = Income × Discretionary %",
                        "Total Expenses = Fixed + Discretionary",
                        "Potential Savings = Income - Total Expenses"
                    ]
                }
            ]
        }
    }



def simulate_debt_management(debt, monthly_payment, interest_rate, extra_payment):
    """
    Simulate the process of paying off debt over time
    """

    # rate is the monthly interest rate, calculated from the annual interest rate
    # balance starts at the total debt
    # month is the counter for how many months it takes to pay off the debt
    # total_interest accumulates the total interest paid
    # history keeps track of the remaining balance each month
    # payment is the total monthly payment including any extra payment
    rate = interest_rate / 12 / 100
    balance = debt
    month = 0
    total_interest = 0
    history = []
    payment = monthly_payment + extra_payment


    # if payment is less than or equal to the interest accrued, debt cannot be reduced
    if payment <= balance * rate:
        return {
            "data": [],
            "summary": "Payment too low to reduce debt.",
            "math_explanation": {"title": "", "sections": []}
        }

    # loop until the balance is paid off
    # interest is calculated as the balance times the monthly rate
    # principal is the payment minus the interest
    # balance is reduced by the principal
    # total_interest is accumulated
    # month is incremented
    # history is updated with the remaining balance
    while balance > 0:
        interest = balance * rate
        principal = payment - interest
        balance -= principal
        total_interest += interest
        month += 1
        history.append(balance if balance > 0 else 0)

        if month > 600: # prevent infinite loop
            break

    return {
        "data": history,
        "summary": f"Debt paid off in {month} months with ₱{total_interest:,.0f} in interest.",
        "math_explanation": {
            "title": "The 'Glass Box': How We Calculate",
            "sections": [
                {
                    "heading": "1. Inputs",
                    "items": [
                        f"Total Debt: ₱{debt:,}",
                        f"Annual Interest Rate: {interest_rate}%",
                        f"Monthly Payment: ₱{monthly_payment:,}",
                        f"Extra Payment: ₱{extra_payment:,}"
                    ]
                },
                {
                    "heading": "2. Formula",
                    "items": [
                        "Monthly Interest = Balance × Monthly Rate",
                        "Principal = Payment - Interest",
                        "Balance -= Principal (until paid off)"
                    ]
                }
            ]
        }
    }




def simulate_investing(initial, monthly, return_rate, years):
    """
    Simulate the growth of an investment over time using the future value formula
    1. Future Value of Lump Sum: FV = P × (1 + r)^n
    2. Future Value of Annuity: FV = PMT × [((1 + r)^n - 1) / r] × (1 + r)
    where:
    - P = initial investment
    - PMT = monthly contribution   
    - r = monthly return rate (annual rate / 12)
    - n = total number of months (years * 12)
    """


    # months is the total number of months, calculated as years * 12
    # r is the monthly return rate, calculated as annual return rate divided by 12 and converted to decimal
    # fv_lump_sum is the future value of the initial investment
    # fv_annuity is the future value of the monthly contributions
    # total is the sum of fv_lump_sum and fv_annuity
    months = years * 12
    r = return_rate / 12 / 100

    fv_lump_sum = initial * ((1 + r) ** months)
    fv_annuity = monthly * (((1 + r) ** months - 1) / r) * (1 + r)
    total = fv_lump_sum + fv_annuity

    projection = []
    current = initial
    for m in range(1, months + 1):
        current = current * (1 + r) + monthly
        projection.append(round(current))

    return {
        "data": projection,
        "summary": f"Estimated future value: ₱{total:,.0f} after {years} years.",
        "math_explanation": {
            "title": "The 'Glass Box': How We Calculate",
            "sections": [
                {
                    "heading": "1. Assumptions",
                    "items": [
                        f"Initial: ₱{initial:,}",
                        f"Monthly: ₱{monthly:,}",
                        f"Annual Return: {return_rate}%",
                        f"Time Horizon: {years} years"
                    ]
                },
                {
                    "heading": "2. Formula",
                    "items": [
                        "FV = Initial × (1 + r)^n + PMT × [((1 + r)^n - 1) / r] × (1 + r)",
                        "*r = monthly rate, n = total months*"
                    ]
                }
            ]
        }
    }




def simulate_education_fund(today_cost, years, current_savings, monthly_contrib, return_rate, inflation_rate):
    """
    Simulate the growth of an education fund over time
    """

    # future_cost is the cost of education in the future, calculated using the inflation rate
    # months is the total number of months until the fund is needed, calculated as years * 12
    # r is the monthly return rate, calculated as annual return rate divided by 12 and converted to decimal
    # fv_savings is the future value of the current savings and monthly contributions
    # gap is the difference between the future value of savings and the future cost
    future_cost = today_cost * ((1 + inflation_rate / 100) ** years)
    months = years * 12
    r = return_rate / 12 / 100

    fv_savings = current_savings * ((1 + r) ** months) + monthly_contrib * (((1 + r) ** months - 1) / r) * (1 + r)
    gap = fv_savings - future_cost

    return {
        "data": [fv_savings, future_cost],
        "summary": f"You will {'exceed' if gap >= 0 else 'fall short by'} ₱{abs(gap):,.0f} in {years} years.",
        "math_explanation": {
            "title": "The 'Glass Box': How We Calculate",
            "sections": [
                {
                    "heading": "1. Projections",
                    "items": [
                        f"Today's Cost: ₱{today_cost:,}",
                        f"Years Until Needed: {years}",
                        f"Expected Inflation: {inflation_rate}%",
                        f"Expected Return: {return_rate}%"
                    ]
                },
                {
                    "heading": "2. Formula",
                    "items": [
                        "Future Cost = Cost × (1 + Inflation)^Years",
                        "Future Value = Lump Sum + Monthly Contributions Compounded",
                        "Gap = Future Value - Future Cost"
                    ]
                }
            ]
        }
    }




def simulate_major_purchase(price, down_pct, years_to_save, current_savings, monthly_contrib, savings_return, loan_rate, loan_term):
    """
    Simulate the process of saving for a major purchase and taking out a loan
    """

    # down_payment is the amount needed for the down payment
    # loan_amount is the total amount of the loan after the down payment
    # save_months is the total number of months to save, calculated as years_to_save
    # r_save is the monthly savings return rate, calculated as annual savings return divided by 12 and converted to decimal
    # fv_savings is the future value of the savings after the saving period
    # r_loan is the monthly loan rate, calculated as annual loan rate divided by 12 and converted to decimal
    # n_loan is the total number of months for the loan term, calculated as loan_term * 12
    # monthly_loan_payment is the monthly payment for the loan, calculated using the formula for an amortizing loan
    # total_interest is the total interest paid over the life of the loan, calculated as the total payments minus the loan amount
    down_payment = price * (down_pct / 100)
    loan_amount = price - down_payment
    save_months = years_to_save * 12
    r_save = savings_return / 12 / 100

    fv_savings = current_savings * ((1 + r_save) ** save_months) + monthly_contrib * (((1 + r_save) ** save_months - 1) / r_save) * (1 + r_save)

    r_loan = loan_rate / 12 / 100
    n_loan = loan_term * 12

    if r_loan == 0:
        monthly_loan_payment = loan_amount / n_loan
    else:
        monthly_loan_payment = loan_amount * r_loan / (1 - (1 + r_loan) ** -n_loan)

    total_interest = (monthly_loan_payment * n_loan) - loan_amount

    return {
        "data": {
            "FV Savings": fv_savings,
            "Required Down Payment": down_payment,
            "Monthly Loan Payment": monthly_loan_payment,
            "Total Interest": total_interest
        },
        "summary": f"Monthly loan payment: ₱{monthly_loan_payment:,.0f}, Total interest: ₱{total_interest:,.0f}.",
        "math_explanation": {
            "title": "The 'Glass Box': How We Calculate",
            "sections": [
                {
                    "heading": "1. Purchase Plan",
                    "items": [
                        f"Target Price: ₱{price:,}",
                        f"Down Payment: {down_pct}%",
                        f"Loan Term: {loan_term} years",
                        f"Loan Rate: {loan_rate}%",
                        f"Savings Rate: {savings_return}%"
                    ]
                },
                {
                    "heading": "2. Formulas",
                    "items": [
                        "FV Savings = Lump Sum + Monthly Contributions Compounded",
                        "Loan Payment = Loan × [r / (1 - (1 + r)^-n)]",
                        "Total Interest = Payment × n - Loan"
                    ]
                }
            ]
        }
    }




def run_simulation(scenario: str, params: dict):
    """
    Run the appropriate financial simulation based on the scenario and parameters provided
    """
    simulations = {
        "emergency": simulate_emergency_fund,
        "budgeting": simulate_budgeting,
        "debt": simulate_debt_management,
        "investing": simulate_investing,
        "education": simulate_education_fund,
        "purchase": simulate_major_purchase,
    }

    if scenario not in simulations:
        raise ValueError("Unsupported scenario")

    return simulations[scenario](**params)
