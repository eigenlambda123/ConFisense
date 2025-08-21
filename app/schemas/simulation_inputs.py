from pydantic import BaseModel, Field
from typing import Optional

class BudgetInput(BaseModel):
    scenario_title: Optional[str] = Field(
        None,
        description="Optional title for the budgeting scenario"
    )
    monthly_net_income: float = Field(
        ...,
        description="Monthly net income for the budget simulation"
    )
    housing_expense: float = Field(
        ...,
        description="Monthly housing expense for the budget simulation"
    )
    food_grocery_expense: float = Field(
        ...,
        description="Monthly food and grocery expense for the budget simulation"
    )
    utilities_expense: float = Field(
        ...,
        description="Monthly utilities expense for the budget simulation"
    )
    transportation_expense: float = Field(
        ...,
        description="Monthly transportation expense for the budget simulation"
    )
    debt_payments_expense: float = Field(
        ...,
        description="Monthly debt payments expense for the budget simulation"
    )
    medical_healthcare_expense: float = Field(
        ...,
        description="Monthly medical and healthcare expense for the budget simulation"
    )
    education_expense: float = Field(
        ...,
        description="Monthly education expense for the budget simulation"
    )
    household_supplies_maintenance_expense: float = Field(
        ...,
        description="Monthly household supplies and maintenance expense for the budget simulation"
    )
    personal_care_shopping_expense: float = Field(
        ...,
        description="Monthly personal care and shopping expense for the budget simulation"
    )
    entertainment_recreation_expense: float = Field(
        ...,
        description="Monthly entertainment and recreation expense for the budget simulation"
    )
    gifts_donations_expense: float = Field(
        ...,
        description="Monthly gifts and donations expense for the budget simulation"
    )
    savings_investment_contribution: float = Field(
        ...,
        description="Monthly savings and investment contribution for the budget simulation"
    )


