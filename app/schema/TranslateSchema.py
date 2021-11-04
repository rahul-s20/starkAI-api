from pydantic import BaseModel


class TranslateSchema(BaseModel):
    input_text: str
    destination: str
