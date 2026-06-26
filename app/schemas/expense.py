from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    amount: float
    description: str
    date: datetime

class ExpenseCreate(ExpenseBase):
    user_id: int
    category_id: int
    account_id: int

class ExpenseUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    date: datetime | None = None
    category_id: int | None = None
    account_id: int | None = None

class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    category_id: int
    account_id: int

    class Config:
        from_attributes = True
