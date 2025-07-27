from fastapi import APIRouter
from app.schemas.simulation_inputs import DebtManagementInput
from app.services.simulation_logic import simulate_debt_management

# logging imports
from app.models.log import SimulationLog
from app.db.session import get_session

# Exception imports
from fastapi import HTTPException
from fastapi import status

# ai explaination imports
from app.services.ai_explainer import generate_ai_explanation

router = APIRouter()

@router.post("/simulate/debt-management")
def simulate_debt_management_route(data: DebtManagementInput):
    """
    POST endpoint to simulate debt management with user inputs:
    - debt: Total debt amount for the debt management simulation
    - monthly_payment: Monthly payment towards the debt
    - interest_rate: Annual interest rate on the debt
    - extra_payment: Extra payment towards the debt (if any)
    """
    # Exception handling for input validation
    checks = [
        (data.debt < 0, "Debt must be non-negative"),
        (data.monthly_payment < 0, "Monthly payment must be non-negative"),
        (data.interest_rate < 0, "Interest rate must be non-negative"),
        (data.extra_payment < 0, "Extra payment must be non-negative"),
        (data.monthly_payment > data.debt, "Monthly payment cannot exceed total debt"),
        (data.extra_payment > data.monthly_payment, "Extra payment cannot exceed monthly payment"),
        (data.debt == 0 and data.monthly_payment == 0, "At least one of debt or monthly payment must be greater than zero"),
        (data.interest_rate > 100, "Interest rate must be between 0 and 100"),
        (data.extra_payment > 0 and data.monthly_payment == 0, "Monthly payment must be greater than zero if extra payment is made"),
    ]
    for condition, message in checks:
        if condition:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)


    result = simulate_debt_management(
        debt=data.debt,
        monthly_payment=data.monthly_payment,
        interest_rate=data.interest_rate,
        extra_payment=data.extra_payment,
    )

    response = {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }


    # Generate AI explanation for the debt management simulation
    try:
        ai_explanation = generate_ai_explanation(
            scenario="debt_management",
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
            scenario="debt_management",
            input_data=data.model_dump(),
            output_data=response,
        )
        session.add(log)
        session.commit()

    return response
