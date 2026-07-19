import os

UPLOAD_BASE_URL = os.getenv("UPLOAD_BASE_URL", "http://localhost/uploads")


def build_photo_url(file_path):
    """URL publique (servie par nginx) d'un fichier photo ; None si pas de photo."""
    if not file_path:
        return None
    return f"{UPLOAD_BASE_URL.rstrip('/')}/{file_path}"
