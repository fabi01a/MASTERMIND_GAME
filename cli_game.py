import requests
from app.utils.screen_bounce import splash_screen
from blessed import Terminal
import time

term = Terminal()

API_URL = "http://127.0.0.1:5000"

def draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=False, welcome_message=None):
    print(term.clear()) #Calls the function
    width = term.width
    horizontal_border = "X" * width

    #Title / Box Design
    print(term.bright_green + term.bold(horizontal_border))
    print(term.olivedrab1 + term.bold(term.center("MASTERMIND - THE GAME")))
    print(term.bright_green + term.bold(horizontal_border))

    #Display the instructions
    if show_instructions:
        print(term.bold + term.center("Game Rules:")) 
        print(term.bold + term.center("-----------")) 
        print(term.center(" Guess the secret number code"))
        print(term.olivedrab1 + term.center(" Use only numbers from 0 to 7"))
        print(term.palevioletred1 + term.center("    • [Easy] level uses 4 digits"))
        print(term.darkorchid2 + term.center("    • [Hard] level uses 6 digits"))
        print()
        print(term.white + term.center(" After each guess, the game will tell you:"))
        print(term.seagreen1 + term.center("      • How many digits are correct and in the correct place"))
        print(term.springgreen3 + term.center("      • How many digits are correct but in the wrong place"))
        print()
        print(term.olivedrab1 + term.center(" You have 10 attempts to crack the code"))
        print(term.bright_green + term.bold(horizontal_border))
        print()
    
        if welcome_message:
            print(term.cyan(term.center(welcome_message)))

        print(term.bold("Choose your difficulty level:"))
        print(term.palevioletred1("\n[1] - Easy [4-digit code]"))
        print(term.darkorchid2("[2] - Hard [6-digit code]"))    
        print(term.firebrick1("\nType Q to end the game early"))
        return

    # ==================
    # TABLE CONFIG
    # ==================
    ATTEMPT_W = 11
    GUESS_W = 18
    CORRECT_DIGITS_W = 19
    CORRECT_POS_W = 37
    PIPE = term.olivedrab2 + "|" + term.white

    border = term.olivedrab2 + (
        "+" + "-" * ATTEMPT_W +
        "+" + "-" * GUESS_W +
        "+" + "-" * CORRECT_DIGITS_W +
        "+" + "-" * CORRECT_POS_W + "+"
    )

    # ==================
    # TABLE RENDERING
    # ==================
    if guesses:
        print(term.olivedrab2 + term.center(border))
        
        header_row = (
            term.bold + 
            PIPE + f"{'Attempt':^{ATTEMPT_W}}" +
            PIPE + f"{'Your Guess':^{GUESS_W}}" +
            PIPE + f"{'Correct Digit':^{CORRECT_DIGITS_W}}" +
            PIPE + f"{'Correct Digit & Correct Position':^{CORRECT_POS_W}}" +
            PIPE
        )
        print(term.center(header_row))
        print(term.olivedrab2 + term.center(border))

        for i, guess in enumerate(guesses, start=1):
            fb = feedbacks[i - 1]
            guess_str = " ".join(map(str,guess))

            row = (
                PIPE + f"{i:^{ATTEMPT_W}}" +
                PIPE + f"{str(guess):^{GUESS_W}}" +
                PIPE + f"{fb['correct_numbers']:^{CORRECT_DIGITS_W}}" +
                PIPE + f"{fb['correct_positions']:^{CORRECT_POS_W}}" +
                PIPE
            )

            print(term.center(term.white + row))
            print(term.olivedrab2 + term.center(border))

    print(term.white + term.bold(f"\nAttempts remaining: {attempts_remaining}"))

def start_game():
    print(term.clear())

    guesses = []
    feedbacks = []

    player_name = input(term.bright_green("Enter your player name: ")).strip().lower()
    if not player_name:
        print(term.firebrick1("Player name cannot be empty. Exiting...."))
        return

    draw_ui(term, 
            guesses,
            feedbacks, 
            attempts_remaining=10, 
            show_instructions=True,
    )

    difficulty_input = ""
    print()
    print(term.bold + term.bright_green("Enter 1 or 2 and press ENTER to begin"))
    
    with term.cbreak():  # read input one key at a time
        while True:
            key = term.inkey()
            if key == " ": # Ignore spacebar completely
                continue
            elif key == "Q":
                print(term.firebrick1("\nYou've ended the game early. Goodbye!"))
                exit()
            elif key.name == "KEY_ENTER":
                if difficulty_input in ("1","2"):
                    break
            else:
                difficulty_input += key
                if difficulty_input not in ("1", "2"):
                    print(term.firebrick1("Invalid input: Please enter 1 for Easy or 2 for Hard"))
                    time.sleep(2)
                    difficulty_input = ""
                    print(term.green("Enter 1 or 2 and press ENTER: "), end="", flush=True)

    difficulty = "easy" if difficulty_input == "1" else "hard"
    
    try:
        response = requests.post(f"{API_URL}/game", json={
            "player_name": player_name, 
            "difficulty": difficulty
        })
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(term.firebrick1(f"Failed to start game: {e}"))
        return
    
    data = response.json()
    game_id = data["game_id"]
    attempts_remaining = data["max_attempts"]
    code_length = data["code_length"]
    welcome_message = data.get("message")
    show_welcome_once = True

    #Clear the instructions, new GAME STARTED screen
    print(term.clear())
    width = term.width
    horizontal_border = "X" * width
    print(term.bright_green + term.bold(horizontal_border))
    print(term.bright_green  + term.bold(term.center("GAME STARTED")))
    print(term.bright_green  + term.bold(horizontal_border))
    print()

    if show_welcome_once and welcome_message:
        print(term.greenyellow(term.center(welcome_message)))
        print()

    print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))

    while attempts_remaining > 0:
        guess_input = input(term.greenyellow(f"Enter your {code_length}-digit guess: "))
        
        if guess_input.strip()== "Q":
            print(term.firebrick1("\nYou've ended the game early. Goodbye!"))
            break

        #Basic validation before sending to backend
        try:
            guess = [int(d) for d in guess_input if d.isdigit()]
            if len(guess) != code_length or any(d < 0 or d > 7 for d in guess):
                raise ValueError
        except ValueError:
            print(term.firebrick1(f"Invalid input: Please enter exactly {code_length} digits between 0 - 7"))
            time.sleep(2)
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            continue

        #Send guess to backend
        res = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
        result = res.json()
        show_welcome_once = False

        if res.status_code != 200:
            print(term.firebrick1(f"Error: {result.get('error', 'Something went wrong.')}"))
            break
        
        #Appending the guess and feedback
        guesses.append(guess)
        feedbacks.append(result["feedback"])
        attempts_remaining = result.get("attempts_remaining", 0)
        
        #Update the progress chart
        draw_ui(term, guesses, feedbacks, attempts_remaining)

        #Display custom feedback from backend
        print(term.aquamarine(result["message"]))

        # Check win/lose condition
        if result.get("message", "").startswith("🥳"):
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            print(term.green(result["message"]))
            break
        elif result.get("message", "").startswith("❌"):
            draw_ui(term, guesses, feedbacks, 0)
            print(term.firebrick1(result["message"]))
            print(term.greenyellow(f"The secret code was: {result['secret_code']}"))
            break

    print(term.aquamarine + term.bold(f"\nThanks for playing, {player_name}!"))
    print()
    input("Press ENTER to exit.")

def main():
    splash_screen()
    start_game()

if __name__ == "__main__":
    
    main()