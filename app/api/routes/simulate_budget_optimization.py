from fastapi import APIRouter, HTTPException, status
from app.schemas.budget_optimization_schema import BudgetOptimizationInput
from app.services.simulation_logic import simulate_budget_optimization
from app.models.budgeting_optimization_model import BudgetOptimizationModel
from app.services.ai_explainer import generate_response
from app.db.session import get_session
from sqlmodel import select
import json

router = APIRouter()

def get_financial_summary(scenario: BudgetOptimizationModel):
    """A helper function to extract and calculate key financial metrics."""
    income = scenario.income
    expenses = scenario.expenses
    savings_goals = scenario.savings_goals
    
    total_monthly_income = income.get("monthly_gross_income", 0) + income.get("other_monthly_income", 0)
    
    fixed_total = sum(expenses.get("fixed_needs", {}).values())
    variable_total = sum(expenses.get("variable_needs", {}).values())
    wants_total = sum(expenses.get("wants_discretionary", {}).values())
    
    total_monthly_expenses = fixed_total + variable_total + wants_total
    
    avg_net_cash_flow = total_monthly_income - total_monthly_expenses - savings_goals.get("target_monthly_savings", 0)
    
    wants = expenses.get("wants_discretionary", {})
    highest_discretionary_category = max(wants, key=wants.get) if wants else "N/A"
    highest_discretionary_value = wants.get(highest_discretionary_category, 0)
    
    discretionary_spending_percent = (wants_total / total_monthly_income) if total_monthly_income else 0
    
    emergency_fund_target = savings_goals.get("emergency_fund_target", 0)
    target_monthly_savings = savings_goals.get("target_monthly_savings", 0)
    
    emergency_fund_months_current = (
        emergency_fund_target / target_monthly_savings if target_monthly_savings > 0 else "N/A"
    )
    
    potential_increase_in_savings = highest_discretionary_value * 0.2 if highest_discretionary_value else 0
    optimized_monthly_savings = target_monthly_savings + potential_increase_in_savings
    emergency_fund_months_optimized = (
        emergency_fund_target / optimized_monthly_savings if optimized_monthly_savings > 0 else "N/A"
    )

    return {
        "total_monthly_income": total_monthly_income,
        "total_monthly_expenses": total_monthly_expenses,
        "avg_net_cash_flow": avg_net_cash_flow,
        "discretionary_spending_percent": discretionary_spending_percent,
        "highest_discretionary_category": highest_discretionary_category,
        "highest_discretionary_value": highest_discretionary_value,
        "emergency_fund_target": emergency_fund_target,
        "emergency_fund_months_current": emergency_fund_months_current,
        "potential_increase_in_savings": potential_increase_in_savings,
        "optimized_monthly_savings": optimized_monthly_savings,
        "emergency_fund_months_optimized": emergency_fund_months_optimized
    }

@router.post("/simulate/budget-optimization")
def simulate_and_save_route(data: BudgetOptimizationInput):
    result = simulate_budget_optimization(
        scenario_type=data.scenario_type,
        user_type=data.user_type,
        projection_months=data.projection_months,
        income=data.income.model_dump(),
        expenses=data.expenses.model_dump(),
        savings_goals=data.savings_goals.model_dump(),
        what_if_factors=data.what_if_factors.model_dump()
    )
    return result


@router.post("/budget-optimization/save")
def save_budget_optimization_to_db(data: BudgetOptimizationInput):
    # run simulation to get results
    sim_result = simulate_budget_optimization(
        scenario_type=data.scenario_type,
        user_type=data.user_type,
        projection_months=data.projection_months,
        income=data.income.model_dump(),
        expenses=data.expenses.model_dump(),
        savings_goals=data.savings_goals.model_dump(),
        what_if_factors=data.what_if_factors.model_dump()
    )
    sim_data = sim_result["data"]

    with get_session() as session:
        scenario = BudgetOptimizationModel(
            scenario_type=data.scenario_type,
            user_type=data.user_type,
            projection_months=data.projection_months,
            income=data.income.model_dump(),
            expenses=data.expenses.model_dump(),
            savings_goals=data.savings_goals.model_dump(),
            what_if_factors=data.what_if_factors.model_dump(),
            chart_data=sim_data.get("chart_data"),
            key_metrics=sim_data.get("key_metrics"),
            insight=sim_data.get("insight")
        )

        session.add(scenario)
        session.commit()
        session.refresh(scenario)

    return {"id": scenario.id}


@router.delete("/budget-optimization/{scenario_id}")
def delete_budget_optimization(scenario_id: int):
    with get_session() as session:
        scenario = session.get(BudgetOptimizationModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
        
        session.delete(scenario)
        session.commit()
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
        what_if_factors = scenario.what_if_factors

        total_monthly_income = income.get("monthly_gross_income", 0) + income.get("other_monthly_income", 0)
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

        # What-if factors context
        income_growth_rate = what_if_factors.get("income_growth_rate", 0)
        wants_reduction_rate = what_if_factors.get("wants_reduction_rate", 0)
        savings_increase_rate = what_if_factors.get("savings_increase_rate", 0)

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
            f"Emergency fund target: ₱{emergency_fund_target:,.2f}. Current path to target: {emergency_fund_months_current} months.\n"
            f"What-if factors: Income growth rate: {income_growth_rate:.2%}, Wants reduction rate: {wants_reduction_rate:.2%}, Savings increase rate: {savings_increase_rate:.2%}."
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
        what_if_factors = scenario.what_if_factors

        total_monthly_income = income.get("monthly_gross_income", 0) + income.get("other_monthly_income", 0)
        wants = expenses.get("wants_discretionary", {})
        highest_discretionary_category = max(wants, key=wants.get) if wants else "N/A"
        highest_discretionary_value = wants.get(highest_discretionary_category, 0)
        emergency_fund_target = savings_goals.get("emergency_fund_target", 0)
        target_monthly_savings = savings_goals.get("target_monthly_savings", 0)
        emergency_fund_months_current = (
            emergency_fund_target / target_monthly_savings if target_monthly_savings else "N/A"
        )

        # What-if factors context
        income_growth_rate = what_if_factors.get("income_growth_rate", 0)
        wants_reduction_rate = what_if_factors.get("wants_reduction_rate", 0)
        savings_increase_rate = what_if_factors.get("savings_increase_rate", 0)

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
            f"Emergency fund target: ₱{emergency_fund_target:,.2f}. Current path to target: {emergency_fund_months_current} months.\n"
            f"What-if factors: Income growth rate: {income_growth_rate:.2%}, Wants reduction rate: {wants_reduction_rate:.2%}, Savings increase rate: {savings_increase_rate:.2%}."
        )
        ai_insight = generate_response(insight_prompt)

        # Build suggestion prompt, instructing the AI to return JSON
        suggestion_prompt = (
            "Given the financial insights from the cash flow analysis and the goal to reach an emergency fund, "
            "recommend actionable, next steps for this Filipino family. The suggestions should be practical, easy to understand, "
            "and directly address the identified weaknesses, particularly regarding discretionary spending. Focus on specific, measurable actions.\n\n"
            "Return your answer as a JSON array of objects with keys: priority, title, description.\n"
            f"Inputs:\n"
            f"Insight: {ai_insight}\n"
            f"Projected data: Potential monthly savings from 20% reduction in highest discretionary: ₱{potential_increase_in_savings:,.2f}. "
            f"Optimized path to emergency fund: {emergency_fund_months_optimized} months.\n"
            f"Emergency Fund Goal: ₱{emergency_fund_target:,.2f}.\n"
            f"What-if factors: Income growth rate: {income_growth_rate:.2%}, Wants reduction rate: {wants_reduction_rate:.2%}, Savings increase rate: {savings_increase_rate:.2%}."
        )

        raw_suggestions = generate_response(suggestion_prompt)

        # Try to parse the AI output as JSON
        try:
            actionable_recommendations = json.loads(raw_suggestions)
        except Exception:
            actionable_recommendations = [{
                "priority": "Info",
                "title": "AI Suggestion",
                "description": raw_suggestions
            }]

        return {
            "status": "success",
            "data": {
                "actionable_recommendations": actionable_recommendations,
                "model_info": {
                    "model_name": "cohere-command",
                    "prompt_version": "v1.0.0"
                }
            }
        }
    