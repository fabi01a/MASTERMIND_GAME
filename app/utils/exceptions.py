class GameNotFoundError(Exception):
    """Raised when a game session cannot be found by ID"""

    pass


class GameOverError(Exception):
    """Raised when a game is already finished and cannot accept guesses"""

    pass


class InvalidGuessError(Exception):
    """Raised when a player's guess is improperly formatted"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
