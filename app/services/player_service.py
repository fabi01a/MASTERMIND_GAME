from app.models.player import Player
from app import db

def get_or_create_player(player_name: str) -> Player:
    player = Player.query.filter_by(player_name=player_name).first()
    
    if player:
        return player, True
    
    player = Player(player_name=player_name)
    db.session.add(player)
    db.session.commit()
    return player, False