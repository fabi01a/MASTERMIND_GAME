from app.utils.terminal import term
from app.screens.render_ui import draw_ui

def process_guess_feedback(
    guess: list[int],
    result: dict,
    guesses: list,
    feedbacks: list,
    attempts_remaining: int
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
