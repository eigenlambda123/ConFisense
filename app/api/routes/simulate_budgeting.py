from fastapi import APIRouter
from app.schemas.simulation_inputs import BudgetInput
from app.services.simulation_logic import simulate_budgeting

router = APIRouter()

@router.post("/simulate/budgeting")
def simulate_budgeting_route(data: BudgetInput):
    """
    POST endpoint to simulate budgeting with user inputs:
    - income: Monthly income for the budget simulation
    - fixed_expenses: Monthly fixed expenses for the budget simulation
    - discretionary_pct: Percentage of income allocated to discretionary spending
    - target_savings: Target savings amount for the budget simulation
    """
    if data.discretionary_pct < 0 or data.discretionary_pct > 100:
        raise ValueError("Discretionary percentage must be between 0 and 100")

    result = simulate_budgeting(
        income=data.income,
        fixed_expenses=data.fixed_expenses,
        discretionary_pct=data.discretionary_pct,
        target_savings=data.target_savings,
    )

    return {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }