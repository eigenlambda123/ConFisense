from fastapi import APIRouter
from app.schemas.simulation_inputs import BudgetInput
from app.schemas.simulation_outputs import SimulationResponse
from app.services.simulation_logic import simulate_budgeting
from app.models.budgeting import BudgetingModel

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# Exception imports
from fastapi import HTTPException
from fastapi import status

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation


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