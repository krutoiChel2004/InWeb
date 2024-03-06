from fastapi import HTTPException, Depends, Response, Request
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from starlette import status
from datetime import timedelta, datetime
from jose import jwt, JWTError

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

from sqlalchemy.orm import Session

from src.auth.schemas import UserBase
from src.auth.models import User

from src.config import SECRET_KEY, ALGORITHM


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def read_use_service(user_id: int, db: Session):
    task = db.query(User).filter(User.id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="User not found")
    return task


def create_user_service(user: UserBase, db: Session, request:Request):
    db_user = User(username=user.username,
                            hashed_password=bcrypt_context.hash(user.hashed_password),
                            email=user.email,
                            phone=user.phone,
                            name=user.name,
                            sex=user.sex,
                            # desc=user.desc,
                            birthday=user.birthday)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    request = RedirectResponse(url='/', status_code=HTTP_303_SEE_OTHER)
    return request

    


def login_user_service(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: Session, response: Response):
    user = auth_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    token = create_access_token(user.username, user.id, timedelta(minutes=1000))
    
    # Set token to cookie
    response = RedirectResponse(url='/news_feed', status_code=HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=token, httponly=True)

    return response

def auth_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



