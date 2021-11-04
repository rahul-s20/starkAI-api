from pydantic import BaseModel


class SymptopmSchema(BaseModel):
    symptoms: str
