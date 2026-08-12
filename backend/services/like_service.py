from extensions import socketio
from models.block_model import is_blocked
from models.like_model import add_like, get_likes_received, is_match, remove_like
from models.notification_model import create_notification
from models.photo_model import get_profile_photo
from models.profile_model import get_profile_by_user_id
from services.errors import ERR_PROFILE_INCOMPLETE, ERR_PROFILE_PHOTO_REQUIRED
from services.socket_service import notify_user
from utils.constants import LikeMessage


def like_user(liker_id, liked_id):
    if liker_id == liked_id:
        raise Exception(LikeMessage.LIKE_YOURSELF)

    profile = get_profile_by_user_id(liker_id)
    if not profile or not profile.get("profile_complete"):
        raise Exception(ERR_PROFILE_INCOMPLETE)

    # subject IV.5: without a profile photo, liking is not allowed
    if not get_profile_photo(liker_id):
        raise Exception(ERR_PROFILE_PHOTO_REQUIRED)

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
