from pydantic import BaseModel


class SqlSchema(BaseModel):
    user: str
    password: str
    host: str
    db: str
