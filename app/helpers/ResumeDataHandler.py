from app.config.base import STARKBase
from app.models.ResumeUploadModel import UploadedResumes
from sqlalchemy.orm import Session


def update_data(db: Session, modelClass, obj_in: dict):
    item_to_update = db.query(modelClass).filter(modelClass.id == obj_in["id"]).first()
    item_to_update.is_screened = obj_in["is_screened"]
    db.commit()
    return item_to_update


class ResumeDataHandle:
    def __init__(self):
        self.stark_base = STARKBase(UploadedResumes)

    def get_all_uploaded_resume(self, db: Session):
        data = self.stark_base.get_multi(db=db, limit=0)
        return data

    def get_resume_detail(self, db: Session):
        pass

    def insert_data(self, db: Session, db_obj: dict):
        res = self.stark_base.create(db=db, obj_in=db_obj)
        return res
