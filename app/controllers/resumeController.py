from app.common.s3handler.helper import S3_Helper
from os import environ as env
from app.models.ResumeUploadModel import UploadedResumes
from app.models.ResumeProfiles import ResumeProfiles
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.helpers.ResumeDataHandler import ResumeDataHandle, updateResume_data, ResumeProfileDataHandler, \
    updateResume_profile_data
from app.schema.ResumeAnalysisSchema import ResumeAnalysisSchema
from app.controllers.resumeScreeningController import resumeScreeningControllerForAnalysis
from app.common.makedecision.skills_extrctor import SkillsExtractor
from datetime import datetime
import requests
import json
import re


class ResumeController:
    def __init__(self):
        self.resumeDataObj = ResumeDataHandle()
        self.resumeProfileObj = ResumeProfileDataHandler()
        self.s3obj = S3_Helper(env['secret'], env['access'], env['OVERRIDE_S3_ENDPOINT'], env['region'])
        self.skillext = SkillsExtractor()

    def get_resumeData(self, db: Session):
        try:
            data = self.resumeDataObj.get_all_uploaded_resume(db=db)
            return {"status": True, "type": "GetResumeData", "data": data}
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
            profile_list = []
            for resume in resumes.list_of_files:
                profile_obj = {}
                data = self.s3obj.read_pdf_s3(bucket_name=env['RESUME_BUCKET'], file_name=resume['name'])
                profile_obj["resumeId"] = resume['id']
                profile_obj["name"] = extract_nameV2(data)
                profile_obj["phone_no"] = extract_mobile_number(data)
                profile_obj["email"] = extract_email(data)
                if isinstance(self.skillext.extract_skills(input_text=data), set):
                    profile_obj["skills"] = ", ".join(self.skillext.extract_skills(input_text=data))
                else:
                    profile_obj["skills"] = self.skillext.extract_skills(input_text=data)
                listed_skills.append(data)
                profile_list.append(profile_obj)
            res = resumeScreeningControllerForAnalysis(input_skills=listed_skills)
            if len(res) == len(resumes.list_of_files):
                for resume in resumes.list_of_files:
                    obj_toUpdate["id"] = resume['id']
                    obj_toUpdate["is_screened"] = True
                    updateResume_data(db=db, modelClass=UploadedResumes, obj_in=obj_toUpdate)
                for index in range(len(res)):
                    update_profile_obj = {}
                    profile_list[index]["domain"] = res[index]
                    resumeProfile = self.resumeProfileObj.get_resume_profile(db=db,
                                                                             resumeId=profile_list[index]["resumeId"])
                    if resumeProfile is None:
                        self.resumeProfileObj.insert_data(db=db, db_obj=profile_list[index])
                    elif resumeProfile.is_Active is False:
                        update_profile_obj["is_Active"] = True
                        update_profile_obj["id"] = resumeProfile.id
                        update_profile_obj["resumeId"] = profile_list[index]["resumeId"]
                        update_profile_obj["name"] = profile_list[index]["name"]
                        update_profile_obj["phone_no"] = profile_list[index]["phone_no"]
                        update_profile_obj["email"] = profile_list[index]["email"]
                        update_profile_obj["domain"] = profile_list[index]["domain"]
                        update_profile_obj["skills"] = profile_list[index]["skills"]
                        update_profile_obj["timestamp"] = datetime.utcnow()
                        updateResume_profile_data(db=db, modelClass=ResumeProfiles, obj_in=update_profile_obj)
                    else:
                        update_profile_obj["is_Active"] = True
                        update_profile_obj["id"] = resumeProfile.id
                        update_profile_obj["resumeId"] = profile_list[index]["resumeId"]
                        update_profile_obj["name"] = profile_list[index]["name"]
                        update_profile_obj["phone_no"] = profile_list[index]["phone_no"]
                        update_profile_obj["email"] = profile_list[index]["email"]
                        update_profile_obj["domain"] = profile_list[index]["domain"]
                        update_profile_obj["skills"] = profile_list[index]["skills"]
                        update_profile_obj["timestamp"] = datetime.utcnow()
                        updateResume_profile_data(db=db, modelClass=ResumeProfiles, obj_in=update_profile_obj)

                return JSONResponse(content={"status": True, "type": "ResumeAnalyzer", "data": 'Analyzed successfully'})
            else:
                return JSONResponse(content={"status": True, "type": "ResumeAnalyzer", "data": "Something went wrong"})
        except Exception as er:
            return JSONResponse(content={"status": False, "type": "ResumeAnalyzer", "data": f"{er}"})

    def get_resumeProfileData(self, db: Session):
        try:
            data = self.resumeProfileObj.get_all_resume_profile(db=db)
            return {"status": True, "type": "GetResumeProfileData", "data": data}
        except Exception as er:
            return JSONResponse(content={"status": False, "type": "GetResumeProfileData", "data": f"{er}"})


def is_pdf(files: list) -> bool:
    not_supported_files = []
    for file in files:
        if '.pdf' not in file.filename and '.PDF' not in file.filename and '.doc' not in file.filename and '.docx' not in file.filename:
            not_supported_files.append(file.filename)
    if len(not_supported_files) > 0:
        return False
    else:
        return True


def extract_nameV2(resume_text: str):
    name = re.findall(r"[^()0-9-]+", resume_text)
    if name:
        try:
            return name[0].split()[0].strip(';')
        except IndexError:
            return None
    else:
        return 'No Name detected'


def extract_mobile_number(resume_text: str) -> str:
    phone = re.findall(re.compile(
        r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'),
        resume_text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number
    else:
        return 'No phone number'


def extract_email(resume_text: str) -> str:
    email = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', resume_text)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None
    else:
        return 'No Email detected'


def extract_skills(resume_text: str) -> str:
    try:
        url = "https://api.iki.ai/api/skills_extraction/"
        payload = {
            "text": str(resume_text[0:2000])
        }

        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(url=url, headers=headers, data=json.dumps(payload))
        return r.json()
    except Exception as er:
        return er
