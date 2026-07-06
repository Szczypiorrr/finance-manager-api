from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel

class Goal(BaseModel):
    __tablename__ = "goals"

    target_amount = Column(Integer)
    current_amount = Column(Integer)
    name = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id")) 

    user = relationship("User", back_populates="goals")