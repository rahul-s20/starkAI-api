from pydantic import BaseModel, EmailStr
from typing import Optional


class Keyssc(BaseModel):
    email: EmailStr
    api_key: Optional[str] = None