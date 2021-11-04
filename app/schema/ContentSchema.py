from pydantic import BaseModel


class ContentSchema(BaseModel):
    bucket: str
    key: str
    columns: list
    default_values: str
    add_primaryKey: bool
    type_of_insertion: str
    db_table: str
