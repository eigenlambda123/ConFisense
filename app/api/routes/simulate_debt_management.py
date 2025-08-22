from fastapi import APIRouter
from requests import session
from app.schemas.debt_management_schema import DebtManagementInput
from app.services.simulation_logic import simulate_debt_management 
from app.models.debt_management_model import DebtManagementModel
from app.services.ai_explainer import generate_response

from app.db.session import get_session
from fastapi import status
from fastapi import HTTPException

from sqlmodel import select


router = APIRouter()


@router.post("/simulate/debt-management")
def simulate_debt_management_route(data: DebtManagementInput):
    result = simulate_debt_management(
        scenario_type=data.scenario_type,
        user_type=data.user_type,
        projection_period=data.projection_period,
        loans=[loan.model_dump() for loan in data.loans],
        business_financials=data.business_financials.model_dump(),
        growth_needs=data.growth_needs.model_dump(),
        proposed_financing=data.proposed_financing.model_dump(),
        reinvestment_rate=data.reinvestment_rate
    )
    return result


@router.post("/debt-management/save")
def save_debt_management_to_db(data: DebtManagementInput):
    with get_session() as session:
        scenario = DebtManagementModel(
            scenario_type=data.scenario_type,
            user_type=data.user_type,
            projection_period=data.projection_period,
            loans=[loan.model_dump() for loan in data.loans],
            business_financials=data.business_financials.model_dump(),
            growth_needs=data.growth_needs.model_dump(),
            proposed_financing=data.proposed_financing.model_dump(),
            reinvestment_rate=data.reinvestment_rate
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)
    return {"id": scenario.id}


@router.delete("/debt-management/{scenario_id}")
def delete_debt_management(scenario_id: int):
    with get_session() as session:
        scenario = session.get(DebtManagementModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        session.delete(scenario)
        session.commit()
        return {"message": "Scenario deleted"}