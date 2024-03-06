from fastapi import APIRouter, Depends
from typing import Annotated

from src.database import SessionLocal
from sqlalchemy.orm import Session

from src.friends.schemas import FriendsBase

from src.friends.service import inv_friends_service, friend_check_list_service, friend_requests_service
from src.client.client import get_user_JWT

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)

@router.post("/inv_friend")
async def inv_friends(
    db: db_dependency,
    friend_id: int,
    user_id: dict = Depends(get_user_JWT)
):
    
    inv_friends = FriendsBase(
        user_id=user_id.get("id"),
        friend_id=friend_id
    )

    return inv_friends_service(db, inv_friends)

@router.get("/friend_list")
async def friend_list(
    db: db_dependency,
    user_id: dict = Depends(get_user_JWT)
):
    
    return friend_check_list_service(db, user_id)

@router.get("/friend_requests_list")
async def friend_requests_list(
    db: db_dependency,
    user_id: dict = Depends(get_user_JWT)
):
    
    return friend_requests_service(db, user_id)