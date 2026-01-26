from app.screens.gameplay_screen import start_game
from app.utils.screen_bounce import splash_screen
from app.utils.flush_helper import flush_input
from app.screens.main_menu_screen import main_menu
from blessed import Terminal

term = Terminal()
print(term.red("DEBUG: CLI_GAME.PY STARTED"))

def main():
    flush_input()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        main_menu()
#         run_game()

# def run_game():
#     flush_input()
#     main_menu()


if __name__ == "__main__":
    main()