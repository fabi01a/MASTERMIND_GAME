import requests

API_URL = "http://127.0.0.1:5000"

def create_game(player_name: str, difficulty: str):
    """Starts a new game session."""
    response = requests.post(f"{API_URL}/game", json={
        "player_name": player_name,
        "difficulty": difficulty
    })
    response.raise_for_status()
    return response.json()

def send_guess(game_id: str, guess: list[int]) -> dict:
    """Submits a player's guess to the backend."""
    try:
        response = requests.post(f"{API_URL}/game/{game_id}/guess", json={"guess": guess})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to submit guess: {e}")