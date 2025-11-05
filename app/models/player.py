from app import db

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_name = db.Column(db.String(20), unique=True)
    game_sessions = db.relationship('GameSession', backref='player')