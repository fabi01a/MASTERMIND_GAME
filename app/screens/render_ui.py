from app.utils.terminal import term
from app.utils.ui_helpers import render_screen_title, generate_horizontal_border
from app.screens.instructions_screen import render_instructions
from app.screens.feedback_table import render_feedback_table

def draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=False, welcome_message=None):
    print(term.clear())
    render_screen_title(term, "MASTERMIND - THE GAME")

    # === INSTRUCTIONS VIEW ===
    if show_instructions:
        horizontal_border = generate_horizontal_border(term)
        render_instructions(welcome_message, horizontal_border)
        return

    # === GAME TABLE HEADER ===
    render_feedback_table(guesses, feedbacks, attempts_remaining)

