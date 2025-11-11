import pytest
from app import create_app
from app.models.player import Player
from app.models.gameSession import GameSession
from app.models.guess import Guess
# from app.routes import games

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client 

def test_create_game(client):
    response = client.post("/game", json={"player_name": "TestPlayer"})
    assert response.status_code == 201
    data = response.get_json()

    assert "game_id" in data
    assert "max_attempts" in data
    assert data["max_attempts"] == 10
    assert "message" in data

# def test_valid_guess(client):
#     create_res = client.post("/game") #First, create a game
#     game_id = create_res.get_json()["game_id"]

#     #Make a valid guess
#     guess_payload = {"guess": [1,2,3,4]}
#     guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)

#     assert guess_res.status_code == 200
#     data = guess_res.get_json()
#     assert "feedback" in data
#     assert "correct_numbers" in data["feedback"]
#     assert "correct_positions" in data["feedback"]


# @pytest.mark.parametrize("bad_guess", [
#     [1, 2, "a", 4],     # string in guess
#     [1, 2, 3],          # too short
#     [1, 2, 3, 4, 5],    # too long
#     "1234",             # string instead of list
#     1234,               # int instead of list
#     ["a", "b", "c", "d"], # all strings
#     [None, 1, 2, 3],    # NoneType in guess
#     [8, 2, 1, 0],       # number out of range (>7)
#     [-1, 2, 3, 4],      # number out of range (<0)
# ])

# def test_invalid_guess_type(client, bad_guess):
#     response = client.post("/game")
#     assert response.status_code == 201
#     game_id = response.get_json()["game_id"]
    
#     #Submit bad guess
#     res = client.post(f"/game/{game_id}/guess", json={"guess": bad_guess})
#     assert res.status_code == 400
    
#     data = res.get_json()
#     assert "error" in data
#     assert (
#         "Invalid guess" in data["error"] 
#         or "Please enter numbers only" in data["error"]
#         or "Please enter four numbers" in data["error"]
#         or "Each number must be between" in data["error"]
#     )

# def test_winning_game(client):
#     res = client.post("/game") #First, start a new game
#     assert res.status_code == 201
#     data = res.get_json()
#     game_id = data["game_id"]

#     #Manually override secret code
#     games[game_id]["secret_code"] = [2,4,0,6]

#     #Submit winning guess
#     guess_payload = {"guess": [2,4,0,6]}
#     guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)
#     assert guess_res.status_code == 200
#     result = guess_res.get_json()

#     #Assert correct win respose
#     assert result["feedback"]["correct_positions"] == 4
#     assert result["message"].startswith("🥳")
#     assert games[game_id]["is_over"] is True
#     assert games[game_id]["win"] is True

# def test_losing_game(client):
#     res = client.post("/game") #First, start a new game
#     assert res.status_code == 201
#     data = res.get_json()
#     game_id = data["game_id"]

#     #Manually override secret code
#     games[game_id]["secret_code"] = [2,4,0,6]

#     #Submit 10 wrong guesses
#     for _ in range(10):
#         guess_payload = {"guess": [1,1,1,1]}
#         guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)
#         assert guess_res.status_code == 200
        
#     #Assert correct loss respose
#     result = guess_res.get_json()
#     assert result["message"].startswith("❌")
#     assert result["secret_code"] == [2,4,0,6]
#     assert games[game_id]["is_over"] is True
#     assert games[game_id]["win"] is False

# def test_guess_after_game_over(client):
#     res = client.post("/game") #First, start a new game
#     assert res.status_code == 201
#     data = res.get_json()
#     game_id = data["game_id"]

#     #Manually end game
#     games[game_id]["is_over"] = True

#     #Try to make a guess after the game is over
#     guess_payload = {"guess": [1,2,3,4]}
#     guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)

#     assert guess_res.status_code == 400
#     data = guess_res.get_json()
#     assert "error" in data
#     assert data["error"] == "Game over. Please start a new game to play again"

# def test_with_invalid_game_id(client):
#     fake_game_id = "nonexistent-game-id-1234"
#     payload = {"guess": [1,1,2,3]}

#     response = client.post(f"/game/{fake_game_id}/guess", json=payload)

#     assert response.status_code == 404
#     data = response.get_json()
#     assert "error" in data
#     assert data["error"] == "Game Not Found"
