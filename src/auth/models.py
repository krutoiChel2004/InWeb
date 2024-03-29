from sqlalchemy import Column, Integer, String, DateTime, func
from datetime import datetime

from src.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String(11), unique=True)
    name = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    desc = Column(String, unique=True)
    birthday = Column(DateTime, nullable=False)
    date_create = Column(DateTime, nullable=False, default=func.now())