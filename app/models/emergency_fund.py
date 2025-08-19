from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class EmergencyFundModel(SQLModel, table=True):
    """
    Emergency Fund Model for the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_title: str
    monthly_expenses: float
    months_of_expenses: int
    current_emergency_savings: float
    monthly_savings: float
    annual_interest_rate_percent: float
    created_at: datetime = Field(default_factory=datetime.utcnow)