from fastapi import APIRouter
from app.schemas.simulation_inputs import MajorPurchaseInput
from app.services.simulation_logic import simulate_major_purchase

router = APIRouter()

@router.post("/simulate-major-purchase")
def simulate_major_purchase_route(data: MajorPurchaseInput):
    
    return simulate_major_purchase(
        price=data.price,
        down_pct=data.down_pct,
        years_to_save=data.years_to_save,
        current_savings=data.current_savings,
        monthly_contrib=data.monthly_contrib,
        savings_return=data.savings_return,
        loan_rate=data.loan_rate,
        loan_term=data.loan_term
    )

    return {
        "labels": list(range(1, len(result["data"]) + 1)),
        "values": result["data"],
        "summary": result["summary"],
        "math_explanation": result["math_explanation"]
    }

    