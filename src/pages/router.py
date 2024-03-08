from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.status import HTTP_303_SEE_OTHER
from starlette.responses import RedirectResponse

from src.post.router import get_post
from src.client.client import get_user_JWT
from src.my_page.router import get_post_user
from src.friends.router import get_mutual_friends, get_request

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/news_feed/")
def get_posts_page(
                    request: Request, 
                    posts = Depends(get_post)
                ):
    return templates.TemplateResponse("news_feed.html", {"request": request, "posts": posts})

@router.get("/")
def get_user_JWT_page(
                    request: Request
                ):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/reg/")
def get_register_page(
                    request: Request
                ):
    return templates.TemplateResponse("reg.html", {"request": request})

@router.get("/my_page/")
def get_user_page(
                    request: Request,
                    my_posts = Depends(get_post_user),
                    user_JWT: dict = Depends(get_user_JWT)
                ):
    return templates.TemplateResponse("my_page.html", {"request": request, "my_posts": my_posts, "user_name": user_JWT.get("username")})

@router.get("/friends_page/")
def get_friends_page(
                    request: Request,
                    list_mutual_friends = Depends(get_mutual_friends),
                    list_request: dict = Depends(get_request)
                ):
    return templates.TemplateResponse("friends_page.html", {"request": request, "list_mutual_friends": list_mutual_friends, "list_request": list_request})

