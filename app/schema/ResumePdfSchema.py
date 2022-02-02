from pydantic import BaseModel


class ResumePdfSchema(BaseModel):
    file_name: str
