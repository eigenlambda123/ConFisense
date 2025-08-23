from sqlmodel import SQLModel, Field, JSON, Column
from typing import Optional
from datetime import datetime

class WealthBuildingModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    goal_name: str
    current_age: int
    target_age: int
    target_amount: float
    current_savings: float
    monthly_contribution: float
    annual_contribution_increase: Optional[float] = Field(default=0)
    expected_annual_return: Optional[float] = Field(default=0.07)
    inflation_rate: Optional[float] = Field(default=0.035)
    risk_profile: Optional[str] = Field(default="Moderate")
    advisor_fee_percent: Optional[float] = Field(default=0)

    chart_data: dict = Field(default={}, sa_column=Column(JSON))
    key_metrics: dict = Field(default={}, sa_column=Column(JSON))
    insight: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)