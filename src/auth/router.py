from fastapi import APIRouter, Depends, Response, Form, Request
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from sqlalchemy import func

from starlette import status

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

from src.database import SessionLocal
from sqlalchemy.orm import Session

from src.auth.schemas import UserBase, Token

from src.auth.service import read_use_service, create_user_service, login_user_service

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

@router.get("/{user_id}", response_model=UserBase)
async def read_user(user_id: int, db: db_dependency):
    return read_use_service(user_id, db)

@router.post("/create_user")
async def create_user(
                        db: db_dependency,
                        request: Request,
                        username: str = Form(...), 
                        hashed_password: str = Form(...), 
                        email: str = Form(None), 
                        phone: str = Form(None),
                        name: str = Form(...),
                        sex: str = Form(...),
                        # desc: str = Form(None),
                        birthday: datetime = Form(...),
                    ):
    
    user_data = UserBase(
                            username=username,
                            hashed_password=hashed_password, 
                            email=email, 
                            phone=phone,
                            name=name,
                            sex=sex,
                            # desc=desc,
                            birthday=birthday
                        )
    print(username)
    return create_user_service(user_data, db, request)

@router.post("/login")
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency, response: Response):
    return login_user_service(form_data, db, response)

