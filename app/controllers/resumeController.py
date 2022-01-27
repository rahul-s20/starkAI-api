from app.common.s3handler.helper import S3_Helper
from os import environ as env
from app.models.ResumeUploadModel import UploadedResumes
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.helpers.ResumeDataHandler import ResumeDataHandle, update_data
from app.schema.ResumeAnalysisSchema import ResumeAnalysisSchema
from app.controllers.resumeScreeningController import resumeScreeningControllerForAnalysis


class ResumeController:
    def __init__(self):
        self.resumeDataObj = ResumeDataHandle()
        self.s3obj = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])

    def get_resumeData(self, db: Session):
        try:
            data = self.resumeDataObj.get_all_uploaded_resume(db=db)
            return {"status": False, "type": "GetResumeData", "data": data}
        except Exception as er:
            return JSONResponse(content={"status": False, "type": "GetResumeData", "data": f"{er}"})

    def upload_resume(self, files, db: Session) -> JSONResponse:
        try:
            db_obj = {}
            validate_file = is_pdf(files)
            if validate_file is True:
                res = self.s3obj.upload_s3(files=files, bucket_name=env['RESUME_BUCKET'])
                if res is True:
                    for file in files:
                        db_obj["name"] = file.filename
                        self.resumeDataObj.insert_data(db=db, db_obj=db_obj)
                    return JSONResponse(content={"status": True, "type": "ResumeUpload", "data": "Resume uploaded "
                                                                                                 "successfully"})
                else:
                    return JSONResponse(
                        content={"status": True, "type": "ResumeUpload", "data": "Something Went wrong"})
            else:
                return JSONResponse(content={"status": False, "type": "ResumeUpload", "data": "File needs to be pdf "
                                                                                              "doc or in docx format"})
        except Exception as er:
            return JSONResponse(content={"status": False, "type": "ResumeUpload", "data": f"{er}"})

    def analyzeResume(self, resumes: ResumeAnalysisSchema, db: Session):
        listed_skills = []
        obj_toUpdate = {}
        try:
            for resume in resumes.list_of_files:
                data = self.s3obj.read_pdf_s3(bucket_name=env['RESUME_BUCKET'], file_name=resume['name'])
                listed_skills.append(data)
            res = resumeScreeningControllerForAnalysis(input_skills=listed_skills)
            if len(res) == len(resumes.list_of_files):
                for resume in resumes.list_of_files:
                    obj_toUpdate["id"] = resume['id']
                    obj_toUpdate["is_screened"] = True
                    update_data(db=db, modelClass=UploadedResumes, obj_in=obj_toUpdate)
                return JSONResponse(content={"status": True, "type": "ResumeAnalyzer", "data": res})
            else:
                return JSONResponse(content={"status": True, "type": "ResumeAnalyzer", "data": "Something went wrong"})
        except Exception as er:
            return JSONResponse(content={"status": False, "type": "ResumeAnalyzer", "data": f"{er}"})


def is_pdf(files: list) -> bool:
    not_supported_files = []
    for file in files:
        if '.pdf' not in file.filename and '.PDF' not in file.filename and '.doc' not in file.filename and '.docx' not in file.filename:
            not_supported_files.append(file.filename)
    if len(not_supported_files) > 0:
        return False
    else:
        return True
