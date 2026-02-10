from app.extensions import db

class GameSession(db.Model):
    game_session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    
    code_length = db.Column(db.Integer,nullable=False)
    difficulty = db.Column(db.String(10), default='easy', nullable=False)
    
    secret_code = db.Column(db.JSON, nullable=False)
    
    attempts_remaining = db.Column(db.Integer, nullable=False)
    max_attempts = db.Column(db.Integer, nullable=False)
    
    is_over = db.Column(db.Boolean, default=False)
    win = db.Column(db.Boolean, nullable=True)
    session_ended = db.Column(db.DateTime, nullable=True)
    
    guesses = db.relationship('Guess', backref='game_session')

    @property
    def in_progress(self) -> bool:
        return not self.is_over
    
    @property
    def has_ended(self) -> bool:
        return self.is_over

    def __repr__(self):
        return (
            f"<Game Session id={self.game_session_id} "
            f"player_id={self.player_id} "
            f"difficulty={self.difficulty}>"
        )