from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Account(BaseModel):
    """Database model representing user financial accounts."""
    
    __tablename__ = "accounts"

    name = Column(String)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))


    income = relationship("Income", back_populates="account")
    user = relationship("User", back_populates="accounts")
    expenses = relationship("Expense", back_populates="account")