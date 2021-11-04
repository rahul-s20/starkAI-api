from pydantic import BaseModel
from app.schema.AwsDetailsSchema import AwsDetailsSchema
from app.schema.SqlSchema import SqlSchema
from app.schema.ContentSchema import ContentSchema


class Csv2MysqlSchema(BaseModel):
    aws_details: AwsDetailsSchema
    mysql_details: SqlSchema
    content_details: ContentSchema
