# review
from app.utils.terminal import term


def generate_horizontal_border(term, char: str = "X") -> str:
    return char * term.width


def render_screen_title(term, title: str, border_char: str = "X"):
    horizontal_border = generate_horizontal_border(term, border_char)
    print(term.bright_green + term.bold(horizontal_border))
    print(term.olivedrab1 + term.bold(term.center(title)))
    print(term.bright_green + term.bold(horizontal_border))


def render_game_started_screen(welcome_message: str, attempts_remaining: int):
    """
    Displays the initial 'Game Started' screen.
    """
    print(term.clear())
    width = term.width
    horizontal_border = "X" * width

    print(term.bright_green(term.bold(horizontal_border)))
    print(term.white(term.bold(term.center("👾 GAME STARTED 👾"))))
    print(term.bright_green(term.bold(horizontal_border)))
    print()

    if welcome_message:
        print(term.olivedrab1(term.center(welcome_message)))
        print()

    print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))
