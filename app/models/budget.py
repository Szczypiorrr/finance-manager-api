from sqlalchemy import Column, Float, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel

class Budget(BaseModel):
    __tablename__ = "budgets"

    limit_amount = Column(Float)
    month = Column(Date)

    user_id = Column(Integer, ForeignKey="users.id")
    category_id = Column(Integer, ForeignKey="categories.id")

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")