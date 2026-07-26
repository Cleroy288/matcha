import logging
import os

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
DEFAULT_LOG_LEVEL = "INFO"


def configure_logging():
    """Configure le logging applicatif ; remplace les print() éparpillés.

    Appelé une seule fois au démarrage, avant l'enregistrement des blueprints."""
    level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
    logging.basicConfig(level=level, format=LOG_FORMAT)
