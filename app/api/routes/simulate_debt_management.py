from fastapi import APIRouter
from requests import session
from app.schemas.debt_management_schema import DebtManagementInput
from app.services.simulation_logic import simulate_debt_management 
from app.models.debt_management_model import DebtManagementModel
from app.services.ai_explainer import generate_response

from app.db.session import get_session
from fastapi import status
from fastapi import HTTPException

from sqlmodel import select
import json


router = APIRouter()


@router.post("/simulate/debt-management")
def simulate_debt_management_route(data: DebtManagementInput):
    result = simulate_debt_management(
        scenario_type=data.scenario_type,
        user_type=data.user_type,
        projection_period=data.projection_period,
        loans=[loan.model_dump() for loan in data.loans],
        business_financials=data.business_financials.model_dump(),
        growth_needs=data.growth_needs.model_dump(),
        proposed_financing=data.proposed_financing.model_dump(),
        reinvestment_rate=data.reinvestment_rate
    )
    return result


@router.post("/debt-management/save")
def save_debt_management_to_db(data: DebtManagementInput):
    with get_session() as session:
        scenario = DebtManagementModel(
            scenario_type=data.scenario_type,
            user_type=data.user_type,
            projection_period=data.projection_period,
            loans=[loan.model_dump() for loan in data.loans],
            business_financials=data.business_financials.model_dump(),
            growth_needs=data.growth_needs.model_dump(),
            proposed_financing=data.proposed_financing.model_dump(),
            reinvestment_rate=data.reinvestment_rate
        )
        session.add(scenario)
        session.commit()
        session.refresh(scenario)
    return {"id": scenario.id}


@router.delete("/debt-management/{scenario_id}")
def delete_debt_management(scenario_id: int):
    with get_session() as session:
        scenario = session.get(DebtManagementModel, scenario_id)
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scenario not found")

        session.delete(scenario)
        session.commit()
        return {"message": "Scenario deleted"}
    


@router.get("/debt-management/ai-explanation")
def get_ai_explanation():
    with get_session() as session:
        scenario = session.exec(
            select(DebtManagementModel).order_by(DebtManagementModel.created_at.desc())
        ).first()
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No debt management scenario found.")

        # Extract key stats for prompt context
        business_financials = scenario.business_financials
        growth_needs = scenario.growth_needs
        chart_data = scenario.chart_data if hasattr(scenario, "chart_data") else []

        avg_monthly_revenue = business_financials.get("avg_monthly_revenue", 0)
        industry = business_financials.get("industry", "N/A")
        capital_required = growth_needs.get("capital_required", 0)
        expected_roi = growth_needs.get("expected_roi", "N/A")

        # Calculate summary stats from chart_data
        total_net_cash_flow_period = sum([c.get("net_operating_cash_flow", 0) for c in chart_data])
        lowest_cash_value = min([c.get("net_cash_position", 0) for c in chart_data]) if chart_data else 0
        lowest_cash_month_idx = (
            [c.get("period", 0) for c in chart_data if c.get("net_cash_position", 0) == lowest_cash_value][0]
            if chart_data and lowest_cash_value else "N/A"
        )
        # Identify primary cash outflow
        significant_drain_name = "operating_expenses"
        max_outflow = 0
        for c in chart_data:
            for key in ["operating_expenses", "loan_principal_payments", "loan_interest_payments"]:
                if c.get(key, 0) > max_outflow:
                    max_outflow = c.get(key, 0)
                    significant_drain_name = key

        prompt = (
            "As an expert financial advisor for Filipino MSMEs, analyze the provided business cash flow projection. "
            "Focus on how revenues, operating expenses, and debt payments impact the net cash position. "
            "Identify the most critical period for cash flow and the primary factor causing it. "
            "Explain the insights clearly, using business-relevant language, directly from the provided data.\n\n"
            f"Inputs:\n"
            f"Business profile: Avg monthly revenue: ₱{avg_monthly_revenue:,.2f}, Industry: {industry}\n"
            f"Projected data: Total projected net cash flow over the period: ₱{total_net_cash_flow_period:,.2f}. "
            f"Lowest projected cash balance: ₱{lowest_cash_value:,.2f} in Month {lowest_cash_month_idx}. "
            f"Primary cash outflow identified: {significant_drain_name.replace('_', ' ').title()}.\n"
            f"Growth plan: Capital required: ₱{capital_required:,.2f}, Expected ROI: {expected_roi}."
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
    


@router.get("/debt-management/ai-suggestions")
def get_ai_suggestions():
    with get_session() as session:
        scenario = session.exec(
            select(DebtManagementModel).order_by(DebtManagementModel.created_at.desc())
        ).first()
        if not scenario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No debt management scenario found.")

        # Extract key stats for prompt context
        business_financials = scenario.business_financials
        growth_needs = scenario.growth_needs
        chart_data = scenario.chart_data if hasattr(scenario, "chart_data") else []

        avg_monthly_revenue = business_financials.get("avg_monthly_revenue", 0)
        capital_required = growth_needs.get("capital_required", 0)

        # Calculate summary stats from chart_data
        lowest_cash_value = min([c.get("net_cash_position", 0) for c in chart_data]) if chart_data else 0
        lowest_cash_month_idx = (
            [c.get("period", 0) for c in chart_data if c.get("net_cash_position", 0) == lowest_cash_value][0]
            if chart_data and lowest_cash_value else "N/A"
        )

        # Get the latest AI insight
        insight_prompt = (
            "As an expert financial advisor for Filipino MSMEs, analyze the provided business cash flow projection. "
            "Focus on how revenues, operating expenses, and debt payments impact the net cash position. "
            "Identify the most critical period for cash flow and the primary factor causing it. "
            "Explain the insights clearly, using business-relevant language, directly from the provided data.\n\n"
            f"Inputs:\n"
            f"Business profile: Avg monthly revenue: ₱{avg_monthly_revenue:,.2f}\n"
            f"Projected data: Lowest projected cash balance: ₱{lowest_cash_value:,.2f} in Month {lowest_cash_month_idx}.\n"
            f"Growth plan: Capital required: ₱{capital_required:,.2f}."
        )
        ai_insight = generate_response(insight_prompt)

        # Build suggestion prompt, instructing the AI to return JSON
        suggestion_prompt = (
            "Based on the cash flow insights and the planned growth initiative, recommend actionable, next steps for this Filipino MSME to optimize their debt and capital structure and ensure sufficient liquidity. Suggestions should be specific to business operations and financing.\n\n"
            "Return your answer as a JSON array of objects with keys: priority, title, description.\n"
            f"Inputs:\n"
            f"Insight: {ai_insight}\n"
            f"Projected data: AI suggests improving cash position by ₱{lowest_cash_value:,.2f} by addressing the Month {lowest_cash_month_idx} cash crunch.\n"
            f"Planned growth: Capital required: ₱{capital_required:,.2f}."
        )

        raw_suggestions = generate_response(suggestion_prompt)

        # Try to parse the AI output as JSON
        try:
            actionable_recommendations = json.loads(raw_suggestions)
        except Exception:
            # fallback: wrap the raw text in a single recommendation
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