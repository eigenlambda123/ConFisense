from fastapi import APIRouter
from requests import session
from app.schemas.wealth_building_schema import WealthBuildingInput
from app.services.simulation_logic import simulate_wealth_building 
from app.models.wealth_building_model import WealthBuildingModel
from app.services.ai_explainer import generate_response

from app.db.session import get_session
from fastapi import status
from fastapi import HTTPException

from sqlmodel import select
import json


router = APIRouter()


@router.post("/simulate/wealth-building")
def simulate_wealth_building_route(data: WealthBuildingInput):
    result = simulate_wealth_building(
        goal_name=data.goal_name,
        current_age=data.current_age,
        target_age=data.target_age,
        target_amount=data.target_amount,
        current_savings=data.current_savings,
        monthly_contribution=data.monthly_contribution,
        annual_contribution_increase=data.annual_contribution_increase,
        expected_annual_return=data.expected_annual_return,
        inflation_rate=data.inflation_rate,
        risk_profile=data.risk_profile,
        advisor_fee_percent=data.advisor_fee_percent
    )

    return result



@router.post("/wealth-building/save")
def save_wealth_building_to_db(data: WealthBuildingInput):
    with get_session() as session:
        scenario = WealthBuildingModel(
            goal_name=data.goal_name,
            current_age=data.current_age,
            target_age=data.target_age,
            target_amount=data.target_amount,
            current_savings=data.current_savings,
            monthly_contribution=data.monthly_contribution,
            annual_contribution_increase=data.annual_contribution_increase,
            expected_annual_return=data.expected_annual_return,
            inflation_rate=data.inflation_rate,
            risk_profile=data.risk_profile,
            advisor_fee_percent=data.advisor_fee_percent
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)
    return {"id": scenario.id}
