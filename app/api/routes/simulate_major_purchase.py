from fastapi import APIRouter
from app.schemas.simulation_inputs import MajorPurchaseInput
from app.services.simulation_logic import simulate_major_purchase

router = APIRouter()

@router.post("/simulate/major-purchase")
def simulate_major_purchase_route(data: MajorPurchaseInput):
    """
    POST endpoint to simulate major purchase savings with user inputs:
    - price: Total price of the major purchase
    - down_pct: Percentage of the price to be paid as a down payment
    - years_to_save: Number of years to save for the purchase
    - current_savings: Current savings amount for the purchase
    - monthly_contrib: Monthly contribution towards the purchase savings
    - savings_return: Expected annual return rate on the savings
    - loan_rate: Expected annual interest rate on the loan
    - loan_term: Number of years for the loan repayment
    """
    result = simulate_major_purchase(
        price=data.price,
        down_pct=data.down_pct,
        years_to_save=data.years_to_save,
        current_savings=data.current_savings,
        monthly_contrib=data.monthly_contrib,
        savings_return=data.savings_return,
        loan_rate=data.loan_rate,
        loan_term=data.loan_term
    )

    return {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }

    