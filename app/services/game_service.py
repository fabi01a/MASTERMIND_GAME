from app.models.gameSession import GameSession
from app.models.player import Player
from app import db

def create_game_session(player_id: int, secret_code: list[int], code_length: int=4):
    new_game = GameSession(
        player_id=player_id,
        secret_code=secret_code,
        attempts_remaining=10,
        code_length=code_length
    )
    db.session.add(new_game)
    db.session.commit()
    return new_game