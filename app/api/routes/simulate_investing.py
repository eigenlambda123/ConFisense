from fastapi import APIRouter
from app.schemas.simulation_inputs import InvestmentInput
from app.services.simulation_logic import simulate_investing

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation

router = APIRouter()

@router.post("/simulate/investing")
def simulate_investing_route(data: InvestmentInput):
    """
    POST endpoint to simulate investing with user inputs:
    - initial: Initial investment amount
    - monthly: Monthly contribution to the investment
    - return_rate: Expected annual return rate on the investment
    - years: Number of years to simulate the investment
    """

    if any(x < 0 for x in [data.initial, data.monthly, data.return_rate, data.years]):
        raise ValueError("All inputs must be non-negative values")
    if data.monthly > data.initial:
        raise ValueError("Monthly investment cannot exceed initial investment")
    if data.monthly == 0 and data.initial == 0:
        raise ValueError("At least one of initial or monthly investment must be greater than zero")
    
    
    result = simulate_investing(
        initial=data.initial,
        monthly=data.monthly,
        return_rate=data.return_rate,
        years=data.years,
    )

    response = {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }

    # Generate AI explanation for the investment simulation
    try:
        ai_explanation = generate_ai_explanation(
            scenario="investment",
            input_data=data.model_dump(),
            output_data=response
        )
        response["ai_explanation"] = ai_explanation

    except Exception as e:
        ai_explanation = "An AI explanation couldn't be generated at the moment."
        # Log the error
        print(f"AI error: {e}")


    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="investment",
            input_data=data.model_dump(),
            output_data=response,
        )
        session.add(log)
        session.commit()

    return response
