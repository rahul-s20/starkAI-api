from app.controllers.symptomController import symptomController, saveSymptomModelController
from app.controllers.langTranslationController import langTranslationController
from app.controllers.apiKeyController import assignKey

from sqlalchemy.orm import Session
from app.config.get_db import get_db
from app.controllers.csv2mysqlController import CSV2Mysql
from app.controllers.csv2postgresqlController import CSV2Postgresql

from fastapi import APIRouter, Depends, File, UploadFile
from app.schema.Csv2MysqlSchema import Csv2MysqlSchema
from app.schema.TranslateSchema import TranslateSchema
from app.schema.SymptopmSchema import SymptopmSchema
from app.schema.KeySchema import Keyssc
from fastapi.responses import JSONResponse
from app.pipelines.migration.csv_to_db.tasks import csv_to_sql_task_run
from app.controllers.sql2sqlController import SQL2SQL
from app.schema.Sql2SqlSchema import Sql2SqlSchema
from app.pipelines.migration.Sql_to_Sql.tasks import sql_to_sql_task_run
from app.controllers.resumeScreeningController import saveResumeScreeningModel, resumeScreeningController
from app.schema.ResumeScreeningSchema import ResumeScreeningSchema
from app.controllers.resumeUploadController import ResumeUploadController
from typing import List
from app.config.init_db_tables import init_db

router = APIRouter()


@router.post("/api/v1/upload_resume")
def resume_upload_route(resume_files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    res = ResumeUploadController(files=resume_files, db=db)
    return res


@router.get("/api/v1/generate_resume_model")
def resume_modelsave_route():
    res = saveResumeScreeningModel()
    return res


@router.get("/api/v1/generate_symptom_model")
def symptom_modelsave_route():
    res = saveSymptomModelController()
    return res


@router.post("/api/v1/symptom_disease")
def symptom_route(input_details: SymptopmSchema):
    res = symptomController(symptoms=input_details)
    return res


@router.post("/api/v1/resume_screening")
def symptom_route(input_details: ResumeScreeningSchema):
    res = resumeScreeningController(input_skills=input_details)
    return res


@router.post("/api/v1/translate")
def translation_route(input_details: TranslateSchema):
    res = langTranslationController(input_text=input_details)
    return res


@router.post('/api/v1/generate_all_table')
def createAlldb(db: Session = Depends(get_db)):
    init_db(db)
    return JSONResponse(content="All tables created!")


@router.post('/api/v1/generate_api_key')
def apiKeyGenerate_route(email: Keyssc, db: Session = Depends(get_db)):
    res = assignKey(email=email, db=db)
    return res


@router.get('/testing')
def getapicheck_route():
    return {"hello": "welcome"}


@router.post('/api/v1/migrate/csv_to_mysql_db')
async def csv2mysql_route(req_details: Csv2MysqlSchema):
    try:
        csv_to_sql_task_run.delay(req_details.aws_details.endpoint, req_details.aws_details.accesskey,
                                  req_details.aws_details.secretkey, req_details.aws_details.region,
                                  req_details.mysql_details.user, req_details.mysql_details.password,
                                  req_details.mysql_details.host, req_details.mysql_details.db,
                                  req_details.content_details.bucket, req_details.content_details.key,
                                  req_details.content_details.columns, req_details.content_details.default_values,
                                  bool(req_details.content_details.add_primaryKey),
                                  req_details.content_details.type_of_insertion, req_details.content_details.db_table)
        response = {"status": True, "type": "csv2Mysql", "data": "Data has been migrated successfully"}
        return JSONResponse(content=response)
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "csv2Mysql_task_fail", "data": f"{er.__cause__}"})


@router.post('/api/v1/migrate/sql_to_sql')
def sql2sql_route(req_details: Sql2SqlSchema):
    try:
        sql_to_sql_task_run.delay(
            req_details.src_mysql_details.user, req_details.src_mysql_details.password,
            req_details.src_mysql_details.host, req_details.src_mysql_details.db, req_details.trgt_sql_details.user,
            req_details.trgt_sql_details.password, req_details.trgt_sql_details.host, req_details.trgt_sql_details.db,
            req_details.content_details.src_db_table, req_details.content_details.trgt_db_table,
            req_details.content_details.extra_columns, req_details.content_details.type_of_insertion)
        return JSONResponse(
            content={"status": True, "type": "Sql2Sql", "data": "Sql Data has been migrated successfully"})
    except Exception as er:
        return JSONResponse(content={"status": False, "type": "Sql2Sql", "data": f"{er.__cause__}"})


@router.post('/api/v1/migrate/csv_to_postgres_db')
def csv2postgressql_route(req_details: Csv2MysqlSchema):
    csvtopsql_obj = CSV2Postgresql(endpoint=req_details.aws_details.endpoint,
                                   accesskey=req_details.aws_details.accesskey,
                                   secretkey=req_details.aws_details.secretkey, region=req_details.aws_details.region,
                                   usr=req_details.mysql_details.user, pwd=req_details.mysql_details.password,
                                   hst=req_details.mysql_details.host, db=req_details.mysql_details.db)

    res = csvtopsql_obj.migrate_csv_to_postgresql(bucket=req_details.content_details.bucket,
                                                  key=req_details.content_details.key,
                                                  columns=req_details.content_details.columns,
                                                  default_values=req_details.content_details.default_values,
                                                  add_primaryKey=bool(req_details.content_details.add_primaryKey),
                                                  type_of_insertion=req_details.content_details.type_of_insertion,
                                                  db_table=req_details.content_details.db_table,
                                                  )

    return res
