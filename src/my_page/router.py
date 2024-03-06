from fastapi import APIRouter, Depends
from typing import Annotated

from src.database import SessionLocal
from sqlalchemy.orm import Session

from src.my_page.service import get_post_user_service
from src.client.client import get_user_JWT

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/user_page",
    tags=["User_page"]
)

@router.get("")
async def get_post_user(
                        db: db_dependency, 
                        user_id = Depends(get_user_JWT)
                        ):
    
    return get_post_user_service(db, user_id)