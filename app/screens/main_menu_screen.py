from blessed import Terminal
# from cli_game import start_game
from app.utils.input_widget import blinking_input
from app.utils.screen_bounce import splash_screen
from app.screens.leaderboard_screen import show_leaderboard
from app.screens.gameplay_screen import start_game

term = Terminal()

def main_menu():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        splash_screen()

        while True:
            print(term.clear())
            print(term.bold(term.center("MAIN MENU")))
            print(term.center("[1] Start Game"))
            print(term.center("[2] View Leaderboard"))
            print(term.center("[Q] Quit"))

            choice = blinking_input(term.green("\nChoose an option: ")).strip().lower()

            if choice == "1":
                start_game()
                break  # after game ends, return to menu
            elif choice == "2":
                show_leaderboard()
            elif choice == "q":
                print(term.firebrick1("Goodbye!"))
                break
            else:
                print(term.red("Invalid input."))