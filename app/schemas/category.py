from pydantic import BaseModel
from schemas.expense import ExpenseResponse
from schemas.budget import BudgetResponse

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    expenses: list[ExpenseResponse]
    budgets: list[BudgetResponse]

    class Config:
        from_attributes = True