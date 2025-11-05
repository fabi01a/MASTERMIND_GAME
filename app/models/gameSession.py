# from app import db

class GameSession(db.Model):
    game_session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # timer = pass
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    # difficulty_level = pass
    secret_code = db.Column(db.JSON, nullable=False)
    attempts_remaining = db.Column(db.Integer,default=10)
    is_over = db.Column(db.Boolean, default=False)
    win = db.Column(db.Boolean, nullable=True)
    session_ended = db.Column(db.DateTime, nullable=True)
    # multi_player = pass
    guesses = db.relationship('Guess', backref='game_session')