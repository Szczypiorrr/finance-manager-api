from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Budget(BaseModel):
    """Database model representing user budgets."""

    __tablename__ = "budgets"

    limit_amount = Column(Float)
    month = Column(Integer)
    year = Column(Integer)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")