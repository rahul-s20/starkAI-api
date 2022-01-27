from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Column, Boolean
from app.config.base_class import Base


class UploadedResumes(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(2000), nullable=False)
    is_screened = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    isActive = Column(Boolean, default=True, nullable=False)
