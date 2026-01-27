import requests
from app.api.api_client import create_game
from app.screens.leaderboard_screen import show_leaderboard
from app.screens.render_ui import draw_ui, _render_instructions
from app.utils.screen_bounce import splash_screen
from app.utils.input_widget import blinking_input
from app.utils.terminal import term
from blessed import Terminal
import time
from app.utils.flush_helper import flush_input
from app.utils.input_helpers import prompt_player_name, prompt_difficulty
from app.utils.error_helpers import show_game_creation_error
from app.screens.gameplay_flow import run_game_loop


def start_game():
    splash_screen() #user presses 1 key to move on
    flush_input() #discard that key immediately

    player_name = prompt_player_name()
    welcome_message = None

    width = term.width
    horizontal_border = "X" * width
    _render_instructions(welcome_message, horizontal_border)
    
    difficulty = prompt_valid_difficulty(welcome_message, horizontal_border)
    if difficulty is None:
        return False
    
    try:
        response_data = create_game(player_name, difficulty)
    except Exception as e:
        show_game_creation_error(e)
        return False
    
    return run_game_loop(player_name, response_data)


def prompt_valid_difficulty(welcome_message, horizontal_border):
    """
    Handles difficulty selection loop.
    Returns:
        "easy" | "hard" if selected
        None if the user quits
    """
    while True:
        difficulty_choice = prompt_difficulty()

        if difficulty_choice == "Q":
            print(term.firebrick1("\nYou've ended the game early. Goodbye!"))
            time.sleep(2)
            return None

        if difficulty_choice == "L":
            show_leaderboard()
            _render_instructions(welcome_message, horizontal_border)
            continue

        if difficulty_choice == "invalid":
            print(
                term.firebrick1(
                    "Invalid input: Please enter 1 for Easy - 2 for Hard - "
                    "L to view Leaderboard - or Q to Quit game early"
                )
            )
            time.sleep(1.5)
            _render_instructions(welcome_message, horizontal_border)
            continue

        # Valid difficulty
        return "easy" if difficulty_choice == "1" else "hard"
