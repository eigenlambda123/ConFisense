from fastapi import APIRouter
from app.schemas.simulation_inputs import BudgetInput
from app.schemas.simulation_outputs import SimulationResponse
from app.services.simulation_logic import simulate_budgeting
import json

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# Exception imports
from fastapi import HTTPException
from fastapi import status

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation


router = APIRouter()

@router.post("/simulate/budgeting", response_model=SimulationResponse)
def simulate_budgeting_route(data: BudgetInput):
    """
    POST endpoint to simulate budgeting with user inputs:
    - income: Monthly income for the budget simulation
    - fixed_expenses: Monthly fixed expenses for the budget simulation
    - discretionary_pct: Percentage of income allocated to discretionary spending
    - target_savings: Target savings amount for the budget simulation
    """

    # Exception handling for input validation
    if data.income <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Income must be greater than zero")
    
    if data.fixed_expenses < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Fixed expenses must be non-negative")
    
    if data.discretionary_pct < 0 or data.discretionary_pct > 100:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Discretionary percentage must be between 0 and 100")
    
    if data.income < 0 or data.fixed_expenses < 0 or data.target_savings < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Income, fixed expenses, and target savings must be non-negative")


    result = simulate_budgeting(
        income=data.income,
        fixed_expenses=data.fixed_expenses,
        discretionary_pct=data.discretionary_pct,
        target_savings=data.target_savings,
    )


    # Generate AI explanation for the budgeting simulation
    try:
        ai_explanation = generate_ai_explanation(
            scenario="budgeting",
            input_data=data.model_dump(),
            output_data=result
        )

    except Exception as e:
        ai_explanation = "An AI explanation couldn't be generated at the moment."
        # Log the error
        print(f"AI error: {e}")


    # response data 
    values = list(result["data"].values())
    math_explanation = result["math_explanation"]

    response = SimulationResponse(
        labels=list(range(1, len(values) + 1)),
        values=values,
        summary=result["summary"],
        math_explanation=math_explanation,
        ai_explanation=ai_explanation,
    )


    # Log the simulation inputs and outputs to Database
    with get_session() as session:
        log = SimulationLog(
            scenario="budgeting",
            input_data=data.model_dump(),
            output_data=response.model_dump(),
        )
        session.add(log)
        session.commit()

    return response
