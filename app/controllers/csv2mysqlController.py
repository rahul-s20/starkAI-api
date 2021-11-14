from app.pipelines.migration.csv_to_db.CSVpreparation import CSVToDf
from app.pipelines.migration.csv_to_db.ToMysql import DfToMysql
from os import environ as env
from fastapi.responses import JSONResponse


class CSV2Mysql:
    def __init__(self, endpoint=None, accesskey=None, secretkey=None, region=None,
                 usr=env['USER'], pwd=env['PASSWORD'], hst=env['HOST'],
                 db=env['DB']):
        if endpoint is not None:
            self.dataFrame_init = CSVToDf(endpoint=endpoint, accesskey=accesskey, secretkey=secretkey,
                                          region=region)
        else:
            self.dataFrame_init = CSVToDf(accesskey=accesskey, secretkey=secretkey)
        self.mysqlengine = DfToMysql(usr=usr, pwd=pwd, hst=hst, db=db)

    def migrate_csv_to_mysql(self, bucket: str = None, key: str = None, columns: list = [],
                             default_values: str = "missing",
                             add_primaryKey: bool = False, type_of_insertion: str = 'append',
                             db_table: str = 'table') -> JSONResponse:
        try:
            df = self.dataFrame_init.prepareCSVdf(bucket=bucket, key=key, columns=columns,
                                                  default_values=default_values,
                                                  add_primaryKey=add_primaryKey)
            if df is not None:
                self.mysqlengine.migrateToMysql(df=df, type_of_insertion=type_of_insertion, db_table=db_table)
            return {"status": True, "type": "csv2Mysql", "data": "Data has been migrated successfully"}

        except Exception as er:
            # res = {"status": False, "type": "csv2Mysql", "data": f"{er.__cause__}"}
            # return JSONResponse(content=res)
            return {"status": False, "type": "csv2Mysql", "data": f"{er.__cause__}"}


def check(text):
    print(text)
    return text