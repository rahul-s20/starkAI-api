from sqlalchemy import Integer, String, Column, Boolean, DateTime,ForeignKey
from app.config.base_class import Base
from datetime import datetime


class ResumeProfiles(Base):
    id = Column(Integer, primary_key=True)
    resumeId = Column(Integer, ForeignKey("uploadedresumes.id"), nullable=True)
    name = Column(String(2000), nullable=False)
    phone_no = Column(String(2000), nullable=False)
    email = Column(String(2000), nullable=False)
    skills = Column(String(20000), nullable=False)
    domain = Column(String(2000), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_Active = Column(Boolean, default=True, nullable=False)
