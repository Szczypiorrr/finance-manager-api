from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


