from pydantic import BaseModel, Field
from typing import Optional


class EmergencyFundInput(BaseModel):
    target: float = Field(
        ...,
        description="Target amount for the emergency fund simulation"
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
        description="Percentage of income allocated to discretionary spending (0-100)"
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
        0.0,
        description="Extra payment towards the debt (zero allowed; defaults to 0 if omitted)"
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


class EducationFundInput(BaseModel):
    today_cost: float = Field(
        ...,
        description="Today's cost of the education"
    )
    years: int = Field(
        ...,
        description="Number of years until the education expense is incurred"
    )
    current_savings: float = Field(
        ...,
        description="Current savings amount for the education fund"
    )
    monthly_contrib: float = Field(
        ...,
        description="Monthly contribution to the education fund"
    )
    return_rate: float = Field(
        ...,
        description="Expected annual return rate on the education fund"
    )
    inflation_rate: float = Field(
        ...,
        description="Expected annual inflation rate for education costs"
    )


class MajorPurchaseInput(BaseModel):
    price: float = Field(
        ...,
        description="Price of the major purchase"
    )
    down_pct: float = Field(
        ...,
        description="Down payment percentage for the major purchase (0-100)"
    )
    years_to_save: int = Field(
        ...,
        description="Number of years to save for the major purchase"
    )
    current_savings: float = Field(
        ...,
        description="Current savings amount for the major purchase"
    )
    monthly_contrib: float = Field(
        ...,
        description="Monthly contribution towards the major purchase"
    )
    savings_return: float = Field(
        ...,
        description="Expected annual return rate on savings for the major purchase"
    )
    loan_rate: float = Field(
        ...,
        description="Annual interest rate on the loan for the major purchase"
    )
    loan_term: int = Field(
        ...,
        description="Loan term in years for the major purchase"
    )