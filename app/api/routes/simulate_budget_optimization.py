from fastapi import APIRouter, HTTPException, status

from sqlmodel import select, delete

from app.db.session import get_session
from app.models.budgeting_optimization_model import BudgetOptimizationModel
from app.schemas.budget_optimization_schema import BudgetOptimizationInput
from app.services.simulation_logic import simulate_budget_optimization
from app.services.ai_explainer import generate_response

router = APIRouter()


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


# @router.delete("/budget-optimization/{scenario_id}")
# def delete_budget_optimization(scenario_id: int):
#     with get_session() as session:
#         scenario = session.get(BudgetOptimizationModel, scenario_id)
#         if not scenario:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
        
#         session.delete(scenario)
#         session.commit()
#         return {"message": "Scenario deleted"}


@router.delete("/budget-optimization/delete-all")
def delete_all_budget_optimizations():
    with get_session() as session:
        result = session.exec(delete(BudgetOptimizationModel))
        session.commit()
        return {"message": f"{result.rowcount} scenarios deleted"}


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

        explanation_prompt = (
            f'''As a financial advisor specializing in helping Filipino families, analyze the following monthly cash flow data.  

            **Output format (IMPORTANT):**  
            Return ONLY one short paragraph of plain text.  
            Do not include JSON, Markdown, bullet points, or extra formatting.  

            Guidelines:
            - Speak directly to the user using "you" and "your," not "this family."
            - Maximum 3–5 sentences (under 120 words).
            - Use a warm, conversational tone.
            - Focus on insights, not repeating the numbers.
            - Mention their overall financial health, the biggest discretionary spending issue, and one clear recommendation.

            [Data provided below]
            • Income: ₱{total_monthly_income:,.2f}
            • Expenses: ₱{total_monthly_expenses:,.2f}
            • Net Cash Flow: ₱{avg_net_cash_flow:,.2f}
            • Discretionary spending: ₱{wants_total:,.2f} ({discretionary_spending_percent:.2%})
            • Highest discretionary category: {highest_discretionary_category} at ₱{highest_discretionary_value:,.2f}
            • Emergency fund target: ₱{emergency_fund_target:,.2f}, current path {emergency_fund_months_current} months
            • What-if factors: Income growth {income_growth_rate:.2%}, Wants reduction {wants_reduction_rate:.2%}, Savings increase {savings_increase_rate:.2%}
            '''
        )

        explanation_text = generate_response(explanation_prompt)

        return {
            "status": "success",
            "data": {
                "explanation_text": explanation_text,
                "model_info": {
                    "model_name": "gemini-1.5-flash"
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

        # Build suggestion prompt, instructing the AI to return JSON
        suggestion_prompt = (
            f'''As a financial expert, generate 3 to 5 actionable next steps for a Filipino family in Lucena City
            to improve their budget and accelerate their savings.

            **Output format (IMPORTANT):**
            - Return a numbered list of practical suggestions.
            - Each item should be a complete sentence or two, without any special formatting like bolding.
            - Do not include any JSON, markdown, or other special formatting.

            **Example Output:**
            1. Reduce Dining Out: Given your high spending on restaurants, consider packing baon (packed lunch) to work at least three times a week. This could save you up to ₱500 per week.
            2. Explore Palengke for Groceries: Shop for your produce at the local palengke (wet market) instead of the supermarket. This can reduce your food expenses by 15-20% monthly.

            **Inputs:**
            • Highest discretionary category: {highest_discretionary_category} at ₱{highest_discretionary_value:,.2f}
            • Emergency Fund Goal: ₱{emergency_fund_target:,.2f}
            • Current path to goal: {emergency_fund_months_current} months
            • Optimized path to goal (20% reduction): {emergency_fund_months_optimized} months
            • Potential increase in monthly savings: ₱{potential_increase_in_savings:,.2f}
            '''
        )

        raw_suggestions = generate_response(suggestion_prompt)

        print('RAW SUGGESTIONS: ', raw_suggestions)

        return {
            "status": "success",
            "data": {
                "suggestions_text": raw_suggestions,
                "model_info": {
                    "model_name": "gemini-1.5-flash"
                }
            }
        }
    