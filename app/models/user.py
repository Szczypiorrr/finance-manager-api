from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class User(BaseModel):
    """Database model representing application users."""

    __tablename__ = "users"

    username = Column(String)

    accounts = relationship("Account", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    budgets = relationship("Budget", back_populates="user")