from app.utils.terminal import term


def render_feedback_table(guesses, feedbacks, attempts_remaining):
    config = _table_config()

    _render_table_header(config)

    if guesses:
        _render_table_rows(config, guesses, feedbacks)

    _render_attempts_remaining(attempts_remaining)
    print(term.normal, end="")


def _table_config():
    ATTEMPT_W = 11
    GUESS_W = 18
    CORRECT_DIGITS_W = 19
    CORRECT_POS_W = 37

    PIPE = "|"
    BORDER = (
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
    print(term.olivedrab2(term.center(cfg["BORDER"])))

    header_row = (
        term.olivedrab2(cfg["PIPE"])
        + term.darkorchid2(f"{'Attempt':^{cfg['ATTEMPT_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.darkorchid2(f"{'Your Guess':^{cfg['GUESS_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.darkorchid2(f"{'Correct Digit':^{cfg['CORRECT_DIGITS_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.darkorchid2(
            f"{'Correct Digit & Correct Position':^{cfg['CORRECT_POS_W']}}"
        )
        + term.olivedrab2(cfg["PIPE"])
    )

    print(term.center(term.bold(header_row)))
    print(term.olivedrab2(term.center(cfg["BORDER"])))


def _render_table_rows(cfg, guesses, feedbacks):
    for i, guess in enumerate(guesses, start=1):
        _render_row(cfg, i, guess, feedbacks[i - 1])
        print(term.olivedrab2(term.center(cfg["BORDER"])))


def _render_row(cfg, attempt_num, guess, feedback):
    guess_str = " ".join(map(str, guess))

    row = (
        term.olivedrab2(cfg["PIPE"])
        + term.white(f"{attempt_num:^{cfg['ATTEMPT_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.white(f"{guess_str:^{cfg['GUESS_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.white(f"{feedback['correct_numbers']:^{cfg['CORRECT_DIGITS_W']}}")
        + term.olivedrab2(cfg["PIPE"])
        + term.white(f"{feedback['correct_positions']:^{cfg['CORRECT_POS_W']}}")
        + term.olivedrab2(cfg["PIPE"])
    )

    print(term.center(term.white(row)))


def _render_attempts_remaining(attempts_remaining):
    print(term.white + term.bold(f"\nAttempts remaining: {attempts_remaining}"))
