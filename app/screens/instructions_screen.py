from app.utils.terminal import term
from app.utils.ui_helpers import render_screen_title


def render_instructions(welcome_message, horizontal_border):
    print(term.clear())
    render_screen_title(term, "👾 MASTERMIND 👾")
    print()
    print(term.white + term.center(term.bold(("Game Rules:"))))
    print(term.darkorchid2(term.center(term.bold("-----------"))))
    print(term.springgreen(term.center(" Guess the secret number code")))
    print(term.olivedrab1(term.center(" Use only numbers from 0 to 7")))
    print(term.palevioletred1(term.center("    • [Easy] level uses 4 digits")))
    print(term.darkorchid2(term.center("    • [Hard] level uses 6 digits")))
    print()
    print(term.white(term.center(" After each guess, the game will tell you:")))
    print(
        term.bright_green(
            term.center("      • How many digits are correct and in the correct place")
        )
    )
    print(
        term.olivedrab1(
            term.center("      • How many digits are correct but in the wrong place")
        )
    )
    print()
    print(
        term.springgreen(
            term.center(term.bold("→ The secret code may contain repeated digits"))
        )
    )
    print(term.white(term.center(term.bold(" You have 10 attempts to crack the code"))))
    print()

    if welcome_message:
        print(term.cyan(term.center(welcome_message)))

    print(term.bold("Choose your difficulty level:"))
    print(term.palevioletred1("\n[1] - Easy [4-digit code]"))
    print(term.darkorchid2("[2] - Hard [6-digit code]"))
    print(term.firebrick1("\nType Q to end the game early"))
    print(term.bold + term.bright_green("Enter 1 or 2 and press ENTER to begin"))
    print(term.bold + term.olivedrab1("Enter L to view the leaderboard"))
