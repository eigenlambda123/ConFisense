from fastapi import APIRouter
from app.schemas.budget_optimization_schema import BudgetOptimizationInput
from app.services.simulation_logic import simulate_budget_optimization  

router = APIRouter()

@router.post("/simulate/budget-optimization")
def simulate_budget_optimization_route(data: BudgetOptimizationInput):
    result = simulate_budget_optimization(
        scenario_type=data.scenario_type,
        user_type=data.user_type,
        projection_months=data.projection_months,
        income=data.income.dict(),
        expenses=data.expenses.dict(),
        savings_goals=data.savings_goals.dict()
    )
    return result