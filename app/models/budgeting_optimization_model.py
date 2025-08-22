from sqlmodel import SQLModel, Field, JSON, Column
from typing import Optional
from datetime import datetime

class BudgetOptimizationModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_type: str = Field(default="cash_flow_optimization")
    user_type: str = Field(default="family")
    projection_months: int

    income: dict = Field(default={}, sa_column=Column(JSON))
    expenses: dict = Field(default={}, sa_column=Column(JSON))
    savings_goals: dict = Field(default={}, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)