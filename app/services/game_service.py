from app.models.gameSession import GameSession
from app.models.player import Player

from app import db

def create_game_session(player_id: int, secret_code: list[int]) -> GameSession:
    game_sesh = GameSession(
        player_id = player_id,
        secret_code = secret_code
    )
    db.session.add(game_sesh)
    db.session.commit ()
    return game_sesh