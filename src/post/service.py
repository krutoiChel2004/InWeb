
from fastapi import HTTPException, Depends, Form

from sqlalchemy.orm import Session, Query
from src.post.schemas import PostBase
from src.post.models import Post
from src.auth.models import User

from src.client.client import get_user_JWT



def get_post_service(
                        db: Session
                    ):
    posts = db.query(Post, User).join(User).order_by(Post.data_create.desc()).all()

    posts = [{
            "id": post.id,
            "text_post": post.text_post,
            "path_photo": post.path_photo,
            "data_create": post.data_create.date(),
            "user_id_post": post.user_id_post,
            "name": user.name
        } for post, user in posts]
    
    return posts



def create_post_service(
                        post_data: PostBase,
                        db: Session,
                        user_id: dict = Depends(get_user_JWT),
                        ):

    db_post = Post(
                    text_post=post_data.text_post,
                    path_photo=post_data.path_photo,
                    user_id_post=user_id.get("id")
                )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)



def del_post_service(
                        posts_id: list[int], 
                        db: Session, user_id: 
                        dict = Depends(get_user_JWT)
                    ):
    
    for post_id in posts_id:
        db.query(Post).filter(Post.user_id_post == user_id.get("id"), Post.id == post_id).delete()
        db.commit()