from app.common.s3handler.helper import S3_Helper
from os import environ as env
from app.models.ResumeUploadModel import UploadedResumes
from sqlalchemy.orm import Session
from app.config.base import STARKBase
from fastapi.responses import JSONResponse
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


def GetResumeData(db: Session) -> JSONResponse:
    try:
        stark_base = STARKBase(UploadedResumes)
        data = stark_base.get_multi(db=db, limit=0)
        return {"status": False, "type": "GetResumeData", "data": data}
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "GetResumeData", "data": f"{er}"})


def ResumeUploadController(files, db: Session):
    try:
        db_obj = {}
        stark_base = STARKBase(UploadedResumes)
        s3obj = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
        validate_file = is_pdf(files)
        if validate_file is True:
            res = s3obj.upload_s3(files=files, bucket_name=env['RESUME_BUCKET'])
            if res is True:
                for file in files:
                    db_obj["name"] = file.filename
                    stark_base.create(db=db, obj_in=db_obj)
                return {"status": True, "type": "ResumeUpload", "data": "Resume uploaded successfully"}
            else:
                return {"status": False, "type": "ResumeUpload", "data": "Something went wrong"}
        else:
            return {"status": False, "type": "ResumeUpload", "data": "File needs to be pdf doc or in docx format"}
    except Exception as er:
        return {"status": False, "type": "ResumeUpload", "data": f"{er}"}


class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def is_pdf(files: list) -> bool:
    for file in files:
        if '.pdf' not in file.filename and '.doc' not in file.filename and '.docx' not in file.filename:
            return False
        else:
            return True
