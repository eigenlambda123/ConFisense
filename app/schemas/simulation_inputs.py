from pydantic import BaseModel, Field
from typing import Optional


class EmergencyFundInput(BaseModel):
    scenario_title: Optional[str] = Field(
        None,
        description="Optional title for the emergency fund scenario"
    )
    monthly_expenses: float = Field(
        ...,
        description="Monthly expenses for the emergency fund simulation"
    )
    months_of_expenses: int = Field(
        ...,
        description="Number of months to cover with the emergency fund"
    )
    current_emergency_savings: float = Field(
        ...,
        description="Current emergency savings amount"
    )
    monthly_savings: float = Field(
        ...,
        description="Monthly contribution to the emergency fund"
    )
    annual_interest_rate_percent: float = Field(
        ...,
        description="Expected annual interest rate (percent) for the emergency fund"
    )


class BudgetInput(BaseModel):
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