from sqlmodel import SQLModel, Field, JSON
from typing import Optional
from datetime import datetime

class BudgetOptimizationModel(SQLModel, table=True):
    """
    Stores all user inputs for budget optimization scenarios.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_type: str = Field(default="cash_flow_optimization")
    user_type: str = Field(default="family")
    projection_months: int

    # Store grouped user inputs as JSON for flexibility
    income: dict = Field(sa_column=Field(default={}, sa_column_kwargs={"type_": JSON}))
    expenses: dict = Field(sa_column=Field(default={}, sa_column_kwargs={"type_": JSON}))
    savings_goals: dict = Field(sa_column=Field(default={}, sa_column_kwargs={"type_": JSON}))

    # Store results and metadata
    results: dict = Field(sa_column=Field(default={}, sa_column_kwargs={"type_": JSON}))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)