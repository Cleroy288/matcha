import os

UPLOAD_BASE_URL = os.getenv("UPLOAD_BASE_URL", "http://localhost/uploads")


def build_photo_url(file_path):
    """Public URL (served by nginx) of a photo file; None when there is no photo."""
    if not file_path:
        return None
    return f"{UPLOAD_BASE_URL.rstrip('/')}/{file_path}"
