from pydantic import BaseModel
from datetime import datetime

class MonthlyStatsResponse(BaseModel):
    """Schema for monthly statistics."""

    total_expenses: float
    total_income: float
    balance: float
    transactions_count: int

class ByCategoryStatsResponse(BaseModel):
    """Schema for category statistics."""

    category_name: str
    total_expenses: float

class BalanceBaseResponse(BaseModel):
    """Base schema for balance statistics."""

    total_expenses: float
    total_income: float
    balance: float

class UserBalanceResponse(BalanceBaseResponse):
    """Schema for user balance statistics."""

    username: str

class AccountBalanceResponse(BalanceBaseResponse):
    """Schema for account balance statistics."""

    account_name: str

class UserAccountBalanceResponse(UserBalanceResponse, AccountBalanceResponse):
    """Schema for user account balance statistics."""

    pass

class TopExpensesResponse(BaseModel):
    """Schema for top expense results."""

    amount: float
    description: str
    created_at: datetime
    account_name: str
    category_name: str

class MonthlyTrendResponse(BaseModel):
    """Schema for monthly expense trends."""

    month: str
    total_expenses: float
    