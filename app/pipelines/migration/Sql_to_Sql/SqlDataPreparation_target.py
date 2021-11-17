from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from pandas import DataFrame
import pandas as pd


class SqlTarget:
    def __init__(self, usr: str = None, pwd: str = None, hst: str = None, db: str = None):
        if (usr and pwd and hst and db) is not None:
            creds = {'usr': usr, 'pwd': pwd, 'hst': hst, 'dbn': db}
            connstr = 'mysql+pymysql://{usr}:{pwd}@{hst}/{dbn}'
            self.engine = create_engine(connstr.format(**creds))

    def write_Newdata(self, df: DataFrame = None, type_of_insertion: str = 'replace',
                      db_table: str = 'table'):
        try:
            if df is not None:
                df.to_sql(name=db_table, con=self.engine, if_exists=type_of_insertion, index=False)
                return "Data migrated successfully"
            else:
                return "Pass sql data to migrate"
        except ProgrammingError as pex:
            print(pex.__cause__)
        except Exception as ex:
            return ex.__cause__


def prepare_src_data(table_name: str = None, extra_columns: list = [], con_engine= None):
    try:
        if table_name is not None:
            sqldf = pd.read_sql(f'SELECT * FROM {table_name}', con=con_engine)
            if len(extra_columns) > 0:
                for i in range(len(extra_columns)):
                    sqldf.insert(loc=i, column=extra_columns[i]['key'], value=extra_columns[i]['value'])
            return sqldf
    except Exception as er:
        return er.__cause__
