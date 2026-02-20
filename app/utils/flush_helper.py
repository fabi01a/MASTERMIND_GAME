# review
import sys
import select
import termios
import tty


def flush_input():
    """Robustly flush stdin input buffer on Unix-like systems."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # Set to raw read mode
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
