# review
from app.utils.terminal import term
from math import floor
from .flush_helper import flush_input


def roundxy(x, y):
    return int(floor(x)), int(floor(y))


def splash_screen():
    title = "MASTERMIND"
    subtitle = "Press any key to begin"

    # Ball position & velocity
    x, y = 2, 2
    xs, ys = 0.6, 0.35

    with term.cbreak(), term.hidden_cursor():
        print(term.clear())
        flush_input()

        while True:
            # Check for ANY key
            key = term.inkey(timeout=0.02)
            if key:
                flush_input()
                print(term.clear())
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
            print(term.move_xy(0, center_y) + term.bold(term.center(title)))
            print(
                term.move_xy(0, center_y + 2) + term.center(term.bright_green(subtitle))
            )
            print(end="", flush=True)
