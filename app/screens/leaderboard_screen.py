import requests
from blessed import Terminal
from app.utils.ui_helpers import render_screen_title

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
    render_screen_title(term,"🏆 MASTERMIND LEADERBOARD 🏆")
    
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
        print(term.center(term.white + ("-" * len(row))))
        
    input(term.bright_green("Press ENTER to return to the main menu."))

