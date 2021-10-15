from app.common.pipeline.s3_handler import Inventory
import pandas as pd
from pandas.io import sql
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from app.common.helpers.helper import keyGenerate
import pandas as pd

# Set database credentials.
creds = {'usr': 'root',
         'pwd': '123456789',
         'hst': '127.0.0.1',
         'prt': 3306,
         'dbn': 'stark_dev'}

connstr = 'mysql+pymysql://{usr}:{pwd}@{hst}:{prt}/{dbn}'

engine = create_engine(connstr.format(**creds))
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="123456789"
# )


access = "minioadmin"
secret = "minioadmin"
region = "ap-south-1"
OVERRIDE_S3_ENDPOINT = "http://127.0.0.1:9000/"


def generate_primaryKey(length: int = None):
    s = []
    if length is not None:
        for i in range(length):
            s.append(keyGenerate(keyLen=6, case='lower'))
    return s


try:
    iv = Inventory(end_point=OVERRIDE_S3_ENDPOINT, aws_access=access, aws_secret=secret, region_name=region)
    # a = iv.read_files(bucket="datasets", key="csv_data/stark_data.csv", header=0)

    a = iv.read_files(bucket="pipeline", key="countrywise/", header=None)
    b = a.isnull().values.any()
    a.columns = ['countryregion', 'confirmed', 'deaths', 'recovered', 'active', 'newcases', 'newdeaths',
                 'newrecovered', 'deathper', 'recoveredper', 'deathperrecovered',
                 'confirmedlastweek', 'aweekchange', 'aweekincper', 'whoreg']
    b = bool(b)
    _ids = generate_primaryKey(length=len(a))
    a.insert(loc=0,
             column='ids',
             value=_ids)
    a.insert(loc=0, column='timestamp', value=pd.to_datetime('now').replace(microsecond=0))
    if b is False:
        print(">>>>>>>>>>>>>")
        a.to_sql(name='countrywise_covid', con=engine, if_exists='replace', index=False)
    print(a)
except ProgrammingError as pex:
    print(pex.__cause__)
# sql.write_frame(a, con=mydb, name='countrywise', if_exists='replace', flavor='mysql')
# sql._wrap_result()
