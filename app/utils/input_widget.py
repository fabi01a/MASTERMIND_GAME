import time
from app.utils.terminal import term
from typing import Optional


def blinking_input(
    prompt_text: str,
    *,
    clear_screen: bool = True,
    ignore_space_bar: bool = False,
    digits_only: bool = False,
    max_length: Optional[int] = None,
) -> str:
    buffer = ""
    cursor_visible = True
    last_blink = time.time()
    BLINK_INTERVAL = 0.5  # seconds

    if clear_screen:
        print(term.clear(), end="", flush=True)
    else:
        print()

    with term.hidden_cursor():
        while True:
            now = time.time()

            # Toggle cursor visibility
            if now - last_blink >= BLINK_INTERVAL:
                cursor_visible = not cursor_visible
                last_blink = now

            # Build the line
            cursor = term.bright_green("▌") if cursor_visible else " "
            line = _render_input_line(prompt_text, buffer, cursor)

            # Redraw the SAME line
            print("\r" + line + " " * 10, end="", flush=True)
            key = term.inkey(timeout=0.05)

            if not key:
                continue

            if key.name == "KEY_ENTER":
                return buffer

            elif key.name == "KEY_BACKSPACE":
                buffer = buffer[:-1]
                continue

            if len(key) == 1 and not key.is_sequence:
                if not _accept_key(
                    key,
                    buffer=buffer,
                    digits_only=digits_only,
                    ignore_space_bar=ignore_space_bar,
                    max_length=max_length,
                ):
                    continue

                buffer += key


def _accept_key(
    key: str,
    *,
    digits_only: bool,
    ignore_space_bar: bool,
    max_length: Optional[int] = None,
    buffer: str,
) -> bool:
    """Determine whether a key should be accepted into the input buffer"""

    if ignore_space_bar and key == " ":
        return False

    if digits_only and not key.isdigit():
        return False

    if max_length is not None and len(buffer) >= max_length:
        return False

    return True


def _render_input_line(prompt_text: str, buffer: str, cursor: str) -> str:
    """Rendering the blinking input line"""
    return term.bright_green(prompt_text) + term.bright_green(buffer) + cursor
