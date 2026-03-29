from models.notification_model import get_notifications, mark_all_read, count_unread

def get_user_notifications(user_id):
    return get_notifications(user_id)

def mark_notifications_read(user_id):
    mark_all_read(user_id)

def get_unread_count(user_id):
    return count_unread(user_id)