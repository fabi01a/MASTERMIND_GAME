import time
from app.utils.terminal import term
from math import floor
from blessed import Terminal
from .flush_helper import flush_input


def roundxy(x, y):
    return int(floor(x)), int(floor(y))


def splash_screen():
    title = "MASTERMIND"
    subtitle = "Press any key to begin"

    # Ball position & velocity
    x, y = 2, 2
    xs, ys = 0.6, 0.35

    with term.cbreak():
        print(term.clear())

        flush_input()

        while True:
            # Check for ANY key
            key = term.inkey(timeout=0.02)
            if key and not key.is_sequence:
                print(term.clear(), end="")
                print(term.move_xy(0, 1) + term.red(f"DEBUG key: {repr(key)}"))
                time.sleep(1)

                break

            # Erase previous ball
            erase_x, erase_y = roundxy(x, y)
            print(term.move_xy(erase_x, erase_y) + " ", end="")

            # Bounce logic
            if x <= 0 or x >= term.width - 1:
                xs *= -1
            if y <= 0 or y >= term.height - 1:
                ys *= -1

            # Move ball
            x += xs
            y += ys

            # Draw ball
            draw_x, draw_y = roundxy(x, y)
            print(term.move_xy(draw_x, draw_y) + term.bright_green("█"), end="")

            # Draw title (foreground, stable)
            center_y = term.height // 2
            print(
                term.move_xy(0, center_y)
                + term.bold(term.center(title))
            )
            print(
                term.move_xy(0, center_y + 2)
                + term.center(term.bright_green(subtitle))
)

            print(end="", flush=True)

