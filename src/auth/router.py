from fastapi import APIRouter, Depends
from typing import Annotated

from ..database import SessionLocal
from sqlalchemy.orm import Session

from .schemas import UserBase

from .service import read_use_service, create_user_service

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
) 

@router.get("/user/{task_id}", response_model=UserBase)
async def read_user(user_id: int, db: db_dependency):
    return read_use_service(user_id, db)

@router.post("/create_user/")
async def create_user(user: UserBase, db: db_dependency):
    return create_user_service(user, db)