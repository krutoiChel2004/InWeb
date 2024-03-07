from sqlalchemy import Column, Integer, ForeignKey, String

from src.database import Base

class Friends(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")