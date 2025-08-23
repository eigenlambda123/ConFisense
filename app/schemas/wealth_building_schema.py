from pydantic import BaseModel, Field
from typing import Optional

class WealthBuildingInput(BaseModel):
    goal_name: str = Field(..., description="Name of the financial goal (e.g., Retirement, Education, House Down Payment)")
    current_age: int = Field(..., description="Current age of the client")
    target_age: int = Field(..., description="Target age for goal achievement")
    target_amount: float = Field(..., description="Financial value needed for the goal")
    current_savings: float = Field(..., description="Amount already accumulated for the goal")
    monthly_contribution: float = Field(..., description="Current monthly contribution towards the goal")
    annual_contribution_increase: Optional[float] = Field(0, description="Annual increase in contribution (%)")
    expected_annual_return: Optional[float] = Field(0.07, description="Expected annual investment return (%)")
    inflation_rate: Optional[float] = Field(0.035, description="Inflation rate (%)")
    risk_profile: Optional[str] = Field("Moderate", description="Investment portfolio risk profile")
    advisor_fee_percent: Optional[float] = Field(0, description="Advisor fee as percent of assets under management")