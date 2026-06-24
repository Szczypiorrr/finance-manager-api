from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String)

    expenses = relationship("Expense", back_populates="category")
    budgets = relationship("Budget", back_populates="category")