from app.screens.gameplay_screen import start_game
from app.utils.screen_bounce import splash_screen
from app.screens.main_menu_screen import main_menu
from blessed import Terminal

term = Terminal()
# def run_game():
#     splash_screen()
#     main_menu()

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        run_game()

def run_game():
    splash_screen()
    main_menu()


if __name__ == "__main__":
    main()