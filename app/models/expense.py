from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Expense(BaseModel):
    __tablename__ = "expenses"

    amount = Column(Float)
    description = Column(String)
    created_at = Column(DateTime)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))

    category = relationship("Category", back_populates="expenses")
    account = relationship("Account", back_populates="expenses")