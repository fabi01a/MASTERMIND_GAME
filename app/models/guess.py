from app.extensions import db


class Guess(db.Model):
    guess_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_session_id = db.Column(
        db.Integer, db.ForeignKey("game_session.game_session_id"), nullable=False
    )
    guess_value = db.Column(db.JSON, nullable=False)
    correct_positions = db.Column(db.Integer, nullable=False)
    correct_numbers = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (
            f"<Game Session ID {self.game_session_id} - "
            f"Player: {self.game_session.player.player_name} - "
            f"Guess ID: {self.guess_id} - "
            f"Guess Value: {self.guess_value}>"
        )
