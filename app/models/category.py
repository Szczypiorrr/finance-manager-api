from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Category(BaseModel):
    """Database model representing expense categories."""

    __tablename__ = "categories"

    name = Column(String)

    expenses = relationship("Expense", back_populates="category")
    budgets = relationship("Budget", back_populates="category")