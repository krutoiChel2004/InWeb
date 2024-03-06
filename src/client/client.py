from fastapi import APIRouter, Depends, HTTPException, Request, Form
from typing import Annotated
from starlette import status
from jose import jwt, JWTError

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

# from src.auth.service import get_current_user

async def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    return token

router = APIRouter(prefix="/client",
                    tags=["Client"])

def get_current_user(token: str):
    try:
        print(token)
        payload = jwt.get_unverified_claims(token)
        print(payload)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        print(username, user_id)
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

@router.get("")
async def get_user_JWT(token: str = Depends(get_token_from_cookie)):
    return get_current_user(token)



