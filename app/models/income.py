from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Income(BaseModel):
    __tablename__ = "incomes"

    amount = Column(Float)
    source = Column(String)
    created_at = Column(DateTime)

    account_id = Column(Integer, ForeignKey("accounts.id"))

    account = relationship("Account", back_populates="income")