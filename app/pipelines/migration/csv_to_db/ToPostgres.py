from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from pandas import DataFrame


class DfToPostgresql:
    def __init__(self, usr: str = 'root', pwd: str = '123456789', hst: str = '127.0.0.1:3306', db: str = 'test'):
        # Set database credentials.
        creds = {'usr': usr, 'pwd': pwd, 'hst': hst,'dbn': db}
        connstr = 'postgresql://{usr}:{pwd}@{hst}/{dbn}'
        self.engine = create_engine(connstr.format(**creds))

    def migrateToPostgresql(self, df: DataFrame = None, type_of_insertion: str = 'append',
                       db_table: str = 'table'):
        try:
            if df is not None:
                df.to_sql(name=db_table, con=self.engine, if_exists=type_of_insertion, index=False)
                return "Data migrated successfully"
            else:
                return "Pass csv file to migrate"
        except ProgrammingError as pex:
            print(pex.__cause__)
        except Exception as ex:
            return ex.__cause__
