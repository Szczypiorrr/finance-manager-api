from pydantic import BaseModel

class CategoryBase(BaseModel):
    """Base schema for category data."""

    name: str

class CategoryCreate(CategoryBase):
    """Schema for creating a category."""

    pass

class CategoryUpdate(CategoryBase):
    """Schema for updating a category."""

    pass

class CategoryResponse(CategoryBase):
    """Schema returned for category data."""

    id: int

    class Config:
        from_attributes = True