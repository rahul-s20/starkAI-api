from pydantic import BaseModel


class ExtraColumnSchema(BaseModel):
    key: str
    value: str
