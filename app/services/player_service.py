from app.models.player import Player
from app import db

def get_or_create_player(player_name: str) -> Player:
    normalized_name = player_name.lower()
    player = Player.query.filter_by(normalized_name=normalized_name).first()
    if player:
        return player, True
    
    player = Player(player_name=player_name, normalized_name=normalized_name)
    db.session.add(player)
    db.session.commit()
    return player, False