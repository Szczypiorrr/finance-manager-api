from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Account(BaseModel):
    __tablename__ = "accounts"

    name = Column(String)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey="users.id")

    user = relationship("User", back_populates="accounts")
    expenses = relationship("Expense", back_populates="account")