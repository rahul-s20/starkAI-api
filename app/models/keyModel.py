from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.config.base_class import Base


class Keys(Base):
    id = Column(Integer, primary_key=True)
    api_key = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
