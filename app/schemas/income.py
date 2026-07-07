from pydantic import BaseModel
from datetime import datetime

class IncomeBase(BaseModel):
    """Base schema for income data."""

    amount: float
    source: str

class IncomeCreate(IncomeBase):
    """Schema for creating income."""

    account_id: int

class IncomeUpdate(BaseModel):
    """Schema for updating income."""

    amount: float | None = None
    source: str | None = None

class IncomeResponse(IncomeBase):
    """Schema returned for income data."""

    created_at: datetime
    id: int
    account_id: int

    class Config:
        from_attributes = True
