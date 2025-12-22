from app import db
from app.models.gameSession import GameSession
from datetime import datetime
from flask import jsonify

def check_game_outcome(game: GameSession, correct_positions: int, feedback: dict):
    if correct_positions == game.code_length:
        game.is_over = True
        game.win = True
        game.session_ended = datetime.utcnow()
        db.session.commit()
        return {
            "message": "🥳 Congrats! You cracked the secret code!!! 🥳",
            "feedback": feedback
        }

    if game.attempts_remaining <= 0:
        game.is_over = True
        game.win = False
        game.session_ended = datetime.utcnow()
        db.session.commit()
        return {
            "message": "❌ Game Over - No more attempts left ❌",
            "secret_code": game.secret_code,
            "feedback": feedback
        }
    
    db.session.commit()
    return None