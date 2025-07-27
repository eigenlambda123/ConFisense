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

    # Exception handling for input validation
    if any(x < 0 for x in [data.current_savings, data.monthly_contrib, data.return_rate, data.inflation_rate]):
        raise ValueError("All inputs must be non-negative values")
    if data.monthly_contrib > data.current_savings:
        raise ValueError("Monthly contribution cannot exceed current savings")
    if data.monthly_contrib == 0 and data.current_savings == 0:
        raise ValueError("At least one of current savings or monthly contribution must be greater than zero")
    if not (0 <= data.inflation_rate <= 100):
        raise ValueError("Inflation rate must be between 0 and 100")
    if not (0 <= data.return_rate <= 100):
        raise ValueError("Return rate must be between 0 and 100")
    if getattr(data, "years", 0) <= 0 or getattr(data, "years_to_save", 0) <= 0:
        raise ValueError("Years to save must be greater than zero")
    if getattr(data, "today_cost", 0) <= 0:
        raise ValueError("Today's cost must be greater than zero")

    

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
    try:
        ai_explanation = generate_ai_explanation(
            scenario="education_fund",
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
            scenario="education_fund",
            input_data=data.model_dump(),
            output_data=response,
        )
        session.add(log)
        session.commit()

    return response