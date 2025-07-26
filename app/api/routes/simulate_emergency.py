from fastapi import APIRouter
from app.schemas.simulation_inputs import EmergencyFundInput
from app.services.simulation_logic import simulate_emergency_fund

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

router = APIRouter()

@router.post("/simulate/emergency-fund")
def simulate_emergency_route(data: EmergencyFundInput):
    """
    POST endpoint to simulate emergency fund growth with user inputs:
    - target: Target amount for the emergency fund
    - monthly_contrib: Monthly contribution towards the fund
    - current_savings: Current savings amount
    """
    result = simulate_emergency_fund(
        target=data.target,
        monthly_contrib=data.monthly_contrib,
        current_savings=data.current_savings,
    )

    # labels: sequence numbers for each value in 'values' (currently just [1, 2])
    # values: [current_savings, target]
    # summary is the result of how long it will take to reach the target
    # math_explanation is the "show my math"
    response = {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "value_descriptions": ["Current Savings", "Target Amount"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }

    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="debt_management",
            input_data=data.model_dump(),
            output_data=result,
        )
        session.add(log)
        session.commit()

    return response
