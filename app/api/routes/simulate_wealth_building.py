from fastapi import APIRouter
from requests import session
from app.schemas.wealth_building_schema import WealthBuildingInput
from app.services.simulation_logic import simulate_wealth_building 
from app.models.wealth_building_model import WealthBuildingModel
from app.services.ai_explainer import generate_response

from app.db.session import get_session
from fastapi import status
from fastapi import HTTPException

from sqlmodel import select
import json


router = APIRouter()


@router.post("/simulate/wealth-building")
def simulate_wealth_building_route(data: WealthBuildingInput):
    result = simulate_wealth_building(
        goal_name=data.goal_name,
        current_age=data.current_age,
        target_age=data.target_age,
        target_amount=data.target_amount,
        current_savings=data.current_savings,
        monthly_contribution=data.monthly_contribution,
        annual_contribution_increase=data.annual_contribution_increase,
        expected_annual_return=data.expected_annual_return,
        inflation_rate=data.inflation_rate,
        risk_profile=data.risk_profile,
        advisor_fee_percent=data.advisor_fee_percent
    )

    return result



@router.post("/wealth-building/save")
def save_wealth_building_to_db(data: WealthBuildingInput):
    with get_session() as session:
        scenario = WealthBuildingModel(
            goal_name=data.goal_name,
            current_age=data.current_age,
            target_age=data.target_age,
            target_amount=data.target_amount,
            current_savings=data.current_savings,
            monthly_contribution=data.monthly_contribution,
            annual_contribution_increase=data.annual_contribution_increase,
            expected_annual_return=data.expected_annual_return,
            inflation_rate=data.inflation_rate,
            risk_profile=data.risk_profile,
            advisor_fee_percent=data.advisor_fee_percent
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)
    return {"id": scenario.id}


@router.delete("/wealth-building/{scenario_id}")
def delete_wealth_building(scenario_id: int):
    with get_session() as session:
        scenario = session.get(WealthBuildingModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        session.delete(scenario)
        session.commit()
        return {"message": "Scenario deleted"}
    


@router.get("/wealth-building/ai-explanation")
def get_ai_explanation():
    with get_session() as session:
        scenario = session.exec(
            select(WealthBuildingModel).order_by(WealthBuildingModel.created_at.desc())
        ).first()
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No wealth building scenario found.")

        goal_name = scenario.goal_name
        current_age = scenario.current_age
        target_age = scenario.target_age
        target_amount = scenario.target_amount
        current_savings = scenario.current_savings
        monthly_contribution = scenario.monthly_contribution
        annual_contribution_increase = scenario.annual_contribution_increase
        expected_annual_return = scenario.expected_annual_return
        inflation_rate = scenario.inflation_rate
        risk_profile = scenario.risk_profile
        advisor_fee_percent = scenario.advisor_fee_percent

        chart_data = scenario.chart_data if hasattr(scenario, "chart_data") else []
        key_metrics = scenario.key_metrics if hasattr(scenario, "key_metrics") else {}

        # Calculate summary stats
        total_projected_value = key_metrics.get("total_projected_value", 0)
        inflation_adjusted_target = key_metrics.get("inflation_adjusted_target", 0)
        projected_shortfall = key_metrics.get("projected_shortfall", 0)
        percent_from_growth = key_metrics.get("percent_from_growth", 0)

        prompt = (
            "As an expert financial advisor, analyze the provided wealth building projection for a client. "
            "Focus on their goal, contributions, investment growth, and inflation-adjusted target. "
            "Identify the projected shortfall or surplus and the main factors driving the outcome. "
            "Explain the insights clearly, using client-relevant language, directly from the provided data.\n\n"
            f"Inputs:\n"
            f"Goal: {goal_name}\n"
            f"Client age: {current_age}, Target age: {target_age}\n"
            f"Target amount: ₱{target_amount:,.2f}\n"
            f"Current savings: ₱{current_savings:,.2f}\n"
            f"Monthly contribution: ₱{monthly_contribution:,.2f}, Annual increase: {annual_contribution_increase:.2%}\n"
            f"Expected annual return: {expected_annual_return:.2%}, Inflation rate: {inflation_rate:.2%}, Risk profile: {risk_profile}\n"
            f"Advisor fee: {advisor_fee_percent:.2f}%\n"
            f"Projected data: Total projected value: ₱{total_projected_value:,.2f}. "
            f"Inflation-adjusted target: ₱{inflation_adjusted_target:,.2f}. "
            f"Projected shortfall/surplus: ₱{projected_shortfall:,.2f}. "
            f"Percent from investment growth: {percent_from_growth:.2f}%."
        )

        explanation_text = generate_response(prompt)

        return {
            "status": "success",
            "data": {
                "explanation_text": explanation_text,
                "model_info": {
                    "model_name": "cohere-command",
                    "prompt_version": "v1.0.0"
                }
            }
        }
    


@router.get("/wealth-building/ai-suggestions")
def get_ai_suggestions():
    with get_session() as session:
        scenario = session.exec(
            select(WealthBuildingModel).order_by(WealthBuildingModel.created_at.desc())
        ).first()
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No wealth building scenario found.")

        # Extract key stats for prompt context
        goal_name = scenario.goal_name
        current_age = scenario.current_age
        target_age = scenario.target_age
        target_amount = scenario.target_amount
        current_savings = scenario.current_savings
        monthly_contribution = scenario.monthly_contribution
        annual_contribution_increase = scenario.annual_contribution_increase
        expected_annual_return = scenario.expected_annual_return
        inflation_rate = scenario.inflation_rate
        risk_profile = scenario.risk_profile
        advisor_fee_percent = scenario.advisor_fee_percent

        key_metrics = scenario.key_metrics if hasattr(scenario, "key_metrics") else {}

        total_projected_value = key_metrics.get("total_projected_value", 0)
        inflation_adjusted_target = key_metrics.get("inflation_adjusted_target", 0)
        projected_shortfall = key_metrics.get("projected_shortfall", 0)
        percent_from_growth = key_metrics.get("percent_from_growth", 0)

        # Get the latest AI insight
        insight_prompt = (
            "As an expert financial advisor, analyze the provided wealth building projection for a client. "
            "Focus on their goal, contributions, investment growth, and inflation-adjusted target. "
            "Identify the projected shortfall or surplus and the main factors driving the outcome. "
            "Explain the insights clearly, using client-relevant language, directly from the provided data.\n\n"
            f"Inputs:\n"
            f"Goal: {goal_name}\n"
            f"Client age: {current_age}, Target age: {target_age}\n"
            f"Target amount: ₱{target_amount:,.2f}\n"
            f"Current savings: ₱{current_savings:,.2f}\n"
            f"Monthly contribution: ₱{monthly_contribution:,.2f}, Annual increase: {annual_contribution_increase:.2%}\n"
            f"Expected annual return: {expected_annual_return:.2%}, Inflation rate: {inflation_rate:.2%}, Risk profile: {risk_profile}\n"
            f"Advisor fee: {advisor_fee_percent:.2f}%\n"
            f"Projected data: Total projected value: ₱{total_projected_value:,.2f}. "
            f"Inflation-adjusted target: ₱{inflation_adjusted_target:,.2f}. "
            f"Projected shortfall/surplus: ₱{projected_shortfall:,.2f}. "
            f"Percent from investment growth: {percent_from_growth:.2f}%."
        )
        ai_insight = generate_response(insight_prompt)

        # Build suggestion prompt, instructing the AI to return JSON
        suggestion_prompt = (
            "Based on the wealth building insights and the client's goal, recommend actionable, next steps for this client to optimize their contributions, investment strategy, and probability of reaching their goal. "
            "Suggestions should be specific to financial planning and investment options.\n\n"
            "Return your answer as a JSON array of objects with keys: priority, title, description.\n"
            f"Inputs:\n"
            f"Insight: {ai_insight}\n"
            f"Projected data: Projected shortfall/surplus: ₱{projected_shortfall:,.2f}. "
            f"Percent from investment growth: {percent_from_growth:.2f}%.\n"
            f"Goal: {goal_name}, Target amount: ₱{target_amount:,.2f}, Target age: {target_age}."
        )

        raw_suggestions = generate_response(suggestion_prompt)

        # Try to parse the AI output as JSON
        try:
            actionable_recommendations = json.loads(raw_suggestions)
        except Exception:
            actionable_recommendations = [{
                "priority": "Info",
                "title": "AI Suggestion",
                "description": raw_suggestions
            }]

        return {
            "status": "success",
            "data": {
                "actionable_recommendations": actionable_recommendations,
                "model_info": {
                    "model_name": "cohere-command",
                    "prompt_version": "v1.0.0"
                }
            }
        }
    

