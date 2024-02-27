from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    hashed_password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: str
    desc: Optional[str] = None
    birthday: datetime
    date_create: datetime