from fastapi import APIRouter
from app.schemas.simulation_inputs import EmergencyFundInput
from app.schemas.simulation_outputs import SimulationResponse
from app.services.simulation_logic import simulate_emergency_fund

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation

router = APIRouter()

@router.post("/simulate/emergency-fund", response_model=SimulationResponse)
def simulate_emergency_route(data: EmergencyFundInput):
    """
    POST endpoint to simulate emergency fund growth with user inputs:
    - target: Target amount for the emergency fund
    - monthly_contrib: Monthly contribution towards the fund
    - current_savings: Current savings amount
    """

    # TODO: Add exception handling for input validation


    result = simulate_emergency_fund(
        target=data.target,
        monthly_contrib=data.monthly_contrib,
        current_savings=data.current_savings,
    )


    # Generate AI explanation for the emergency fund simulation
    try:
        ai_explanation = generate_ai_explanation(
            scenario="emergency_fund",
            input_data=data.model_dump(),
            output_data=result
        )

    except Exception as e:
        ai_explanation = "An AI explanation couldn't be generated at the moment."
        # Log the error
        print(f"AI error: {e}")


    # response data
    response = SimulationResponse(
        labels=list(range(1, len(result["data"]) + 1)),
        values=result["data"],
        summary=result["summary"],
        math_explanation=result["math_explanation"],
        ai_explanation=ai_explanation
    )


    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="emergency_fund",
            input_data=data.model_dump(),
            output_data=response.model_dump()
        )
        session.add(log)
        session.commit()

    return response
