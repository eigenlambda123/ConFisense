from fastapi import APIRouter, HTTPException, status
from app.schemas.simulation_inputs import EmergencyFundInput
from app.services.simulation_logic import simulate_emergency_fund
from app.models.log import SimulationLog
from app.db.session import get_session
from app.services.ai_explainer import generate_ai_explanation, generate_ai_suggestions

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


    try:
        # AI explanation generation
        ai_explanation = generate_ai_explanation(
            scenario="emergency_fund",
            input_data=data.model_dump(),
            output_data=result
        )
        # add ai explanation to the result
        result["ai_explanation"] = ai_explanation

        # AI suggestions generation
        ai_suggestions = generate_ai_suggestions(
            scenario="emergency_fund",
            input_data=data.model_dump(),
            output_data=result
        )
        # add ai suggestions to the result
        result["ai_suggestions"] = ai_suggestions

    except Exception as e:
        result["ai_explanation"] = "An AI explanation couldn't be generated at the moment."
        print(f"AI error: {e}")
    
    
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