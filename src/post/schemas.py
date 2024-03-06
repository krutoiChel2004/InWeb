from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    text_post: Optional[str] = None
    path_photo: Optional[str] = None