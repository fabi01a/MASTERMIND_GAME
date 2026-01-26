
import time
from blessed import Terminal
# from cli_game import start_game
from app.utils.input_widget import blinking_input
from app.utils.screen_bounce import splash_screen
from app.screens.leaderboard_screen import show_leaderboard
from app.screens.gameplay_screen import start_game
from app.utils.flush_helper import flush_input

term = Terminal()

def main_menu():
    # with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    #     splash_screen()

    while True:
            # print(term.clear())
            # print(term.bold(term.center("MAIN MENU")))
            # print(term.center("[1] Start Game"))
            # print(term.center("[2] View Leaderboard"))
            # print(term.center("[Q] Quit"))

            # choice = blinking_input(term.green("\nChoose an option: ")).strip().lower()

            # if choice == "1":
            #     while True:
        played = start_game()

        if not played:
            print(term.firebrick1("Thanks for playing Mastermind - Goodbye!"))
            break
        
        again = input("Would you like to play again? (Y/N): ").strip().lower()
        # flush_input()

        if again == "y":
            print(term.clear())
            continue
        else:
            print(term.green("Thanks for playing Mastermind - Goodbye!"))
            time.sleep(2)
            break  # after game ends, return to menu

            # elif choice == "2":
            #     show_leaderboard()
            #     input(term.bold("Press ENTER to return to the menu."))

            # elif choice == "q":
            #     print(term.firebrick1("Goodbye!"))
            #     break

            # else:
            #     print(term.red("Invalid input."))

