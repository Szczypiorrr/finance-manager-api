from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Income(BaseModel):
    __tablename__ = "incomes"

    amount = Column(Float)
    source = Column(String)
    date = Column(DateTime)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="income")