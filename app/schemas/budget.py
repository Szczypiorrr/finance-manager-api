from pydantic import BaseModel
from datetime import date

class BudgetBase(BaseModel):
    limit_amount: float
    month: date

class BudgetCreate(BudgetBase):
    user_id: int
    category_id: int

class BudgetUpdate(BaseModel):
    limit_amount: float | None = None
    month: date | None = None
    category_id: int | None = None

class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True
