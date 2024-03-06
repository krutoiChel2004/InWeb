from pydantic import BaseModel

class FriendsBase(BaseModel):
    user_id: int
    friend_id: int