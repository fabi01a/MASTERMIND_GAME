from blessed import Terminal
from app.utils.flush_helper import flush_input  # adjust path as needed

term = Terminal()

def test_keypress_behavior():
    with term.cbreak(), term.hidden_cursor():
        print(term.clear())
        print(term.bold("Test: Press any key to continue..."))

        flush_input()  # Ensure input buffer is clear
        key = term.inkey()
        print(f"DEBUG: First key received: {repr(key)}")

        flush_input()  # Clear again
        print(term.bold("Now press one more key to confirm..."))
        key2 = term.inkey()
        print(f"DEBUG: Second key received: {repr(key2)}")

if __name__ == "__main__":
    test_keypress_behavior()
