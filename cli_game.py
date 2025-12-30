from app.screens.gameplay_screen import start_game
from blessed import Terminal

term = Terminal()

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        start_game()

if __name__ == "__main__":
    main()