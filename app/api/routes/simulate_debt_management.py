from fastapi import APIRouter
from app.schemas.simulation_inputs import DebtManagementInput
from app.services.simulation_logic import simulate_debt_management

router = APIRouter()

@router.post("/simulate/debt-management")
def simulate_debt_management_route(data: DebtManagementInput):
    """
    POST endpoint to simulate debt management with user inputs:
    - debt: Total debt amount for the debt management simulation
    - monthly_payment: Monthly payment towards the debt
    - interest_rate: Annual interest rate on the debt
    - extra_payment: Extra payment towards the debt (if any)
    """
    result = simulate_debt_management(
        debt=data.debt,
        monthly_payment=data.monthly_payment,
        interest_rate=data.interest_rate,
        extra_payment=data.extra_payment,
    )

    return {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }