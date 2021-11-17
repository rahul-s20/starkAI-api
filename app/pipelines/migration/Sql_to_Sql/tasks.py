from . import app as celery_app, celery_log
from app.controllers.sql2sqlController import SQL2SQL


@celery_app.task(retry_kwargs={'max_retries': 5})
def sql_to_sql_task_run(src_sql_user, src_sql_passwrd, src_sql_host, src_sql_db,
                        trg_sql_user, trg_sql_passwrd, trg_sql_host, trg_sql_db,
                        src_table, trg_table, extr_cols, type_of_insertion):
    try:
        sql_obj = SQL2SQL(usr=src_sql_user, pwd=src_sql_passwrd, hst=src_sql_host, db=src_sql_db)
        res = sql_obj.migrate_data_to_sql(src_table_name=src_table,
                                          trgt_table_name=trg_table, extra_columns=extr_cols,
                                          type_of_insertion=type_of_insertion, usr=trg_sql_user, pwd=trg_sql_passwrd,
                                          hst=trg_sql_host, db=trg_sql_db)
        celery_log.info("All sql data is migrated successfully")
        return res
    except Exception as er:
        return er.__cause__
