
from fastapi import HTTPException
from typing import Optional
import json

from sqlalchemy.orm import Session, Query
from .schemas import PostBase
from .models import Post
from ..auth.models import User



def get_post_service(db: Session):
    posts = db.query(Post, User).join(User).all()
    # if user_id == None:
    #     posts = db.query(Post, User).join(User).all()
    # else:
    #     posts = db.query(Post, User).join(User).filter(Post.user_id_post == user_id).all()
    print(posts)

    if not posts:
        raise HTTPException(status_code=404, detail="Post not found")
    
    posts = [{
            "id": post.id,
            "text_post": post.text_post,
            "path_photo": post.path_photo,
            "data_create": post.data_create.date(),
            "user_id_post": post.user_id_post,
            "name": user.name
        } for post, user in posts]
    
    return posts


def create_post_service(post: PostBase, db: Session):
    print(post)
    db_post = Post(text_post=post.text_post,
                    path_photo=post.path_photo,
                    data_create=post.data_create,
                    user_id_post=post.user_id_post)
    

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    

    return db_post

def del_post_service(user_id: int, posts_id: list[int], db: Session):
    for post_id in posts_id:
        db.query(Post).filter(Post.user_id_post == user_id, Post.id == post_id).delete()
        db.commit()