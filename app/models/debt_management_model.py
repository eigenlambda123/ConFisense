from sqlmodel import SQLModel, Field, JSON, Column
from typing import Optional
from datetime import datetime

class DebtManagementModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_type: str = Field(default="debt_management")
    user_type: str = Field(default="msme")
    projection_period: int

    loans: dict = Field(default={}, sa_column=Column(JSON))
    business_financials: dict = Field(default={}, sa_column=Column(JSON))
    growth_needs: dict = Field(default={}, sa_column=Column(JSON))
    proposed_financing: dict = Field(default={}, sa_column=Column(JSON))
    reinvestment_rate: Optional[float] = Field(default=0)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)