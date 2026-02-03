from app.utils.terminal import term
from app.screens.leaderboard_screen import show_leaderboard
from app.utils.input_widget import blinking_input

def handle_game_over(player_name: str) -> bool:
    print("DEBUG: Entered handle_game_over()")

    show_leaderboard()

    while True:
        print()
        replay = input("\nWould you like to play again? (Y/N): ").strip().lower()

        if replay == "y":
            return True
        elif replay == "n":
            print(term.cyan("\nThanks for playing! See you next time."))
            return False
        else:
            print(term.move_up + term.clear_eol, end="")
            print(term.firebrick1("Invalid input. Please enter Y or N."))