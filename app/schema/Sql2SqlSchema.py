from pydantic import BaseModel
from app.schema.SqlSchema import SqlSchema
from app.schema.SqlContentSchema import SqlContentSchema


class Sql2SqlSchema(BaseModel):
    src_mysql_details: SqlSchema
    trgt_sql_details: SqlSchema
    content_details: SqlContentSchema
