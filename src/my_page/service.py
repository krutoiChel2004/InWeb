from fastapi import HTTPException, Depends, Form
from sqlalchemy.orm import Session

from src.post.models import Post
from src.auth.models import User

from src.client.client import get_user_JWT


def get_post_user_service(
                            db: Session,
                            user_id: dict = Depends(get_user_JWT),
                        ):
    posts = db.query(Post, User).join(User).filter(Post.user_id_post == user_id.get("id")).order_by(Post.data_create.desc()).all()
    
    posts = [{
            "id": post.id,
            "text_post": post.text_post,
            "path_photo": post.path_photo,
            "data_create": post.data_create.date(),
            "user_id_post": post.user_id_post,
            "name": user.name
        } for post, user in posts]

    return posts