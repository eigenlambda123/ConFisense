from pydantic import BaseModel, Field
from typing import Optional, Dict

class IncomeDetails(BaseModel):
    monthly_net_income: float = Field(..., description="Take-home pay after taxes and deductions")
    other_monthly_income: Optional[float] = Field(0, description="Other income sources")
    income_frequency: Optional[str] = Field("monthly", description="Income frequency (monthly, semi-monthly, weekly)")

class FixedNeeds(BaseModel):
    rent_mortgage: float = 0
    utilities: float = 0
    loan_payments: float = 0
    insurance_premiums: float = 0
    tuition_fees: float = 0
    groceries: float = 0
    transportation: float = 0

class VariableNeeds(BaseModel):
    household_supplies: float = 0
    medical_health: float = 0
    misc_needs: float = 0

class WantsDiscretionary(BaseModel):
    dining_out: float = 0
    entertainment_hobbies: float = 0
    personal_care: float = 0
    shopping_leisure: float = 0
    travel_vacation: float = 0
    misc_wants: float = 0

class Expenses(BaseModel):
    fixed_needs: FixedNeeds
    variable_needs: VariableNeeds
    wants_discretionary: WantsDiscretionary

class SavingsGoals(BaseModel):
    target_monthly_savings: float = 0
    emergency_fund_target: float = 0

class BudgetOptimizationInput(BaseModel):
    scenario_type: str = Field("cash_flow_optimization", description="Type of scenario")
    user_type: str = Field("family", description="User type")
    projection_months: int = Field(..., description="Number of months for projection")
    income: IncomeDetails
    expenses: Expenses
    savings_goals: SavingsGoals