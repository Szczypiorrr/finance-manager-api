from pydantic import BaseModel
from datetime import datetime

class IncomeBase(BaseModel):
    amount: float
    source: str

class IncomeCreate(IncomeBase):
    account_id: int

class IncomeUpdate(BaseModel):
    amount: float | None = None
    source: str | None = None

class IncomeResponse(IncomeBase):
    created_at: datetime
    id: int
    account_id: int

    class Config:
        from_attributes = True
