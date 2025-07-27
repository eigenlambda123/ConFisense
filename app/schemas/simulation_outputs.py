from pydantic import BaseModel
from typing import List, Union, Optional


class BudgetSimulationResponse(BaseModel):
    """Response model for budget simulation"""
    labels: List[int]                       
    values: List[float]                     
    summary: str                            
    math_explanation: str                   
    ai_explanation: Optional[str] = None   
