from app.controllers.symptomController import symptomController
from app.controllers.langTranslationController import langTranslationController
from app.controllers.transcriptController import transcriptController
from app.controllers.apiKeyController import assignKey

from sqlalchemy.orm import Session
from app.config.get_db import get_db
from app.controllers.csv2mysqlController import CSV2Mysql
from app.controllers.csv2postgresqlController import CSV2Postgresql

from fastapi import APIRouter, Depends
from app.schema.Csv2MysqlSchema import Csv2MysqlSchema
from app.schema.TranslateSchema import TranslateSchema
from app.schema.TransriptSchema import TransriptSchema
from app.schema.SymptopmSchema import SymptopmSchema
from app.schema.KeySchema import Keyssc
from fastapi.responses import JSONResponse
from app.pipelines.migration.csv_to_db.tasks import csv_to_sql_task_run

router = APIRouter()


@router.post("/api/v1/symptom_disease")
def symptom_route(input_details: SymptopmSchema):
    res = symptomController(symptoms=input_details)
    return res


@router.post("/api/v1/translate")
def translation_route(input_details: TranslateSchema):
    res = langTranslationController(input_text=input_details)
    return res


@router.post("/api/v1/transcript")
def transcript_route(input_details: TransriptSchema):
    res = transcriptController(vid_id=input_details)
    return res


@router.post('/api/v1/generate_all_table')
def createAlldb(db: Session = Depends(get_db)):
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
