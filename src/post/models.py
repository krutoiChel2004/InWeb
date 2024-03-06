from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, ARRAY, func
from datetime import datetime

from src.database import Base

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    text_post = Column(String(1000))
    path_photo = Column(String)
    data_create = Column(DateTime, nullable=False, default=func.now())
    user_id_post = Column(Integer, ForeignKey("user.id"), nullable=False)
    likes = Column(Integer, default=0)