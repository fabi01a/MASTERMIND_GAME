import time
from app.utils.input_widget import blinking_input
from app.utils.terminal import term
from app.utils.flush_helper import flush_input

def prompt_player_name() -> str:
    """
    Prompt the user to enter a valid name. Repeats until non-empty.
    """
    flush_input()
    while True:
        name = blinking_input("Enter your player name: ").strip().lower()
        if name:
            return name
        print(term.firebrick1("Player name cannot be empty. Please try again."))
        time.sleep(1)

def prompt_difficulty() -> str:
    """
    Prompt the user to enter difficulty level: 1 (easy), 2 (hard), L (leaderboard), or Q (quit).
    Validates input and loops until valid.
    """
    choice = blinking_input(
        "", clear_screen=False, ignore_space_bar=True
    ).strip()

    if choice == "1":
        return "easy"
    elif choice == "2":
        return "hard"
    elif choice == "L":
        return "leaderboard"
    elif choice == "Q":
        return "quit"
    else:
        return "invalid"