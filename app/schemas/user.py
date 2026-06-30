from pydantic import BaseModel
from schemas.account import AccountResponse
from schemas.expense import ExpenseResponse
from schemas.income import IncomeResponse
from schemas.goal import GoalResponse
from schemas.budget import BudgetResponse

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserResponseDetail(UserResponse):
    accounts: list[AccountResponse]
    expenses: list[ExpenseResponse]
    income: list[IncomeResponse]
    goals: list[GoalResponse]
    budgets: list[BudgetResponse]

    class Config:
        from_attributes = True

