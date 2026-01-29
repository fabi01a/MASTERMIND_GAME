from app.utils.terminal import term
from app.screens.leaderboard_screen import show_leaderboard

def handle_game_over(player_name: str):
    print(term.aquamarine + term.bold(f"\nThanks for playing, {player_name}!"))
    print()
    show_leaderboard()
