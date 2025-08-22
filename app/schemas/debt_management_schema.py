from pydantic import BaseModel, Field
from typing import Optional, List

class LoanDetails(BaseModel):
    loan_name: str = Field(..., description="Name or type of the loan")
    principal_amount: float = Field(..., description="Original loan amount")
    outstanding_balance: float = Field(..., description="Current amount owed")
    annual_interest_rate: float = Field(..., description="Annual interest rate (%)")
    monthly_payment: float = Field(..., description="Current required monthly payment")
    remaining_term_months: int = Field(..., description="Months left to pay")

class BusinessFinancials(BaseModel):
    avg_monthly_revenue: float = Field(..., description="Average monthly revenue")
    avg_monthly_operating_expenses: float = Field(..., description="Average monthly operating expenses (excluding loan payments)")
    current_cash_reserves: float = Field(..., description="Current cash reserves")

class GrowthNeeds(BaseModel):
    capital_required: float = Field(..., description="Capital required for growth/expansion")
    expected_roi: Optional[float] = Field(None, description="Expected ROI from investment (%)")

class ProposedFinancing(BaseModel):
    proposed_loan_amount: Optional[float] = Field(0, description="Proposed new loan amount")
    proposed_annual_interest_rate: Optional[float] = Field(0, description="Proposed annual interest rate (%)")
    proposed_loan_term: Optional[int] = Field(0, description="Proposed loan term (months)")

class DebtManagementInput(BaseModel):
    scenario_type: str = Field("debt_management", description="Type of scenario")
    user_type: str = Field("msme", description="User type")
    projection_period: int = Field(..., description="Number of months/quarters for projection")
    loans: List[LoanDetails]
    business_financials: BusinessFinancials
    growth_needs: GrowthNeeds
    proposed_financing: ProposedFinancing
    reinvestment_rate: Optional[float] = Field(0, description="Percentage of net income to reinvest into the business")