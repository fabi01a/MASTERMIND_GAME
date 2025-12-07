import requests
from blessed import Terminal
import time

term = Terminal()

API_URL = "http://127.0.0.1:5000"

def draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=False):
    print(term.clear()) #Calls the function
    width = term.width
    horizontal_border = "X" * width

    #Title / Box Design
    print(term.orange + term.bold(horizontal_border))
    print(term.orange + term.bold(term.center("MASTERMIND - THE GAME")))
    print(term.orange + term.bold(horizontal_border))

    #Display the instructions
    if show_instructions:
        print(term.bold + term.center("Game Rules:")) 
        print(term.center("- Guess the right four-number combination between 0 - 7"))
        print(term.center("- After each guess, you'll see feeback:"))
        print(term.center("     * Correct number(s) in the correct place"))
        print(term.center("     * Correct number(s) but in the wrong place"))
        print(term.center("- You have 10 attempts to crack the code"))
        print(term.orange + term.bold(horizontal_border))
        print()
        # print(term.pink("\nWant to play with six numbers? Click here!"))
        # print()
        print(term.green("\nHit ENTER to play"))
        print(term.red("\nType Q to end the game early"))
        return

    #If guesses exist, show the table
    if guesses: 
        print(term.center("+-----------+--------------+-------------------+------------------------------+"))
        print(term.center("|  Attempt  |  Your Guess  |  Matching Digits  |  Matching Digits & Position  |"))
        print(term.center("+-----------+--------------+-------------------+------------------------------+"))
        for i, (guess, fb) in enumerate(zip(guesses, feedbacks), start=1):
            print(term.center(f"|   {i:<7} | {str(guess):<11} | {fb['correct_numbers']:^16} | {fb['correct_positions']:^29} |"))
        print(term.center("+-----------+--------------+-------------------+------------------------------+"))


def start_game():
    print(term.clear())
    player_name = input(term.cyan("Enter your player name: ")).strip()

    if not player_name:
        print(term.red("Player name cannot be empty. Exiting...."))
        return
    try:
        response = requests.post(f"{API_URL}/game", json={"player_name": player_name})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(term.red(f"Failed to start game: {e}"))
        return

    data = response.json()
    game_id = data["game_id"]
    attempts_remaining = data["max_attempts"]
    print(response.status_code)
    print(response.text)

    guesses = []
    feedbacks = []
    attempts_remaining = 10

    show_instructions = False

    #Show instructions ONCE before starting the game loop
    draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=True)

    #Capture user decision BEFORE entering game loop
    while True:
        with term.cbreak():  # read input one key at a time
            key = term.inkey()
            
            if key.name == "KEY_ENTER":
                break
            elif key == "Q":
                print(term.red("\nYou've ended the game early. Goodbye!"))
                exit()
            elif key == " ":
                # Ignore spacebar completely
                continue
            else:
                print(term.red("Invalid input: Please hit ENTER to begin the game"))
                time.sleep(2)
                
    #Clear the instructions, new GAME STARTED screen
    print(term.clear())
    width = term.width
    horizontal_border = "X" * width
    print(term.orange + term.bold(horizontal_border))
    print(term.orange + term.bold(term.center("GAME STARTED")))
    print(term.orange + term.bold(horizontal_border))
    print()
    print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))

    while attempts_remaining > 0:
        guess_input = input(term.yellow("Enter your four-digit guess: "))
        
        if guess_input.strip()== "Q":
            print(term.red("\nYou've ended the game early. Goodbye!"))
            break

        #Basic validation before sending to backend
        try:
            guess = [int(d) for d in guess_input if d.isdigit()]
            if len(guess) != 4:
                raise ValueError
        except ValueError:
            print(term.red("Invalid input: Please enter exactly four digits between 0 - 7"))
            time.sleep(2)
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            continue

        #Send guess to backend
        res = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
        result = res.json()

        if res.status_code != 200:
            print(term.red(f"Error: {result.get('error', 'Something went wrong.')}"))
            break
        
        #Appending the guess and feedback
        guesses.append(guess)
        feedbacks.append(result["feedback"])
        attempts_remaining = result.get("attempts_remaining", 0)
        
        #Update the progress chart
        draw_ui(term, guesses, feedbacks, attempts_remaining)

        #Display custom feedback from backend
        print(term.cyan(result["message"]))

        # Check win/lose condition
        if result.get("message", "").startswith("🥳"):
            draw_ui(term, guesses, feedbacks, attempts_remaining)
            print(term.green(result["message"]))
            break
        elif result.get("message", "").startswith(" ❌"):
            draw_ui(term, guesses, feedbacks, 0)
            print(term.red(result["message"]))
            print(term.red(f"The secret code was: {result['secret_code']}"))
            break

    print(term.bold("\nGame Over. Thanks for playing!"))
    input("Press ENTER to exit.")


if __name__ == "__main__":
    start_game()