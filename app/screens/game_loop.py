# app/screens/game_loop.py

import time
import requests
from app.utils.terminal import term
from app.utils.input_widget import blinking_input
from app.screens.render_ui import draw_ui
from app.screens.gameplay_flow import API_URL

def run_game_loop(game_id, code_length, player_name, attempts_remaining, guesses, feedbacks, welcome_message=None):
    show_welcome_once = True

    print(term.clear())
    width = term.width
    border = "X" * width

    print(term.bright_green + term.bold(border))
    print(term.bright_green + term.bold(term.center("GAME STARTED")))
    print(term.bright_green + term.bold(border))
    print()

    if show_welcome_once and welcome_message:
        print(term.greenyellow(term.center(welcome_message)))
        print()

    print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))

    while attempts_remaining > 0:
        guess_input = blinking_input(
            term.greenyellow(f"Enter your {code_length}-digit guess: "),
            clear_screen=False,
            digits_only=True,
            max_length=code_length
        )
        
        if guess_input.strip() == "Q":
            print(term.firebrick1("\nYou've ended the game early. Goodbye!"))
            break

        try:
            guess = [int(d) for d in guess_input if d.isdigit()]
            if len(guess) != code_length or any(d < 0 or d > 7 for d in guess):
                raise ValueError
        except ValueError:
            print(term.firebrick1(f"Invalid input: Please enter exactly {code_length} digits between 0 - 7"))
            time.sleep(2)
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            continue

        # Send to backend
        res = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
        result = res.json()
        show_welcome_once = False

        if res.status_code != 200:
            print(term.firebrick1(f"Error: {result.get('error', 'Something went wrong.')}"))
            break

        guesses.append(guess)
        feedbacks.append(result["feedback"])
        attempts_remaining = result.get("attempts_remaining", 0)

        draw_ui(term, guesses, feedbacks, attempts_remaining)
        print(term.aquamarine(result["message"]))

        # Check for win/lose message
        if result.get("message", "").startswith("🥳"):
            print(term.green(result["message"]))
            time.sleep(4)
            break
        elif result.get("message", "").startswith("❌"):
            print(term.firebrick1(result["message"]))
            print(term.greenyellow(f"The secret code was: {result['secret_code']}"))
            time.sleep(4)
            break

    print(term.aquamarine + term.bold(f"\nThanks for playing, {player_name}!"))
    print()
