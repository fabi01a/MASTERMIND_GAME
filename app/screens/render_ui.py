from app.utils.terminal import term

def draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=False, welcome_message=None):
    print(term.clear())
    width = term.width
    horizontal_border = "X" * width

    # === HEADER ===
    print(term.bright_green + term.bold(horizontal_border))
    print(term.olivedrab1 + term.bold(term.center("MASTERMIND - THE GAME")))
    print(term.bright_green + term.bold(horizontal_border))

    # === INSTRUCTIONS VIEW ===
    if show_instructions:
        _render_instructions(welcome_message, horizontal_border)
        return

    # === GAME TABLE HEADER ===
    _render_feedback_table(guesses, feedbacks, attempts_remaining)


def _render_instructions(welcome_message, horizontal_border):
    print(term.bold + term.center("Game Rules:"))
    print(term.bold + term.center("-----------"))
    print(term.center(" Guess the secret number code"))
    print(term.olivedrab1 + term.center(" Use only numbers from 0 to 7"))
    print(term.palevioletred1 + term.center("    • [Easy] level uses 4 digits"))
    print(term.darkorchid2 + term.center("    • [Hard] level uses 6 digits"))
    print()
    print(term.white + term.center(" After each guess, the game will tell you:"))
    print(term.seagreen1 + term.center("      • How many digits are correct and in the correct place"))
    print(term.springgreen3 + term.center("      • How many digits are correct but in the wrong place"))
    print()
    print(term.olivedrab1 + term.center("The secret code may contain repeated digits"))
    print(term.white + term.center(" You have 10 attempts to crack the code"))
    print(term.bright_green + term.bold(horizontal_border))
    print()

    if welcome_message:
        print(term.cyan(term.center(welcome_message)))

    print(term.bold("Choose your difficulty level:"))
    print(term.palevioletred1("\n[1] - Easy [4-digit code]"))
    print(term.darkorchid2("[2] - Hard [6-digit code]"))    
    print(term.firebrick1("\nType Q to end the game early"))
    print(term.bold + term.bright_green("Enter 1 or 2 and press ENTER to begin"))
    print(term.bold + term.lawngreen("Enter L to view the leaderboard"))


def _render_feedback_table(guesses, feedbacks, attempts_remaining):
    ATTEMPT_W = 11
    GUESS_W = 18
    CORRECT_DIGITS_W = 19
    CORRECT_POS_W = 37
    PIPE = term.olivedrab2 + "|" + term.white

    border = term.olivedrab2 + (
        "+" + "-" * ATTEMPT_W +
        "+" + "-" * GUESS_W +
        "+" + "-" * CORRECT_DIGITS_W +
        "+" + "-" * CORRECT_POS_W + "+"
    )

    if guesses:
        print(term.olivedrab2 + term.center(border))

        header_row = (
            term.bold +
            PIPE + f"{'Attempt':^{ATTEMPT_W}}" +
            PIPE + f"{'Your Guess':^{GUESS_W}}" +
            PIPE + f"{'Correct Digit':^{CORRECT_DIGITS_W}}" +
            PIPE + f"{'Correct Digit & Correct Position':^{CORRECT_POS_W}}" +
            PIPE
        )
        print(term.center(header_row))
        print(term.olivedrab2 + term.center(border))

        for i, guess in enumerate(guesses, start=1):
            fb = feedbacks[i - 1]
            guess_str = " ".join(map(str, guess))

            row = (
                PIPE + f"{i:^{ATTEMPT_W}}" +
                PIPE + f"{guess_str:^{GUESS_W}}" +
                PIPE + f"{fb['correct_numbers']:^{CORRECT_DIGITS_W}}" +
                PIPE + f"{fb['correct_positions']:^{CORRECT_POS_W}}" +
                PIPE
            )

            print(term.center(term.white + row))
            print(term.olivedrab2 + term.center(border))

    print(term.white + term.bold(f"\nAttempts remaining: {attempts_remaining}"))
