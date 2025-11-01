class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(20), unique=True)
    game_sessions = db.relationship('GameSession', backref='player')

class GameSession(db.Model):
    game_session_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # timer = pass
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    # difficulty_level = pass
    attempts_remaining = db.Column(db.Integer,default=10)
    is_over = db.Column(db.Boolean, default=False)
    win = db.Column(db.Boolean, nullable=True)
    session_ended = db.Column(db.DateTime, nullable=True)
    # multi_player = pass
    guesses = db.relationship('Guess', backref='game_session')

class Guess(db.Model):
    guess_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_session_id = db.Column(
        db.Integer, 
        db.ForeignKey('game_session.game_session_id'),
        nullable=False
    )
    guess_value = db.Column(db.JSON, nullable=False)
    correct_positions = db.Column(db.Integer, nullable=False)
    correct_numbers = db.Column(db.Integer, nullable=False)