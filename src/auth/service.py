from fastapi import HTTPException

from sqlalchemy.orm import Session

from .schemas import UserBase
from .models import User


def read_use_service(user_id: int, db: Session):
    task = db.query(User).filter(User.id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="User not found")
    return task


def create_user_service(user: UserBase, db: Session):
    db_user = User(username=user.username,
                          hashed_password=user.hashed_password,
                          email=user.email,
                          phone=user.phone,
                          name=user.name,
                          desc=user.desc,
                          birthday=user.birthday)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)