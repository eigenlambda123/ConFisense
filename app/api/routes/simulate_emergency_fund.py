from fastapi import APIRouter, HTTPException, status
from app.schemas.simulation_inputs import EmergencyFundInput
from app.services.simulation_logic import simulate_emergency_fund
from app.models.log import SimulationLog
from app.db.session import get_session
from app.services.ai_explainer import generate_ai_explanation, generate_ai_suggestions
from fastapi import Body
from app.models.emergency_fund import EmergencyFund

router = APIRouter()

@router.post("/simulate/emergency-fund")
def simulate_emergency_fund_route(data: EmergencyFundInput):

    if data.monthly_expenses < 0 or data.months_of_expenses <= 0 or data.current_emergency_savings < 0 or data.monthly_savings < 0 or data.annual_interest_rate_percent < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="All inputs must be non-negative and months > 0.")


    result = simulate_emergency_fund(
        monthly_expenses=data.monthly_expenses,
        months_of_expenses=data.months_of_expenses,
        current_emergency_savings=data.current_emergency_savings,
        monthly_savings=data.monthly_savings,
        annual_interest_rate_percent=data.annual_interest_rate_percent,
    )
    
    
    # Log the simulation
    with get_session() as session:
        log = SimulationLog(
            scenario="emergency_fund",
            input_data=data.model_dump(),
            output_data=result
        )
        session.add(log)
        session.commit()

    return result


@router.post("/simulate/emergency-fund/ai")
def emergency_fund_ai(data: dict = Body(...)):
    """
    Accepts simulation result and returns AI explanation and suggestions.
    """
    try:
        ai_explanation = generate_ai_explanation(
            scenario="emergency_fund",
            input_data=data.get("inputs_received", {}),
            output_data=data.get("data", {})
        )
        ai_suggestions = generate_ai_suggestions(
            scenario="emergency_fund",
            input_data=data.get("inputs_received", {}),
            output_data=data.get("data", {})
        )
        return {
            "ai_explanation": ai_explanation,
            "ai_suggestions": ai_suggestions
        }
    except Exception as e:
        return {
            "ai_explanation": "An AI explanation couldn't be generated at the moment.",
            "ai_suggestions": []
        }


@router.post("/emergency-fund/save")
def save_emergency_fund(data: EmergencyFundInput):
    with get_session() as session:
        scenario = EmergencyFund(
            scenario_title=data.scenario_title,
            monthly_expenses=data.monthly_expenses,
            months_of_expenses=data.months_of_expenses,
            current_emergency_savings=data.current_emergency_savings,
            monthly_savings=data.monthly_savings,
            annual_interest_rate_percent=data.annual_interest_rate_percent,
        )
        session.add(scenario)
        session.commit()
        return {"id": scenario.id, "message": "Scenario saved"}
    