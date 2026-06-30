from pydantic import BaseModel

class BudgetBase(BaseModel):
    limit_amount: float

class BudgetCreate(BudgetBase):
    user_id: int
    category_id: int

class BudgetUpdate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    month: int
    year: int
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True
