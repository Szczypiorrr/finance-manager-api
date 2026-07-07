from pydantic import BaseModel

class GoalBase(BaseModel):
    """Base schema for goal data."""

    target_amount: int
    name: str

class GoalCreate(GoalBase):
    """Schema for creating a goal."""

    user_id: int

class GoalUpdate(BaseModel):
    """Schema for updating a goal."""

    target_amount: int | None = None
    name: str | None = None

class GoalResponse(GoalBase):
    """Schema returned for goal data."""

    current_amount: int
    id: int
    user_id: int
    
    class Config:
        from_attributes = True