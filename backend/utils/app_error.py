DEFAULT_ERROR_STATUS = 400


class AppError(Exception):
    """Erreur métier attendue, dont le message est destiné à l'utilisateur.

    Définie dans utils/ parce que c'est la seule couche importée à la fois par
    les services et les contrôleurs. À l'étape 3, les services lèveront AppError
    au lieu d'Exception et les contrôleurs n'attraperont plus qu'elle : tout le
    reste remontera au handler global, logué et renvoyé en 500 générique."""

    def __init__(self, message, status=DEFAULT_ERROR_STATUS):
        super().__init__(message)
        self.message = message
        self.status = status
