from fastapi import APIRouter, Depends, Form
from typing import Annotated

from src.database import SessionLocal
from sqlalchemy.orm import Session

from src.friends.schemas import FriendsBase

from src.friends.service import send_request_service, \
                                get_request_service, \
                                accept_request_service, \
                                get_mutual_friends_service
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

@router.post("/send_request")
async def send_request(
    db: db_dependency,
    friend_id: int = Form(...),
    user_id: dict = Depends(get_user_JWT)
):
    print(friend_id)
    request = FriendsBase(
        user_id=user_id.get("id"),
        friend_id=friend_id
    )

    return send_request_service(db, request)


@router.get("/get_request")
async def get_request(
    db: db_dependency, 
    JWT_user: dict = Depends(get_user_JWT)
):

    return get_request_service(db, JWT_user)

@router.put("/accept_request")
async def accept_request(
    db: db_dependency,
    JWT_user: dict = Depends(get_user_JWT),
    friend_id: int = Form(...),
):
    return accept_request_service(db, JWT_user, friend_id)

@router.get("/get_mutual_friends")
async def get_mutual_friends(
    db: db_dependency,
    JWT_user: dict = Depends(get_user_JWT)
):
    return get_mutual_friends_service(db, JWT_user)