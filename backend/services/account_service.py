import logging
import os

from models.photo_model import get_photos_by_user
from models.user_model import delete_user
from services.constants import UPLOAD_DIR
from services.errors import ERR_USER_NOT_FOUND
from services.socket_service import disconnect_user

logger = logging.getLogger(__name__)


def delete_user_account(user_id):
    """Droit à l'effacement (RGPD art. 17) : supprime le compte et toutes les
    données personnelles qui vont avec — profil, position GPS, photos, tags,
    likes, visites, blocks, reports, messages et notifications.

    Les fichiers sont listés avant le DELETE : les lignes photos disparaissent
    en cascade et leurs chemins seraient alors introuvables."""
    photo_files = collect_photo_files(user_id)

    if not delete_user(user_id):
        raise Exception(ERR_USER_NOT_FOUND)

    remove_photo_files(photo_files)
    disconnect_user(user_id)


def collect_photo_files(user_id):
    """Chemins disque des photos du user, avant que la cascade ne les efface."""
    return [
        os.path.join(UPLOAD_DIR, photo["file_path"])
        for photo in get_photos_by_user(user_id)
    ]


def remove_photo_files(photo_files):
    """Efface les fichiers du disque ; un échec ne doit pas annuler la suppression
    du compte, qui est déjà commitée en base."""
    for path in photo_files:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            logger.exception("Could not delete uploaded file %s", path)
