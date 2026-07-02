from pydantic import BaseModel
from datetime import datetime

class MonthlyStatsResponse(BaseModel):
    total_expenses: float
    total_income: float
    balance: float
    transactions_count: int

class ByCategoryStatsResponse(BaseModel):
    category_name: str
    total_expenses: float

class BalanceBaseResponse(BaseModel):
    total_expenses: float
    total_income: float
    balance: float

class UserBalanceResponse(BalanceBaseResponse):
    username: str

class AccountBalanceResponse(BalanceBaseResponse):
    account_name: str

class UserAccountBalanceResponse(UserBalanceResponse, AccountBalanceResponse):
    pass

class TopExpensesResponse(BaseModel):
    amount: float
    description: str
    created_at: datetime
    account_name: str
    category_name: str

class MonthlyTrendResponse(BaseModel):
    month: str
    total_expenses: float
    