from pydantic import BaseModel


class ResumeAnalysisSchema(BaseModel):
    list_of_files: list
