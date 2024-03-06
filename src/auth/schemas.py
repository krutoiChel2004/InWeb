from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class ModelName(str, Enum):
    men = 'men'
    woman = 'woman'

class UserBase(BaseModel):
    username: str
    hashed_password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: str
    sex: ModelName
    # desc: Optional[str] = None
    birthday: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
