from fastapi import APIRouter
from app.schemas.budget_optimization_schema import BudgetOptimizationInput
from app.services.simulation_logic import simulate_budget_optimization  
from app.models.budgeting_optimization_model import BudgetOptimizationModel

from app.db.session import get_session
from fastapi import status

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

@router.post("/budget-optimization/save")
def save_budget_optimization_to_db(data: BudgetOptimizationInput):
    with get_session() as session:
        scenario = BudgetOptimizationModel(
            scenario_type=data.scenario_type,
            user_type=data.user_type,
            projection_months=data.projection_months,
            income=data.income.model_dump(),
            expenses=data.expenses.model_dump(),
            savings_goals=data.savings_goals.model_dump()
        )

        session.add(scenario)
        session.commit()
        session.refresh(scenario)

    return {"id": scenario.id}
