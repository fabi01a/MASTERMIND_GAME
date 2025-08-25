import requests
from blessed import Terminal
import time

term = Terminal()

API_URL = "http://127.0.0.1:5000"

def draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=False): #UI rendering functions
    print(term.clear()) #calls the function
    print(term.bold_underline(term.center("MASTERMIND - THE GAME")))
    print()

    #Display the instructions
    if show_instructions:
        print(term.bold("Game Rules:")) 
        print("- Guess the right four-number combination between 0 - 7")
        print("- After each guess, you'll see feeback:")
        print("     * Correct number(s) in the correct place")
        print("     * Correct number(s) but in the wrong place")
        print("- You have 10 attempts to crack the code")
        print()
        # print(term.orange("\nWant to play with six numbers? Click here!"))
        print(term.green("\nHit ENTER to play"))
        term.inkey()
    
        print(term.clear)
        print(term.bold_underline(term.center("GAME STARTED")))
        print()

        #Display attempts
        print(term.bold(f"You have {attempts_remaining} attempts remaining\n"))

    #if guesses exist, show the table
    if guesses: 
        print("+-----------+--------------+-------------------+------------------------------+")
        print("|  Attempt  |  Your Guess  |  Matching Digits  |  Matching Digits & Position  |")
        print("+-----------+--------------+-------------------+------------------------------+")
        for i, (guess, fb) in enumerate(zip(guesses, feedbacks), start=1):
            print(f"|   {i:<7} | {str(guess):<11} | {fb['correct_numbers']:^16} | {fb['correct_positions']:^29} |")
        print("+-----------+--------------+-------------------+------------------------------+")

def start_game():
    # Start new game
    response = requests.post(f"{API_URL}/game")
    data = response.json()
    game_id = data["game_id"]

    guesses = []
    feedbacks = []
    attempts_remaining = 10

    show_instructions = True

    #show instructions ONCE before starting the game loop
    draw_ui(term, guesses, feedbacks, attempts_remaining, show_instructions=show_instructions)

    while attempts_remaining > 0:
        guess_input = input(term.yellow("Enter your four-digit guess: "))

        # Basic validation before sending to backend
        try:
            guess = [int(d) for d in guess_input if d.isdigit()]
            if len(guess) != 4:
                raise ValueError
        except ValueError:
            print(term.red("Invalid input: Please enter exactly four digits between 0 - 7"))
            time.sleep(1)
            continue

        # Send guess to backend
        res = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
        result = res.json()

        if res.status_code != 200:
            print(term.red(f"Error: {result.get('error', 'Something went wrong.')}"))
            break
        
        #appending the guess and feedback
        guesses.append(guess)
        feedbacks.append(result["feedback"])
        attempts_remaining = result.get("attempts_remaining", 0)

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