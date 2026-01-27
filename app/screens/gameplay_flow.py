import time
import requests
from app.utils.input_widget import blinking_input
from app.screens.render_ui import draw_ui
from app.utils.terminal import term
# from app.utils.leaderboard import show_leaderboard

API_URL = "http://127.0.0.1:5000"

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
    show_welcome_once = True

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
            if len(guess) != code_length or any(d < 0 or d > 7 for d in guess):
                raise ValueError
        except ValueError:
            print(term.firebrick1(
                f"Invalid input: Please enter exactly {code_length} digits between 0 - 7"
            ))
            time.sleep(2)
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            continue

        # === SEND TO BACKEND ===
        try:
            res = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
            result = res.json()
        except Exception as e:
            print(term.firebrick1(f"Failed to submit guess: {e}"))
            break

        if res.status_code != 200:
            print(term.firebrick1(f"Error: {result.get('error', 'Something went wrong.')}"))
            break

        # === PROCESS FEEDBACK ===
        guesses.append(guess)
        feedbacks.append(result["feedback"])
        attempts_remaining = result.get("attempts_remaining", 0)

        draw_ui(term, guesses, feedbacks, attempts_remaining)
        print(term.aquamarine(result["message"]))
        show_welcome_once = False

        # === WIN / LOSE CHECK ===
        if result["message"].startswith("🥳"):
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            print(term.green(result["message"]))
            time.sleep(4)
            break

        elif result["message"].startswith("❌"):
            draw_ui(term, guesses, feedbacks, 0)
            print(term.firebrick1(result["message"]))
            print(term.greenyellow(f"The secret code was: {result['secret_code']}"))
            time.sleep(4)
            break

    # === GAME OVER CLEANUP ===
    print(term.aquamarine + term.bold(f"\nThanks for playing, {player_name}!"))
    print()

    from app.screens.leaderboard_screen import show_leaderboard
    show_leaderboard()

    return True


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
