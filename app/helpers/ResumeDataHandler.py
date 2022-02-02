from app.config.base import STARKBase
from app.models.ResumeUploadModel import UploadedResumes
from app.models.ResumeProfiles import ResumeProfiles
from sqlalchemy.orm import Session
from typing import Any


def updateResume_data(db: Session, modelClass, obj_in: dict):
    item_to_update = db.query(modelClass).filter(modelClass.id == obj_in["id"]).first()
    item_to_update.is_screened = obj_in["is_screened"]
    db.commit()
    return item_to_update


def updateResume_profile_data(db: Session, modelClass, obj_in: dict):
    item_to_update = db.query(modelClass).filter(modelClass.id == obj_in["id"]).first()
    item_to_update.is_Active = obj_in["is_Active"]
    item_to_update.resumeId = obj_in["resumeId"]
    item_to_update.name = obj_in["name"]
    item_to_update.phone_no = obj_in["phone_no"]
    item_to_update.email = obj_in["email"]
    item_to_update.domain = obj_in["domain"]
    item_to_update.skills = obj_in["skills"]
    item_to_update.timestamp = obj_in["timestamp"]
    db.commit()
    return item_to_update


class ResumeDataHandle:
    def __init__(self):
        self.stark_base = STARKBase(UploadedResumes)

    def get_all_uploaded_resume(self, db: Session):
        data = self.stark_base.get_multi(db=db, limit=0)
        return data

    def get_resume_detail(self, db: Session, id: Any):
        return self.stark_base.get(db=db, id=id)

    def insert_data(self, db: Session, db_obj: dict):
        res = self.stark_base.create(db=db, obj_in=db_obj)
        return res


class ResumeProfileDataHandler:
    def __init__(self):
        self.stark_base = STARKBase(ResumeProfiles)

    def get_all_resume_profile(self, db: Session):
        data = self.stark_base.get_multi(db=db, limit=0)
        return data

    def get_resume_profile(self, db: Session, resumeId: Any):
        data = self.stark_base.get_resumeProfile_by_resumeId(db=db, resumeId=resumeId)
        return data

    def insert_data(self, db: Session, db_obj: dict):
        res = self.stark_base.create(db=db, obj_in=db_obj)
        return res
