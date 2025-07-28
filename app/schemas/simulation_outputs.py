from pydantic import BaseModel
from typing import List, Any, Optional


class SimulationResponse(BaseModel):
    """Base class for simulation responses"""
    labels: List[int]                       
    values: List[float]                     
    summary: str                            
    math_explanation: Any                 
    ai_explanation: Optional[str] = None   
