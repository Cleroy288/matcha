from models.block_model import add_block, remove_block, is_blocked
from models.like_model import remove_like

def block_user(blocker_id, blocked_id):
    if blocker_id == blocked_id:
        raise Exception("You cannot block yourself")

    add_block(blocker_id, blocked_id)

    remove_like(blocker_id, blocked_id)
    remove_like(blocked_id, blocker_id)


def unblock_user(blocker_id, blocked_id):
    remove_block(blocker_id, blocked_id)


def check_is_blocked(user1_id, user2_id):
    return is_blocked(user1_id, user2_id)