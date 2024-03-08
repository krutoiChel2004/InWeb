from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.friends.models import Friends
from src.friends.schemas import FriendsBase
from src.auth.models import User

def send_request_service(
    db: Session,
    request: FriendsBase
):
    
    request_verification = db.query(Friends).filter(
        Friends.user_id == request.user_id, 
        Friends.friend_id == request.friend_id).first()
    
    if request_verification is not None:
        return {"messege":"Запрос уже отправлен"}

    db_friends = Friends(
        user_id=request.user_id,
        friend_id=request.friend_id
    )

    db.add(db_friends)
    db.commit()
    db.refresh(db_friends)

def get_request_service(
    db: Session, 
    JWT_user: dict
):
    user_id = JWT_user.get("id")

    results = db.query(User).join(Friends, and_(Friends.user_id == User.id, 
                                                Friends.friend_id == user_id)).filter(Friends.status=="pending").all()

    return results

def accept_request_service(
    db: Session, 
    JWT_user: dict,
    friend_id: int 
):
    user_id = JWT_user.get("id")
    db.query(Friends).filter(Friends.user_id==friend_id, 
                             Friends.friend_id==user_id).update({"status":"accepted"})
    
    accept_req = Friends(
        user_id=user_id,
        friend_id=friend_id,
        status="accepted"
    )

    db.add(accept_req)
    db.commit()
    db.refresh(accept_req)

def get_mutual_friends_service(
        db: Session,
        JWT_user: dict
):
    user_id = JWT_user.get("id")

    results = db.query(User).join(Friends, and_(Friends.user_id == User.id, 
                                                Friends.friend_id == user_id)).filter(Friends.status=="accepted").all()
    return results