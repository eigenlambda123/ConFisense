from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class BudgetingModel(SQLModel, table=True):
    """
    Budgeting Model for the database
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario_title: str
    monthly_net_income: float
    housing_expense: float
    food_grocery_expense: float
    utilities_expense: float
    transportation_expense: float
    debt_payments_expense: float
    medical_healthcare_expense: float
    education_expense: float
    household_supplies_maintenance_expense: float
    personal_care_shopping_expense: float
    entertainment_recreation_expense: float
    gifts_donations_expense: float
    savings_investment_contribution: float
