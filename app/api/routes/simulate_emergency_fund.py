from fastapi import APIRouter, HTTPException, status
from app.schemas.simulation_inputs import EmergencyFundInput
from app.services.simulation_logic import simulate_emergency_fund
from app.models.log import SimulationLog
from app.db.session import get_session
from app.models.emergency_fund import EmergencyFundModel
from app.services.ai_explainer import generate_response, count_tokens


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


# @router.post("/simulate/emergency-fund/ai")
# def emergency_fund_ai(data: dict = Body(...)):
#     """
#     Accepts simulation result and returns AI explanation and suggestions.
#     """
#     try:
#         ai_explanation = generate_ai_explanation(
#             scenario="emergency_fund",
#             input_data=data.get("inputs_received", {}),
#             output_data=data.get("data", {})
#         )
#         ai_suggestions = generate_ai_suggestions(
#             scenario="emergency_fund",
#             input_data=data.get("inputs_received", {}),
#             output_data=data.get("data", {})
#         )
#         return {
#             "ai_explanation": ai_explanation,
#             "ai_suggestions": ai_suggestions
#         }
#     except Exception as e:
#         return {
#             "ai_explanation": "An AI explanation couldn't be generated at the moment.",
#             "ai_suggestions": []
#         }


@router.post("/emergency-fund/save")
def save_emergency_fund(data: EmergencyFundInput):
    with get_session() as session:
        scenario = EmergencyFundModel(
            scenario_title=data.scenario_title,
            monthly_expenses=data.monthly_expenses,
            months_of_expenses=data.months_of_expenses,
            current_emergency_savings=data.current_emergency_savings,
            monthly_savings=data.monthly_savings,
            annual_interest_rate_percent=data.annual_interest_rate_percent,
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)
        return {"id": scenario.id, "message": "Scenario saved"}
    

@router.get("/emergency-fund/all")
def get_all_emergency_fund():
    with get_session() as session:
        scenarios = session.query(EmergencyFundModel).all()
        return [s.dict() for s in scenarios]
    

@router.delete("/emergency-fund/{scenario_id}")
def delete_emergency_fund_scenario(scenario_id: int):
    with get_session() as session:
        scenario = session.get(EmergencyFundModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")
        session.delete(scenario)
        session.commit()
        session.refresh(scenario)
        return {"message": "Scenario deleted"}
    


@router.get("/emergency-fund/ai-explanation")
def emergency_fund_ai_explanation():
    """
    Generate an AI explanation based on all emergency fund scenarios in the database.
    """
    with get_session() as session:
        scenarios = session.query(EmergencyFundModel).all()
        if not scenarios:
            return {"ai_explanation": "No emergency fund scenarios found."}

        scenario_descriptions = []
        for s in scenarios:
            scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Target ₱{s.monthly_expenses * s.months_of_expenses}, "
                f"Current Savings ₱{s.current_emergency_savings}, "
                f"Monthly Savings ₱{s.monthly_savings}, "
                f"Months of Expenses {s.months_of_expenses}, "
                f"Annual Interest Rate {s.annual_interest_rate_percent}%"
            )

        prompt = (
            "Compare the emergency fund scenarios below. "
            "For each, mention the scenario number and title, target amount, and current savings. "
            "Highlight the main differences. Keep it concise and clear. "
            "Express all amounts in Philippine pesos (₱). "
            "Do not introduce the summary or repeat the prompt. "
            "Start your summary immediately after this sentence.\n\n"
            + "\n".join(scenario_descriptions)
            + "\nExample: Scenario 1 (Basic): Target ₱60,000, Savings ₱20,000. Scenario 2 (Advanced): Target ₱120,000, Savings ₱50,000. The advanced scenario has higher expenses and savings, showing more progress toward a larger target."
        )
        print(prompt)
        print("Prompt length:", len(prompt))
        print("Prompt tokens:", count_tokens(prompt))
        explanation = generate_response(prompt)
        print(explanation)
        return {"ai_explanation": explanation}



@router.get("/emergency-fund/ai-suggestions")
def emergency_fund_ai_suggestions():
    """
    Generate AI suggestions based on all emergency fund scenarios in the database.
    """
    with get_session() as session:
        scenarios = session.query(EmergencyFundModel).all()
        if not scenarios:
            return {"ai_suggestions": ["No emergency fund scenarios found."]}

        scenario_descriptions = []
        for s in scenarios:
            scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Monthly Expenses ₱{s.monthly_expenses}, "
                f"Months of Expenses {s.months_of_expenses}, "
                f"Current Emergency Savings ₱{s.current_emergency_savings}, "
                f"Monthly Savings ₱{s.monthly_savings}, "
                f"Annual Interest Rate {s.annual_interest_rate_percent}%, "
                f"Target ₱{s.monthly_expenses * s.months_of_expenses}, "
                f"Current Savings ₱{s.current_emergency_savings}"
            )

        prompt = (
            "You are a financial advisor. Below are multiple emergency fund scenarios, each with their variables listed. "
            "Based on all scenarios, give 3 specific, practical suggestions to improve the user's emergency fund outcomes. "
            "Be direct and actionable. Express all amounts in Philippine pesos (₱). "
            "Do not repeat the prompt or introduce the suggestions, just list them as:\n"
            "1. ...\n2. ...\n3. ...\n\n"
            + "\n".join(scenario_descriptions)
        )

        suggestions_text = generate_response(prompt)
        # Optionally, split suggestions into a list
        suggestions = [line.strip("- ").strip() for line in suggestions_text.split("\n") if line.strip()]
        return {"ai_suggestions": suggestions}
    

@router.get("/emergency-fund/summary")
def emergency_fund_summary():
    """
    Fetch all emergency fund scenarios and generate an AI summary.
    """
    with get_session() as session:
        scenarios = session.query(EmergencyFundModel).all()
        if not scenarios:
            return {"summary": "No emergency fund scenarios found."}

        # scenario descriptions (can be more detailed)
        scenario_descriptions = []
        for s in scenarios:
            scenario_descriptions.append(
                f"Scenario {s.id} ({s.scenario_title or 'Untitled'}): "
                f"Monthly Expenses ₱{s.monthly_expenses}, "
                f"Months of Expenses {s.months_of_expenses}, "
                f"Current Emergency Savings ₱{s.current_emergency_savings}, "
                f"Monthly Savings ₱{s.monthly_savings}, "
                f"Annual Interest Rate {s.annual_interest_rate_percent}%, "
                f"Target ₱{s.monthly_expenses * s.months_of_expenses}, "
                f"Current Savings ₱{s.current_emergency_savings}"
            )

        prompt = (
            "You are a financial advisor. Below are several emergency fund scenarios. "
            "Write a short, clear summary that compares these scenarios. "
            "Do not introduce the summary or repeat the prompt. "
            "Reference each scenario by its number and title, mention the target amount and current savings, and highlight key differences. "
            "Keep the summary concise and do not list every variable. "
            "Express all amounts in Philippine pesos (₱). "
            "Start your summary immediately after this sentence.\n\n"
            + "\n".join(scenario_descriptions)
            + "For example: Scenario 1 (Basic): Target ₱60,000, Savings ₱20,000. Scenario 2 (Advanced): Target ₱120,000, Savings ₱50,000. The advanced scenario has higher expenses and savings, showing more progress toward a larger target."
        )

        print(prompt)
        print("Prompt length:", len(prompt))
        print("Prompt tokens:", count_tokens(prompt))
        summary = generate_response(prompt)
        return {"summary": summary}
    