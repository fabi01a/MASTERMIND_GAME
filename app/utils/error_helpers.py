# review
from app.utils.terminal import term


def show_game_creation_error(error: Exception):
    print(term.clear())
    print(term.firebrick1("⚠️ Failed to start the game."))
    print(term.red(str(error)))
