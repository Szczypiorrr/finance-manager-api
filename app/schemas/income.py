from pydantic import BaseModel
from datetime import datetime

class IncomeBase(BaseModel):
    amount: float
    source: str
    date: datetime

class IncomeCreate(IncomeBase):
    user_id: int

class IncomeUpdate(BaseModel):
    amount: float | None = None
    source: str | None = None
    date: datetime | None = None

class IncomeResponse(IncomeBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
