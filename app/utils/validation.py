from app.game_settings import MIN_VALUE, MAX_VALUE
from app.models.gameSession import GameSession
from app.models.player import Player
from app.utils.exceptions import InvalidGuessError
from app import db

def validate_guess_input(player_guess: list[int], code_length: int = 4):
    if not isinstance(player_guess, list) or len(player_guess) != code_length:
        raise InvalidGuessError(f"Please enter four numbers")
    
    for num in player_guess:
        if not isinstance(num, int):
            raise InvalidGuessError("Invalid guess - Please enter numbers only")
        if not (MIN_VALUE <= num <= MAX_VALUE):
            raise InvalidGuessError(f"Invalid guess - Each number must be between {MIN_VALUE} and {MAX_VALUE}")