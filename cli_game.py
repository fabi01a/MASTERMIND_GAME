from app.utils.flush_helper import flush_input
from app.screens.main_menu_screen import main_menu
from blessed import Terminal

term = Terminal()

def main():
    flush_input()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main_menu()

if __name__ == "__main__":
    main()