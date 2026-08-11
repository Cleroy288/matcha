import logging
import os

from models.photo_model import get_photos_by_user
from models.user_model import delete_user
from services.constants import UPLOAD_DIR
from services.errors import ERR_USER_NOT_FOUND
from services.socket_service import disconnect_user

logger = logging.getLogger(__name__)


def delete_user_account(user_id):
    """Right to erasure (GDPR art. 17): deletes the account and every personal
    record that goes with it — profile, GPS position, photos, tags, likes,
    visits, blocks, reports, messages and notifications.

    The files are listed before the DELETE: photo rows disappear through the
    cascade and their paths would no longer be reachable."""
    photo_files = collect_photo_files(user_id)

    if not delete_user(user_id):
        raise Exception(ERR_USER_NOT_FOUND)

    remove_photo_files(photo_files)
    disconnect_user(user_id)


def collect_photo_files(user_id):
    """Disk paths of the user photos, before the cascade wipes them."""
    return [
        os.path.join(UPLOAD_DIR, photo["file_path"])
        for photo in get_photos_by_user(user_id)
    ]


def remove_photo_files(photo_files):
    """Removes the files from disk; a failure must not undo the account
    deletion, which is already committed in the database."""
    for path in photo_files:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            logger.exception("Could not delete uploaded file %s", path)
