from pydantic import BaseModel, Field
from typing import Optional


class EmergencyFundInput(BaseModel):
    target: float = Field(
        ...,
        description="Target for the simulation, default is 'emergency_fund'"
    )
    monthly_contrib: float = Field(
        ...,
        description="Monthly contribution to the emergency fund"
    )
    current_savings: float = Field(
        ...,
        description="Current savings amount"
    )


class BudgetInput(BaseModel):
    income: float = Field(
        ...,
        description="Monthly income for the budget simulation"
    )
    fixed_expenses: float = Field(
        ...,
        description="Monthly fixed expenses for the budget simulation"
    )
    discretionary_pct: float = Field(
        ...,
        description="Percentage of income allocated to discretionary spending"
    )
    target_savings: float = Field(
        ...,
        description="Target savings amount for the budget simulation"
    )


class DebtManagementInput(BaseModel):
    debt: float = Field(
        ...,
        description="Total debt amount for the debt management simulation"
    )
    monthly_payment: float = Field(
        ...,
        description="Monthly payment towards the debt"
    )
    interest_rate: float = Field(
        ...,
        description="Annual interest rate on the debt"
    )
    extra_payment: float = Field(
        ...,
        description="Extra payment towards the debt (if any)"
    )


class InvestmentInput(BaseModel):
    initial: float = Field(
        ...,
        description="Initial investment amount"
    )
    monthly: float = Field(
        ...,
        description="Monthly contribution to the investment"
    )
    return_rate: float = Field(
        ...,
        description="Expected annual return rate on the investment"
    )
    years: int = Field(
        ...,
        description="Number of years for the investment simulation"
    )