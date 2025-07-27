from fastapi import APIRouter
from app.schemas.simulation_inputs import BudgetInput
from app.services.simulation_logic import simulate_budgeting

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# Exception imports
from fastapi import HTTPException
from fastapi import status

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation


router = APIRouter()

@router.post("/simulate/budgeting")
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

    # TODO: instead of using dict as a response, create a Pydantic model for the response
    response = {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }

    # Generate AI explanation for the budgeting simulation
    try:
        ai_explanation = generate_ai_explanation(
            scenario="budgeting",
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
            scenario="budgeting",
            input_data=data.model_dump(),
            output_data=response,
        )
        session.add(log)
        session.commit()

    return response
