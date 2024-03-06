import os

from fastapi import FastAPI, Depends, HTTPException, Request, Form
from typing import Annotated
from fastapi.staticfiles import StaticFiles
from src.database import engine, Base, SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.middleware.cors import CORSMiddleware

from src.auth.router import router as auth_router
from src.post.router import router as post_router
from src.pages.router import router as pages_router
from src.client.client import router as client_router
from src.my_page.router import router as my_page_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router)
app.include_router(post_router)
app.include_router(pages_router)
app.include_router(client_router)
app.include_router(my_page_router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
