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
    

@router.get("/budget-optimization/ai-suggestions")
def get_ai_suggestions():
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

        total_monthly_income = income.get("monthly_net_income", 0) + income.get("other_monthly_income", 0)
        wants = expenses.get("wants_discretionary", {})
        highest_discretionary_category = max(wants, key=wants.get) if wants else "N/A"
        highest_discretionary_value = wants.get(highest_discretionary_category, 0)
        emergency_fund_target = savings_goals.get("emergency_fund_target", 0)
        target_monthly_savings = savings_goals.get("target_monthly_savings", 0)
        emergency_fund_months_current = (
            emergency_fund_target / target_monthly_savings if target_monthly_savings else "N/A"
        )

        # Simulate a 20% reduction in highest discretionary category
        potential_increase_in_savings = highest_discretionary_value * 0.2 if highest_discretionary_value else 0
        optimized_monthly_savings = target_monthly_savings + potential_increase_in_savings
        emergency_fund_months_optimized = (
            emergency_fund_target / optimized_monthly_savings if optimized_monthly_savings else "N/A"
        )

        # Get the latest AI insight
        insight_prompt = (
            "As an expert financial advisor for Filipino families, analyze the provided monthly cash flow projection for a family in Lucena City. "
            "Focus on their income, expenses (fixed, variable, discretionary), and their net cash flow trend over the projected period. "
            "Identify key strengths or weaknesses in their spending habits. Explain in natural language, drawing insights specifically from the data. "
            "Highlight the most significant area of discretionary spending and its impact. Keep it concise, value-adding, and directly based on the numbers provided.\n\n"
            f"Inputs:\n"
            f"User profile: Income: ₱{total_monthly_income:,.2f}\n"
            f"Projected data: Highest discretionary category: {highest_discretionary_category} at ₱{highest_discretionary_value:,.2f}.\n"
            f"Emergency fund target: ₱{emergency_fund_target:,.2f}. Current path to target: {emergency_fund_months_current} months."
        )
        ai_insight = generate_response(insight_prompt)

        # Build suggestion prompt
        suggestion_prompt = (
            "Given the financial insights from the cash flow analysis and the goal to reach an emergency fund, "
            "recommend actionable, next steps for this Filipino family. The suggestions should be practical, easy to understand, "
            "and directly address the identified weaknesses, particularly regarding discretionary spending. Focus on specific, measurable actions.\n\n"
            f"Inputs:\n"
            f"Insight: {ai_insight}\n"
            f"Projected data: Potential monthly savings from 20% reduction in highest discretionary: ₱{potential_increase_in_savings:,.2f}. "
            f"Optimized path to emergency fund: {emergency_fund_months_optimized} months.\n"
            f"Emergency Fund Goal: ₱{emergency_fund_target:,.2f}."
        )

        # Get actionable recommendations
        raw_suggestions = generate_response(suggestion_prompt)

        # We may need to parse the LLM output into structured recommendations

        return {
            "status": "success",
            "data": {
                "actionable_recommendations": [
                    {
                        "priority": "High",
                        "title": "Reduce Discretionary Spending",
                        "description": f"Aim to reduce your monthly '{highest_discretionary_category.replace('_', ' ')}' expense by ₱{potential_increase_in_savings:,.2f}. This could mean cooking at home more often or bringing packed lunches to work."
                    },
                    {
                        "priority": "High",
                        "title": "Automate Savings",
                        "description": f"Set up an automatic transfer of ₱{optimized_monthly_savings:,.2f} from your payroll account to a separate emergency fund savings account each payday."
                    },
                    {
                        "priority": "Medium",
                        "title": "Track All Expenses",
                        "description": "Use a simple budgeting app or notebook to record all your daily variable expenses for one month. This builds awareness and helps you stick to your revised budget."
                    }
                ],
                "model_info": {
                    "model_name": "cohere-command",
                    "prompt_version": "v1.0.0"
                }
            }
        }