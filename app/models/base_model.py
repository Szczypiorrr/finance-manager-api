from sqlalchemy import Integer, Column
from app.core.database import Base

class BaseModel(Base):
    """Base model with common database fields."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)