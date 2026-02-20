# review
from blessed import Terminal
from app.screens.gameplay_screen import start_game

term = Terminal()


def main_menu():
    while True:
        played = start_game()

        if not played:
            print(term.firebrick1("Thanks for playing Mastermind - Goodbye!"))
            break
