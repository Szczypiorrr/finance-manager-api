from sqlalchemy import Integer, Column
from app.core.database import Base

class BaseModel(Base):

    __abstract__ = True

    id = Column(Integer, primary_key=True)