from . import app as celery_app, celery_log
from app.controllers.csv2mysqlController import CSV2Mysql


@celery_app.task(retry_kwargs={'max_retries': 5})
def csv_to_sql_task_run(s3_endpoint, s3_accesskey, s3_secretkey, s3_region, sql_user, sql_passwrd, sql_host, sql_db,
                        s3_src_bkt, s3_src_key, cols, default_value, is_primaryKey, insert_type, tablename):
    try:
        csvtomysql_obj = CSV2Mysql(endpoint=s3_endpoint, accesskey=s3_accesskey, secretkey=s3_secretkey,
                                   region=s3_region, usr=sql_user, pwd=sql_passwrd, hst=sql_host, db=sql_db)
        res = csvtomysql_obj.migrate_csv_to_mysql(bucket=s3_src_bkt, key=s3_src_key, columns=cols,
                                                  default_values=default_value, add_primaryKey=bool(is_primaryKey),
                                                  type_of_insertion=insert_type, db_table=tablename )
        celery_log.info("All data is migrated successfully")
        return res
    except Exception as er:
        return er.__cause__
