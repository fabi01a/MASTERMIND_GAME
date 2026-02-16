import time
from app.screens.render_ui import draw_ui
from app.utils.terminal import term
from app.screens.leaderboard_screen import show_leaderboard
from app.utils.input_widget import blinking_input


def handle_game_over(player_name: str) -> bool:
    show_leaderboard()

    while True:
        print()
        replay = input("\nWould you like to play again? (Y/N): ").strip().lower()

        if replay == "y":
            return True
        elif replay == "n":
            print(term.cyan("\nThanks for playing! See you next time."))
            return False
        else:
            print(term.move_up + term.clear_eol, end="")
            print(term.firebrick1("Invalid input. Please enter Y or N."))


def display_error_and_redraw(
    error_message: str,
    guesses: list,
    feedbacks: list,
    attempts_remaining: int,
    delay: float = 1.5,
):
    print(term.clear())
    draw_ui(term, guesses, feedbacks, attempts_remaining)
    print(term.firebrick1(error_message))
    time.sleep(delay)
    print(term.clear())
    draw_ui(term, guesses, feedbacks, attempts_remaining)


def process_guess_feedback(
    guess: list[int],
    result: dict,
    guesses: list,
    feedbacks: list,
    attempts_remaining: int,
) -> int:
    """
    Appends the new guess and feedback to the tracking lists,
    redraws the UI, and returns updated attempts remaining.
    """
    guesses.append(guess)
    feedbacks.append(result["feedback"])
    attempts_remaining = result.get("attempts_remaining", 0)

    draw_ui(term, guesses, feedbacks, attempts_remaining)
    print(term.aquamarine(result["message"]))

    return attempts_remaining
