from fastapi import APIRouter
from app.schemas.simulation_inputs import BudgetInput
from app.services.simulation_logic import simulate_budgeting
from app.models.budgeting import BudgetingModel

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# Exception imports
from fastapi import HTTPException
from fastapi import status

# ai explaination imports
from app.services.ai_explainer import generate_response, count_tokens

router = APIRouter()

@router.post("/simulate/budgeting")
def simulate_budgeting_route(data: BudgetInput):

    result = simulate_budgeting(
        monthly_net_income=data.monthly_net_income,
        housing_expense=data.housing_expense,
        food_grocery_expense=data.food_grocery_expense,
        utilities_expense=data.utilities_expense,
        transportation_expense=data.transportation_expense,
        debt_payments_expense=data.debt_payments_expense,
        medical_healthcare_expense=data.medical_healthcare_expense,
        education_expense=data.education_expense,
        household_supplies_maintenance_expense=data.household_supplies_maintenance_expense,
        personal_care_shopping_expense=data.personal_care_shopping_expense,
        entertainment_recreation_expense=data.entertainment_recreation_expense,
        gifts_donations_expense=data.gifts_donations_expense,
        savings_investment_contribution=data.savings_investment_contribution
    )

    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="budgeting",
            input_data=data.model_dump(),
            output_data=result,
        )
        session.add(log)
        session.commit()

    return result

@router.get("/budgeting/all")
def get_all_budgeting_scenarios():
    with get_session() as session:
        scenarios = session.query(BudgetingModel).all()
        return [s.dict() for s in scenarios]


@router.post("/budgeting/save")
def save_budgeting(data: BudgetInput):
    with get_session() as session:
        scenario = BudgetingModel(
            scenario_title=data.scenario_title,
            monthly_net_income=data.monthly_net_income,
            housing_expense=data.housing_expense,
            food_grocery_expense=data.food_grocery_expense,
            utilities_expense=data.utilities_expense,
            transportation_expense=data.transportation_expense,
            debt_payments_expense=data.debt_payments_expense,
            medical_healthcare_expense=data.medical_healthcare_expense,
            education_expense=data.education_expense,
            household_supplies_maintenance_expense=data.household_supplies_maintenance_expense,
            personal_care_shopping_expense=data.personal_care_shopping_expense,
            entertainment_recreation_expense=data.entertainment_recreation_expense,
            gifts_donations_expense=data.gifts_donations_expense,
            savings_investment_contribution=data.savings_investment_contribution

        )
    session.add(scenario)
    session.commit()
    session.refresh(scenario)
    return {"id": scenario.id, "message": "Scenario saved"}


@router.delete("/budgeting/{scenario_id}")
def delete_budgeting_scenario(scenario_id: int):
    with get_session() as session:
        scenario = session.get(BudgetingModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
        session.delete(scenario)
        session.commit()
        session.refresh(scenario)
        return {"message": "Scenario deleted"}
    

@router.get("/budgeting/ai-explanation")
def budgeting_ai_explanation():
    """
    Generate an AI explanation based on all budgeting scenarios in the database.
    """
    with get_session() as session:
        scenarios = session.query(BudgetingModel).all()
        if not scenarios:
            return {"ai_explanation": "No budgeting scenarios found."}

        scenario_descriptions = []
        for s in scenarios:
            scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Monthly Net Income ₱{s.monthly_net_income}, "
                f"Housing Expense ₱{s.housing_expense}, "
                f"Food & Grocery Expense ₱{s.food_grocery_expense}, "
                f"Utilities Expense ₱{s.utilities_expense}, "
                f"Transportation Expense ₱{s.transportation_expense}, "
                f"Debt Payments Expense ₱{s.debt_payments_expense}, "
                f"Medical & Healthcare Expense ₱{s.medical_healthcare_expense}, "
                f"Education Expense ₱{s.education_expense}, "
                f"Household Supplies & Maintenance Expense ₱{s.household_supplies_maintenance_expense}, "
                f"Personal Care & Shopping Expense ₱{s.personal_care_shopping_expense}, "
                f"Entertainment & Recreation Expense ₱{s.entertainment_recreation_expense}, "
                f"Gifts & Donations Expense ₱{s.gifts_donations_expense}, "
                f"Savings & Investment Contribution ₱{s.savings_investment_contribution}"
            )

        prompt = (
            "Compare the budgeting scenarios below. "
            "For each, mention the scenario number and title, and all expense categories. "
            "Highlight the main differences. Keep it concise and clear. "
            "Express all amounts in Philippine pesos (₱). "
            "Do not introduce the summary or repeat the prompt. "
            "Start your summary immediately after this sentence.\n\n"
            + "\n".join(scenario_descriptions)
            + "\nExample: Scenario 1 (Basic): Monthly Net Income ₱50,000, Housing Expense ₱15,000, Food & Grocery Expense ₱10,000. Scenario 2 (Advanced): Monthly Net Income ₱100,000, Housing Expense ₱30,000, Food & Grocery Expense ₱20,000. The advanced scenario has higher income and expenses, showing more complexity."
        )
        print(prompt)
        explanation = generate_response(prompt)
        print(explanation)
        return {"ai_explanation": explanation}
    

@router.get("/budgeting/ai-suggestions")
def budgeting_ai_suggestions():
    """
    Generate AI suggestions based on all budgeting scenarios in the database.
    """
    with get_session() as session:
        scenarios = session.query(BudgetingModel).all()
        if not scenarios:
            return {"ai_suggestions": ["No budgeting scenarios found."]}
        
    scenario_descriptions = []
    for s in scenarios:
        scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Monthly Net Income ₱{s.monthly_net_income}, "
                f"Housing Expense ₱{s.housing_expense}, "
                f"Food & Grocery Expense ₱{s.food_grocery_expense}, "
                f"Utilities Expense ₱{s.utilities_expense}, "
                f"Transportation Expense ₱{s.transportation_expense}, "
                f"Debt Payments Expense ₱{s.debt_payments_expense}, "
                f"Medical & Healthcare Expense ₱{s.medical_healthcare_expense}, "
                f"Education Expense ₱{s.education_expense}, "
                f"Household Supplies & Maintenance Expense ₱{s.household_supplies_maintenance_expense}, "
                f"Personal Care & Shopping Expense ₱{s.personal_care_shopping_expense}, "
                f"Entertainment & Recreation Expense ₱{s.entertainment_recreation_expense}, "
                f"Gifts & Donations Expense ₱{s.gifts_donations_expense}, "
                f"Savings & Investment Contribution ₱{s.savings_investment_contribution}"
            )
        

    prompt = (
        "You are a financial advisor. Below are multiple budgeting scenarios, each with their variables listed. "
        "Based on all scenarios, give 3 specific, practical suggestions to improve the user's budgeting outcomes. "
        "Be direct and actionable. Express all amounts in Philippine pesos (₱). "
        "Do not repeat the prompt or introduce the suggestions, just list them as:\n"
        "1. ...\n2. ...\n3. ...\n\n"
        + "\n".join(scenario_descriptions)
    )

    suggestions_text = generate_response(prompt)
    suggestions = [line.strip("- ").strip() for line in suggestions_text.split("\n") if line.strip()]
    return {"ai_suggestions": suggestions}


@router.get("/budgeting/summary")
def budgeting_summary():
    """
    Fetch all budgeting scenarios and generate an AI summary.
    """

    with get_session() as session:
        scenarios = session.query(BudgetingModel).all()
        if not scenarios:
            return {"summary": "No budgeting scenarios found."}
    
    scenario_descriptions = []
    for s in scenarios:
        scenario_descriptions.append(
            f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
            f"Monthly Net Income ₱{s.monthly_net_income}, "
            f"Housing Expense ₱{s.housing_expense}, "
            f"Food & Grocery Expense ₱{s.food_grocery_expense}, "
            f"Utilities Expense ₱{s.utilities_expense}, "
            f"Transportation Expense ₱{s.transportation_expense}, "
            f"Debt Payments Expense ₱{s.debt_payments_expense}, "
            f"Medical & Healthcare Expense ₱{s.medical_healthcare_expense}, "
            f"Education Expense ₱{s.education_expense}, "
            f"Household Supplies & Maintenance Expense ₱{s.household_supplies_maintenance_expense}, "
            f"Personal Care & Shopping Expense ₱{s.personal_care_shopping_expense}, "
            f"Entertainment & Recreation Expense ₱{s.entertainment_recreation_expense}, "
            f"Gifts & Donations Expense ₱{s.gifts_donations_expense}, "
            f"Savings & Investment Contribution ₱{s.savings_investment_contribution}"
        )

    prompt = (
            "You are a financial advisor. Below are several emergency fund scenarios. "
            "Write a short, clear summary that compares these scenarios. "
            "Do not introduce the summary or repeat the prompt. "
            "Reference each scenario by its number and title, mention the target amount and current savings, and highlight key differences. "
            "Keep the summary concise and do not list every variable. "
            "Express all amounts in Philippine pesos (₱). "
            "Start your summary immediately after this sentence.\n\n"
            + "\n".join(scenario_descriptions)
            + "For example: Scenario 1 (Basic): Target ₱60,000, Savings ₱20,000. Scenario 2 (Advanced): Target ₱120,000, Savings ₱50,000. The advanced scenario has higher expenses and savings, showing more progress toward a larger target."
        )

    print(prompt)
    summary = generate_response(prompt)
    return {"summary": summary}
    