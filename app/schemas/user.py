from pydantic import BaseModel


class UserBase(BaseModel):
    """Base schema for user data."""

    username: str

class UserCreate(UserBase):
    """Schema for creating a user."""

    pass

class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str

class UserResponse(UserBase):
    """Schema returned for user data."""

    id: int

    class Config:
        from_attributes = True


