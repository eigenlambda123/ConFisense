from fastapi import APIRouter, HTTPException, status
from app.schemas.simulation_inputs import EmergencyFundInput
from app.services.simulation_logic import simulate_emergency_fund
from app.models.log import SimulationLog
from app.db.session import get_session
from app.services.ai_explainer import generate_ai_explanation, generate_ai_suggestions
from fastapi import Body
from app.models.emergency_fund import EmergencyFund

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


@router.post("/simulate/emergency-fund/ai")
def emergency_fund_ai(data: dict = Body(...)):
    """
    Accepts simulation result and returns AI explanation and suggestions.
    """
    try:
        ai_explanation = generate_ai_explanation(
            scenario="emergency_fund",
            input_data=data.get("inputs_received", {}),
            output_data=data.get("data", {})
        )
        ai_suggestions = generate_ai_suggestions(
            scenario="emergency_fund",
            input_data=data.get("inputs_received", {}),
            output_data=data.get("data", {})
        )
        return {
            "ai_explanation": ai_explanation,
            "ai_suggestions": ai_suggestions
        }
    except Exception as e:
        return {
            "ai_explanation": "An AI explanation couldn't be generated at the moment.",
            "ai_suggestions": []
        }


@router.post("/emergency-fund/save")
def save_emergency_fund(data: EmergencyFundInput):
    with get_session() as session:
        scenario = EmergencyFund(
            scenario_title=data.scenario_title,
            monthly_expenses=data.monthly_expenses,
            months_of_expenses=data.months_of_expenses,
            current_emergency_savings=data.current_emergency_savings,
            monthly_savings=data.monthly_savings,
            annual_interest_rate_percent=data.annual_interest_rate_percent,
        )
        session.add(scenario)
        session.commit()
        return {"id": scenario.id, "message": "Scenario saved"}
    

@router.get("/emergency-fund/all")
def get_all_emergency_fund():
    with get_session() as session:
        scenarios = session.query(EmergencyFund).all()
        return [s.dict() for s in scenarios]
    

from app.services.ai_explainer import generate_peso_response

@router.get("/emergency-fund/summary")
def emergency_fund_summary():
    """
    Fetch all emergency fund scenarios and generate an AI summary.
    """
    with get_session() as session:
        scenarios = session.query(EmergencyFund).all()
        if not scenarios:
            return {"summary": "No emergency fund scenarios found."}

        # scenario descriptions
        scenario_descriptions = []
        for s in scenarios:
            scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Monthly Expenses: ₱{s.monthly_expenses}, "
                f"Months of Expenses: {s.months_of_expenses}, "
                f"Current Emergency Savings: ₱{s.current_emergency_savings}, "
                f"Monthly Savings: ₱{s.monthly_savings}, "
                f"Annual Interest Rate: {s.annual_interest_rate_percent}%"
            )

        # AI prompt
        prompt = (
            "Below are multiple emergency fund scenarios. For each, the variables are listed. "
            "Summarize and compare these scenarios in a short, clear paragraph. "
            "Highlight monetary differences, progress, and calculated target amounts. "
            "Express all amounts in Philippine pesos (₱).\n\n"
            + "\n".join(scenario_descriptions)
        )
        print(prompt)
        summary = generate_peso_response(prompt)
        return {"summary": summary}