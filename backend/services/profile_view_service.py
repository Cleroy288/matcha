from models.profile_view_model import add_view, get_views_received
from models.block_model import is_blocked
from models.notification_model import create_notification
from services.socket_service import notify_user
from extensions import socketio

def view_profile(viewer_id, viewed_id):
    if viewer_id == viewed_id:
        return
    if is_blocked(viewer_id, viewed_id):
        return
    
    add_view(viewer_id, viewed_id)
    create_notification(viewed_id, viewer_id, "visit")
    notify_user(socketio, viewed_id, "visit", {"from_user_id": viewer_id})
    


def get_profile_views(user_id):
    return get_views_received(user_id)