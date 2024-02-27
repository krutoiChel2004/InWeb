from fastapi import APIRouter, Depends, Request
from typing import Annotated, Optional
from fastapi.templating import Jinja2Templates

from ..database import SessionLocal
from sqlalchemy.orm import Session

from .schemas import PostBase
from .service import get_post_service, create_post_service, del_post_service

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get("")
async def get_post(db: db_dependency):
    posts = get_post_service(db)
    return posts


@router.post("")
async def create_post(post: PostBase, db: db_dependency):
    return create_post_service(post, db)

@router.delete("")
async def del_post(user_id: int, posts_id: list[int], db: db_dependency):
    return del_post_service(user_id, posts_id, db)