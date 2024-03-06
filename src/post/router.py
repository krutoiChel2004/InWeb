from fastapi import APIRouter, Depends, Request, Form
from typing import Annotated, Optional
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

from src.database import SessionLocal
from sqlalchemy.orm import Session

from src.post.schemas import PostBase
from src.post.service import get_post_service, create_post_service, del_post_service
from src.client.client import get_user_JWT

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
async def get_post(
                    db: db_dependency
                ):
    
    return get_post_service(db)



@router.post("/add")
async def create_post(
                        db: db_dependency,
                        text_post: str = Form(None),
                        path_photo: str = Form(None),
                        user_id = Depends(get_user_JWT)
                        ):
    if text_post == None and path_photo == None:
        print("Введите хотябы одно значение")
        return RedirectResponse(url='/news_feed', status_code=HTTP_303_SEE_OTHER)
    
    post_data = PostBase(
                            text_post=text_post, 
                            path_photo=path_photo
                        )
    
    create_post_service(post_data, db, user_id)
    return RedirectResponse(url='/news_feed', status_code=HTTP_303_SEE_OTHER)



@router.delete("/del_post/{posts_id}")
async def del_post(
                    posts_id: str, 
                    db: db_dependency, 
                    user_id: dict = Depends(get_user_JWT)
                ):
    post_ids = posts_id.split(',')
    print(post_ids)
    return del_post_service(post_ids, db, user_id)

