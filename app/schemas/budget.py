from pydantic import BaseModel

class BudgetBase(BaseModel):
    """Base schema for budget data."""

    limit_amount: float

class BudgetCreate(BudgetBase):
    """Schema for creating a budget."""

    user_id: int
    category_id: int

class BudgetUpdate(BudgetBase):
    """Schema for updating a budget."""

    pass

class BudgetResponse(BudgetBase):
    """Schema returned for budget data."""

    month: int
    year: int
    id: int
    user_id: int
    category_id: int

    class Config:
        from_attributes = True
