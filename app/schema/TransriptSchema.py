from pydantic import BaseModel


class TransriptSchema(BaseModel):
    vid: str
