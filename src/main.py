import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .database import engine, Base

from .auth.router import router as auth_router
from .post.router import router as post_router
from .pages.router import router as pages_router

app = FastAPI()

# templates = Jinja2Templates(directory="src\\..\\templates")
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(pages_router)
    

# @app.get('/')
# async def name(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "name": "codingwithroby"})