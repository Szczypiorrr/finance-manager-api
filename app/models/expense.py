from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Expense(BaseModel):
    __tablename__ = "expenses"

    amount = Column(Float)
    description = Column(String)
    date = Column(DateTime)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
    account = relationship("Account", back_populates="expenses")