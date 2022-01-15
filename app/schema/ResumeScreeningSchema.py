from pydantic import BaseModel


class ResumeScreeningSchema(BaseModel):
    skills: list
