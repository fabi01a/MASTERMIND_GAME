from dataclasses import dataclass
from app.models.gameSession import GameSession
from app.models.player import Player
from app.services.player_service import get_or_create_player
from app.utils.difficulty_config import get_difficulty_settings
from app.utils.secret_code_generation import generate_secret_code
from app.utils.normalization import normalize_name

from app import db

@dataclass
class GameInitResult:
    game: GameSession
    player: Player
    message: str

def initialize_new_game(raw_name: str, difficulty: str) -> GameInitResult:
    normalized_name = normalized_name(raw_name)
    player, is_returning = get_or_create_player(normalized_name)

    settings = get_difficulty_settings(difficulty)
    code_length = settings.code_length
    max_attempts = settings.max_attempts

    secret_code = generate_secret_code(code_length)
    game_sesh = create_game_session(
        player_id=player.player_id, 
        secret_code=secret_code, 
        code_length=code_length,
        max_attempts=max_attempts,
        difficulty=difficulty
    )

    message = (
        f"Welcome back, {raw_name}! New game created - Good Luck!"
        if is_returning else
        f"New game created - Good Luck {raw_name}!"
    )

    return GameInitResult(game=game_sesh, player=player, message=message)


def create_game_session(player_id: int, secret_code: list[int], code_length: int, max_attempts: int, difficulty: str):
    new_game = GameSession(
        player_id=player_id,
        secret_code=secret_code,
        attempts_remaining=max_attempts,
        code_length=code_length,
        max_attempts=max_attempts,
        difficulty=difficulty
    )
    db.session.add(new_game)
    db.session.commit()
    return new_game