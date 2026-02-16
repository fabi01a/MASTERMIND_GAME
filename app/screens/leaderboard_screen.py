import requests
from blessed import Terminal
from app.utils.ui_helpers import render_screen_title
from app.api.api_client import send_guess
from app.utils.table_formatter import format_table_row, format_divider

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

    render_screen_title(term, "🏆 MASTERMIND LEADERBOARD 🏆")

    headers = ["Rank", "Player", "Attempts", "Difficulty"]
    col_widths = [6, 14, 10, 12]
    print(term.bold + term.center(format_table_row(headers, col_widths)))
    print(term.bold + term.center(format_divider(col_widths)))

    for i, entry in enumerate(data, start=1):
        row = format_table_row(
            [
                str(i),
                entry["player_name"],
                str(entry["attempts_used"]),
                entry["difficulty"].capitalize(),
            ],
            col_widths,
        )

        highlight = i == 1  # only highlight rank 1
        styled_row = term.gold(row) if highlight else row
        print(term.center(styled_row))

    input(term.bright_green("Press ENTER to return to the main menu."))
