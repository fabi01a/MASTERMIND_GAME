from app.utils.terminal import term


def render_feedback_table(guesses, feedbacks, attempts_remaining):
    config = _table_config()

    if guesses:
        _render_table_header(config)
        _render_table_rows(config, guesses, feedbacks)

    _render_attempts_remaining(attempts_remaining)


def _table_config():
    ATTEMPT_W = 11
    GUESS_W = 18
    CORRECT_DIGITS_W = 19
    CORRECT_POS_W = 37

    PIPE = term.olivedrab2 + "|" + term.white
    BORDER = term.olivedrab2 + (
        "+"
        + "-" * ATTEMPT_W
        + "+"
        + "-" * GUESS_W
        + "+"
        + "-" * CORRECT_DIGITS_W
        + "+"
        + "-" * CORRECT_POS_W
        + "+"
    )

    return {
        "ATTEMPT_W": ATTEMPT_W,
        "GUESS_W": GUESS_W,
        "CORRECT_DIGITS_W": CORRECT_DIGITS_W,
        "CORRECT_POS_W": CORRECT_POS_W,
        "PIPE": PIPE,
        "BORDER": BORDER,
    }


def _render_table_header(cfg):
    print(term.olivedrab2 + term.center(cfg["BORDER"]))

    header_row = (
        term.bold
        + cfg["PIPE"]
        + f"{'Attempt':^{cfg['ATTEMPT_W']}}"
        + cfg["PIPE"]
        + f"{'Your Guess':^{cfg['GUESS_W']}}"
        + cfg["PIPE"]
        + f"{'Correct Digit':^{cfg['CORRECT_DIGITS_W']}}"
        + cfg["PIPE"]
        + f"{'Correct Digit & Correct Position':^{cfg['CORRECT_POS_W']}}"
        + cfg["PIPE"]
    )
    print(term.center(header_row))
    print(term.olivedrab2 + term.center(cfg["BORDER"]))


def _render_table_rows(cfg, guesses, feedbacks):
    for i, guess in enumerate(guesses, start=1):
        _render_row(cfg, i, guess, feedbacks[i - 1])
        print(term.olivedrab2 + term.center(cfg["BORDER"]))


def _render_row(cfg, attempt_num, guess, feedback):
    guess_str = " ".join(map(str, guess))

    row = (
        cfg["PIPE"]
        + f"{attempt_num:^{cfg['ATTEMPT_W']}}"
        + cfg["PIPE"]
        + f"{guess_str:^{cfg['GUESS_W']}}"
        + cfg["PIPE"]
        + f"{feedback['correct_numbers']:^{cfg['CORRECT_DIGITS_W']}}"
        + cfg["PIPE"]
        + f"{feedback['correct_positions']:^{cfg['CORRECT_POS_W']}}"
        + cfg["PIPE"]
    )

    print(term.center(term.white + row))


def _render_attempts_remaining(attempts_remaining):
    print(term.white + term.bold(f"\nAttempts remaining: {attempts_remaining}"))
