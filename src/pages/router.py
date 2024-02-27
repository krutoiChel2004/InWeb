from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from ..post.router import get_post

router = APIRouter(
    tags=["Pages"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/news_feed/")
def get_posts_page(request: Request, posts = Depends(get_post)):
    return templates.TemplateResponse("news_feed.html", {"request": request, "posts": posts})