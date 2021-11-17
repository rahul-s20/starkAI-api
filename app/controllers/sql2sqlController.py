from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from app.pipelines.migration.Sql_to_Sql.SqlDataPreparation_target import prepare_src_data, SqlTarget


class SQL2SQL:
    def __init__(self, usr: str = None, pwd: str = None, hst: str = None, db: str = None):
        if (usr and pwd and hst and db) is not None:
            creds = {'usr': usr, 'pwd': pwd, 'hst': hst, 'dbn': db}
            connstr = 'mysql+pymysql://{usr}:{pwd}@{hst}/{dbn}'
            self.engine = create_engine(connstr.format(**creds))

    def migrate_data_to_sql(self, src_table_name: str = None, trgt_table_name: str = None, extra_columns: list = [],
                            usr: str = None, pwd: str = None, hst: str = None, db: str = None,
                            type_of_insertion: str = 'replace'):
        try:
            prepared_data = prepare_src_data(table_name= src_table_name, extra_columns=extra_columns,
                                             con_engine= self.engine)
            trgt_db = SqlTarget(usr=usr, pwd=pwd, hst=hst, db=db)
            trgt_db.write_Newdata(df=prepared_data, type_of_insertion=type_of_insertion, db_table=trgt_table_name)
            return {"status": True, "type": "sql2sql", "data": "Sql Data has been migrated successfully"}
        except ProgrammingError as pex:
            return {"status": False, "type": "sql2sql", "data": f"{pex.__cause__}"}
        except Exception as er:
            return {"status": False, "type": "sql2sql", "data": f"{er.__cause__}"}

