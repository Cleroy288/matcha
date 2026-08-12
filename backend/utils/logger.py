import logging
import os

LOG_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
DEFAULT_LOG_LEVEL = "INFO"


def configure_logging():
    """Configures application logging; replaces the scattered print() calls.

    Called once at startup, before the blueprints are registered."""
    level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
    logging.basicConfig(level=level, format=LOG_FORMAT)
