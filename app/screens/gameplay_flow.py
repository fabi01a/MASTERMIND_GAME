import time
import requests
from app.api.api_client import send_guess
from app.utils.input_widget import blinking_input
from app.screens.render_ui import draw_ui
from app.utils.terminal import term
from app.utils.validation import validate_guess_input
from app.utils.exceptions import InvalidGuessError
from app.utils.game_helpers import process_guess_feedback
from app.utils.game_outcome_utils import interpret_game_outcome
from app.services.game_outcome_service import check_game_outcome
from app.utils.handle_game_flow_helpers import handle_game_over
# from app.utils.leaderboard import show_leaderboard


def run_game_loop(player_name: str, game_data: dict) -> bool:
    """
    Handles the full game loop once the game has been initialized.
    """
    game_id = game_data["game_id"]
    attempts_remaining = game_data["max_attempts"]
    code_length = game_data["code_length"]
    welcome_message = game_data.get("message", "")
    guesses = []
    feedbacks = []

    _render_game_started_screen(welcome_message, attempts_remaining)

    while attempts_remaining > 0:
        guess_input = blinking_input(
            term.greenyellow(f"Enter your {code_length}-digit guess: "),
            clear_screen=False,
            digits_only=True,
            max_length=code_length
        ).strip()

        if guess_input.upper() == "Q":
            print(term.firebrick1("\nYou've ended the game early. Goodbye!"))
            break

        # === VALIDATE INPUT ===
        try:
            guess = [int(d) for d in guess_input if d.isdigit()]
            validate_guess_input(guess, code_length)
        except (ValueError, InvalidGuessError) as e:
            print(term.firebrick1(f"Invalid input: {e}"))
            time.sleep(2)
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            continue

        # === SEND TO BACKEND ===
        try:
            result = send_guess(game_id, guess)
        except RuntimeError as e:
            print(term.firebrick1(str(e)))
            break

        # === PROCESS FEEDBACK ===
        attempts_remaining = process_guess_feedback(
            guess, result, guesses, feedbacks, attempts_remaining
        )
        
        # === WIN / LOSE CHECK ===
        outcome = interpret_game_outcome(result)

        if outcome == "win":
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            print(term.green(result["message"]))
            time.sleep(4)
            break

        elif outcome == "lose":
            draw_ui(term, guesses, feedbacks, 0)
            print(term.firebrick1(result["message"]))
            print(term.greenyellow(f"The secret code was: {result['secret_code']}"))
            time.sleep(4)
            break
    
    handle_game_over(player_name)


def _render_game_started_screen(welcome_message: str, attempts_remaining: int):
    print(term.clear())
    width = term.width
    horizontal_border = "X" * width

    print(term.bright_green + term.bold(horizontal_border))
    print(term.bright_green + term.bold(term.center("GAME STARTED")))
    print(term.bright_green + term.bold(horizontal_border))
    print()

    if welcome_message:
        print(term.greenyellow(term.center(welcome_message)))
        print()

    print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))
