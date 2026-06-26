from pydantic import BaseModel

class GoalBase(BaseModel):
    target_amount: int
    current_amount: int
    name: str

class GoalCreate(GoalBase):
    user_id: int

class GoalUpdate(BaseModel):
    target_amount: int | None = None
    current_amount: int | None = None
    name: str | None = None

class GoalResponse(GoalBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True