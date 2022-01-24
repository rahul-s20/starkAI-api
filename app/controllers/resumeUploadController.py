from app.common.s3handler.helper import S3_Helper
from os import environ as env
from app.models.ResumeUploadModel import UploadedResumes
from sqlalchemy.orm import Session
from app.config.base import STARKBase


def ResumeUploadController(files, db: Session):
    try:
        db_obj = {}
        stark_base = STARKBase(UploadedResumes)
        s3obj = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
        res = s3obj.upload_s3(files=files, bucket_name=env['RESUME_BUCKET'])
        if res is True:
            for file in files:
                db_obj["name"] = file.filename
                stark_base.create(db=db, obj_in=db_obj)
            return {"status": True, "type": "ResumeUpload", "data": "Resume uploaded successfully"}
        else:
            return {"status": False, "type": "ResumeUpload", "data": "Something went wrong"}
    except Exception as er:
        return {"status": False, "type": "ResumeUpload", "data": f"{er}"}
