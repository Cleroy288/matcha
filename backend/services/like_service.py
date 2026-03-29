from models.like_model import add_like, remove_like, is_match, get_likes_received
from models.block_model import is_blocked
from models.notification_model import create_notification
from utils.constants import LikeMessage
from services.socket_service import notify_user
from extensions import socketio

def like_user(liker_id, liked_id):
    if liker_id == liked_id:
        raise Exception(LikeMessage.LIKE_YOURSELF)
    
    if is_blocked(liker_id, liked_id):
        raise Exception(LikeMessage.LIKE_IMPOSSIBLE)
    liked = add_like(liker_id, liked_id)
    if not liked:
        raise Exception(LikeMessage.LIKE_ALREADY)
    

    if is_match(liker_id, liked_id):
        create_notification(liker_id, liked_id, "match")
        create_notification(liked_id, liker_id, "match")
        notify_user(socketio, liker_id, "match", {"with_user_id": liked_id})
        notify_user(socketio, liked_id, "match", {"with_user_id": liker_id})
        return {"liked": True, "match": True}

    create_notification(liked_id, liker_id, "like")
    notify_user(socketio, liked_id, "like", {"from_user_id": liker_id})

    return {"liked": True, "match": False}

def unlike_user(liker_id, liked_id):
    if liker_id == liked_id:
        raise Exception(LikeMessage.LIKE_YOURSELF)

    remove_like(liker_id, liked_id)
    create_notification(liked_id, liker_id, "unlike")
    notify_user(socketio, liked_id, "unlike", {"from_user_id": liker_id})

    return {"unliked": True}

def get_received_likes(user_id):
    return get_likes_received(user_id)