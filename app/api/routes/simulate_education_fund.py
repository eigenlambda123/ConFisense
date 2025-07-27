from fastapi import APIRouter
from app.schemas.simulation_inputs import EducationFundInput
from app.services.simulation_logic import simulate_education_fund

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation

router = APIRouter()

@router.post("/simulate/education-fund")
def simulate_education_fund_route(data: EducationFundInput):
    """
    POST endpoint to simulate education fund savings with user inputs:
    - current_savings: Current amount saved for education
    - monthly_contribution: Monthly contribution towards the education fund
    - target_amount: Target amount needed for education
    - years_to_save: Number of years to save for education
    """

    # catch division zero error and other invalid inputs
    if data.years <= 0 or data.monthly_contrib < 0 or data.current_savings < 0:
        raise ValueError("Invalid input values for education fund simulation")

    result = simulate_education_fund(
        today_cost=data.today_cost,
        years=data.years,
        current_savings=data.current_savings,
        monthly_contrib=data.monthly_contrib,
        return_rate=data.return_rate,
        inflation_rate=data.inflation_rate
    )

    response = {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }


    # Generate AI explanation for the education fund simulation
    ai_explanation = generate_ai_explanation(
        scenario="education_fund",
        input_data=data.model_dump(),
        output_data=response
    )
    response["ai_explanation"] = ai_explanation



    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="education_fund",
            input_data=data.model_dump(),
            output_data=response,
        )
        session.add(log)
        session.commit()

    return response