from sqlalchemy import asc
from app.extensions import db
from app.models.game_session import GameSession
from app.models.player import Player


def get_top_leaderboard(limit=10):
    """Return top players by fewest attempts used to win a game."""
    return (
        db.session.query(
            GameSession.game_session_id,
            Player.player_name,
            GameSession.difficulty,
            (GameSession.max_attempts - GameSession.attempts_remaining).label(
                "attempts_used"
            ),
            GameSession.session_ended,
        )
        .join(Player, GameSession.player_id == Player.player_id)
        .filter(GameSession.win == True, GameSession.is_over == True)
        .order_by(asc("attempts_used"), GameSession.session_ended)
        .limit(limit)
        .all()
    )
