from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    """Base schema for expense data."""

    amount: float
    description: str

class ExpenseCreate(ExpenseBase):
    """Schema for creating an expense."""

    category_id: int
    account_id: int

class ExpenseUpdate(BaseModel):
    """Schema for updating an expense."""

    amount: float | None = None
    description: str | None = None
    category_id: int | None = None
    account_id: int | None = None

class ExpenseResponse(ExpenseBase):
    """Schema returned for expense data."""

    created_at: datetime
    id: int
    category_id: int
    account_id: int

    class Config:
        from_attributes = True
