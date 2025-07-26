from fastapi import APIRouter
from app.schemas.simulation_inputs import InvestmentInput
from app.services.simulation_logic import simulate_investing

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
    result = simulate_investing(
        initial=data.initial,
        monthly=data.monthly,
        return_rate=data.return_rate,
        years=data.years,
    )

    return {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }