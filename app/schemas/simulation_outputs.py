from pydantic import BaseModel
from typing import List, Any, Optional


class BudgetSimulationResponse(BaseModel):
    """Response model for budget simulation"""
    labels: List[int]                       
    values: List[float]                     
    summary: str                            
    math_explanation: Any                 
    ai_explanation: Optional[str] = None   
