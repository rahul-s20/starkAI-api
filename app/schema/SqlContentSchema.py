from pydantic import BaseModel


class SqlContentSchema(BaseModel):
    src_db_table: str
    trgt_db_table: str
    extra_columns: list
    type_of_insertion: str
