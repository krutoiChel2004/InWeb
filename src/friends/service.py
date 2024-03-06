from sqlalchemy.orm import Session


from src.friends.models import Friends
from src.friends.schemas import FriendsBase

def inv_friends_service(
    db: Session,
    inv_friends: FriendsBase
):
    
    request_verification = db.query(Friends).filter(
        Friends.user_id == inv_friends.user_id, 
        Friends.friend_id == inv_friends.friend_id).first()
    
    if request_verification is not None:
        return {"messege":"Запрос уже отправлен"}

    db_friends = Friends(
        user_id=inv_friends.user_id,
        friend_id=inv_friends.friend_id
    )

    db.add(db_friends)
    db.commit()
    db.refresh(db_friends)


def get_all_request(
    db: Session,
    user_id: dict
):
    peoples_requests: Friends = db.query(Friends.user_id).filter(
        Friends.friend_id == user_id.get("id")).all()
    peoples_requests_list = [request[0] for request in peoples_requests]
    print(peoples_requests_list)
    print(peoples_requests)

    my_requests: Friends = db.query(Friends.friend_id).filter(
        Friends.user_id == user_id.get("id")).all()
    my_requests_list = [request[0] for request in my_requests]
    print(my_requests_list)
    print(my_requests)

    return {"peoples_requests_list":peoples_requests_list, "my_requests_list":my_requests_list}

def friend_check(list1, list2):
    """
    Находит одинаковые элементы в двух списках.
    
    Параметры:
        list1 (list): Первый список.
        list2 (list): Второй список.
        
    Возвращает:
        list: Список, содержащий одинаковые элементы из двух списков.
    """
    set1 = set(list1)
    set2 = set(list2)
    
    return list(set1.intersection(set2))

def friend_check_list_service(
    db: Session,
    user_id: dict
):

    all_request = get_all_request(db, user_id)


    return {"friend_check_list": friend_check(
        all_request.get("peoples_requests_list"), 
        all_request.get("my_requests_list")
        )}

def friend_requests(list1, list2):
    """
    Находит уникальные элементы в обоих списках.
    
    Параметры:
        list1 (list): Первый список.
        list2 (list): Второй список.
        
    Возвращает:
        list: Список, содержащий уникальные элементы из обоих списков.
    """

    set1 = set(list1)
    set2 = set(list2)
    
    return list(set1.symmetric_difference(set2))

def friend_requests_service(
    db: Session,
    user_id: dict
):
    
    all_request = get_all_request(db, user_id)

    return {"friend_check_list": friend_requests(
        all_request.get("peoples_requests_list"), 
        all_request.get("my_requests_list")
        )}



    