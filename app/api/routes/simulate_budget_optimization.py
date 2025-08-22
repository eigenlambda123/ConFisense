from fastapi import APIRouter
from requests import session
from app.schemas.budget_optimization_schema import BudgetOptimizationInput
from app.services.simulation_logic import simulate_budget_optimization  
from app.models.budgeting_optimization_model import BudgetOptimizationModel
from app.services.ai_explainer import generate_response

from app.db.session import get_session
from fastapi import status
from fastapi import HTTPException

from sqlmodel import select


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


@router.delete("/budget-optimization/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget_optimization(scenario_id: int):
    with get_session() as session:
        scenario = session.get(BudgetOptimizationModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        session.delete(scenario)
        session.commit()
        session.refresh(scenario)
        return {"message": "Scenario deleted"}


@router.get("/budget-optimization/ai-explanation")
def get_ai_explanation():
    with get_session() as session:
        scenario = session.exec(
            select(BudgetOptimizationModel).order_by(BudgetOptimizationModel.created_at.desc())
        ).first()
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No budget optimization scenario found.")

        # Extract key stats for prompt context
        income = scenario.income
        expenses = scenario.expenses
        savings_goals = scenario.savings_goals

        # Extract summary stat
        total_monthly_income = income.get("monthly_net_income", 0) + income.get("other_monthly_income", 0)
        fixed = expenses.get("fixed_needs", {})
        variable = expenses.get("variable_needs", {})
        wants = expenses.get("wants_discretionary", {})
        fixed_total = sum(fixed.values())
        variable_total = sum(variable.values())
        wants_total = sum(wants.values())
        total_monthly_expenses = fixed_total + variable_total + wants_total
        avg_net_cash_flow = total_monthly_income - total_monthly_expenses - savings_goals.get("target_monthly_savings", 0)
        discretionary_spending_percent = (wants_total / total_monthly_income) if total_monthly_income else 0
        highest_discretionary_category = max(wants, key=wants.get) if wants else "N/A"
        highest_discretionary_value = wants.get(highest_discretionary_category, 0)
        emergency_fund_target = savings_goals.get("emergency_fund_target", 0)
        emergency_fund_months_current = (
            emergency_fund_target / savings_goals.get("target_monthly_savings", 1)
            if savings_goals.get("target_monthly_savings", 0) else "N/A"
        )

        prompt = (
            "As an expert financial advisor for Filipino families, analyze the provided monthly cash flow projection for a family in Lucena City. "
            "Focus on their income, expenses (fixed, variable, discretionary), and their net cash flow trend over the projected period. "
            "Identify key strengths or weaknesses in their spending habits. Explain in natural language, drawing insights specifically from the data. "
            "Highlight the most significant area of discretionary spending and its impact. Keep it concise, value-adding, and directly based on the numbers provided.\n\n"
            f"Inputs:\n"
            f"User profile: Income: ₱{total_monthly_income:,.2f}\n"
            f"Projected data: Average monthly net income: ₱{total_monthly_income:,.2f}. "
            f"Average monthly total expenses: ₱{total_monthly_expenses:,.2f}. "
            f"Average monthly net cash flow: ₱{avg_net_cash_flow:,.2f}. "
            f"Discretionary spending: ₱{wants_total:,.2f} ({discretionary_spending_percent:.2%} of income). "
            f"Highest discretionary category: {highest_discretionary_category} at ₱{highest_discretionary_value:,.2f}.\n"
            f"Emergency fund target: ₱{emergency_fund_target:,.2f}. Current path to target: {emergency_fund_months_current} months."
        )

        explanation_text = generate_response(prompt)

        return {
            "status": "success",
            "data": {
                "explanation_text": explanation_text,
                "model_info": {
                    "model_name": "cohere-command",
                    "prompt_version": "v1.0.0"
                }
            }
        }