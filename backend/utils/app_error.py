DEFAULT_ERROR_STATUS = 400


class AppError(Exception):
    """Expected business error whose message is meant for the end user.

    Defined in utils/ because it is the only layer imported by both the
    services and the controllers. In step 3 the services will raise AppError
    instead of Exception and the controllers will catch only this one:
    everything else bubbles up to the global handler, logged and returned as a generic 500."""

    def __init__(self, message, status=DEFAULT_ERROR_STATUS):
        super().__init__(message)
        self.message = message
        self.status = status
