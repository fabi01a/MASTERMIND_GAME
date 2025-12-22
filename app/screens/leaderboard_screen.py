import requests
from blessed import Terminal

API_URL = "http://127.0.0.1:5000"
term = Terminal()
width = term.width
horizontal_border = "X" * width

def show_leaderboard():
    print(term.clear())

    try:
        response = requests.get(f"{API_URL}/leaderboard") 
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(term.firebrick1(f"Failed to fetch leaderboard: {e}"))
        return

    data = response.json()
    if not data:
        print(term.bold("No leaderboard data yet"))
        return

    horizontal_border = "X" * term.width
    title = "🏆 MASTERMIND LEADERBOARD 🏆"
    
    print(term.bright_green + term.bold(horizontal_border))
    print(term.olivedrab1 + term.bold + term.center(title))
    print(term.bright_green + term.bold(horizontal_border))

    header = "Rank | Player       | Attempts | Difficulty"
    divider = "-----+--------------+----------+-----------"
    print(term.bold + term.center(header))
    print(term.bold + term.center(divider))

    for i, entry in enumerate(data, start=1):
        row = (
            f"{i:>4} | "
            f"{entry['player_name']:<12} | "
            f"{entry['attempts_used']:^8} | "
            f"{entry['difficulty'].capitalize():^10}"
        )
    highlight = (i == 1) #only highlight rank 1
    styled_row = term.gold(row) if highlight else row
    print(term.center(styled_row))
    print(term.center(term.dim + ("-" * len(row))))
    input(term.bold("Press ENTER to return to the main menu."))
