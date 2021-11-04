from pydantic import BaseModel
from typing import Optional


class AwsDetailsSchema(BaseModel):
    endpoint: Optional[str] = None
    accesskey: str
    secretkey: str
    region: Optional[str] = None
