import time
from blessed import Terminal

term = Terminal()

def blinking_input(prompt_text:str) -> str:
    buffer = ""
    cursor_visible = True
    last_blink = time.time()
    BLINK_INTERVAL = 0.5  # seconds

    with term.cbreak(), term.hidden_cursor():
        print()

        while True:
            now = time.time()

            # Toggle cursor visibility
            if now - last_blink >= BLINK_INTERVAL:
                cursor_visible = not cursor_visible
                last_blink = now
            
            # Build the line
            cursor = term.bright_green("▌") if cursor_visible else " "
            line = (
                term.bright_green(prompt_text)
                + term.bright_green(buffer)
                + cursor
            )

            #Redraw the SAME line
            print("\r" + line + " " * 5, end="", flush=True)

            key = term.inkey(timeout=0.05)

            if not key:
                continue

            if key.name == "KEY_ENTER":
                print()
                return buffer

            elif key.name == "KEY_BACKSPACE":
                buffer = buffer[:-1]

            elif len(key) == 1 and not key.is_sequence:
                buffer += key
