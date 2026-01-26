import time
from blessed import Terminal
from app.utils.input_widget import blinking_input
from app.utils.screen_bounce import splash_screen
from app.screens.leaderboard_screen import show_leaderboard
from app.screens.gameplay_screen import start_game
from app.utils.flush_helper import flush_input

term = Terminal()

def main_menu():
    while True:
        played = start_game()

        if not played:
            print(term.firebrick1("Thanks for playing Mastermind - Goodbye!"))
            break
        
        again = input("Would you like to play again? (Y/N): ").strip().lower()

        if again == "y":
            print(term.clear())
            continue
        else:
            print(term.green("Thanks for playing Mastermind - Goodbye!"))
            time.sleep(2)
            break  # after game ends, return to menu

