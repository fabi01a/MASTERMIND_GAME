import time
from app.utils.terminal import term
from blessed import Terminal
from typing import Optional

def blinking_input(
        prompt_text:str, 
        *, 
        clear_screen: bool = True,
        ignore_space_bar: bool = False,
        digits_only: bool = False,
        max_length: int = None,
) -> str:
    buffer = ""
    cursor_visible = True
    last_blink = time.time()
    BLINK_INTERVAL = 0.5  # seconds
    
    if clear_screen:
        print(term.clear(), end="", flush=True)
    else:
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
        print("\r" + line + " " * 10, end="", flush=True)

        key = term.inkey(timeout=0.05)
        
        if not key:
            continue

        if ignore_space_bar and key == " ":
            continue

        if key.name == "KEY_ENTER":
            return buffer

        elif key.name == "KEY_BACKSPACE":
            buffer = buffer[:-1]

        elif len(key) == 1 and not key.is_sequence:
                
            if digits_only and not key.isdigit():
                continue

            if max_length is not None and len(buffer) >= max_length:
                continue
            
            buffer += key

