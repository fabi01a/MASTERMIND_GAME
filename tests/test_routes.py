import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client 

def test_create_game(client):
    response = client.post("/game")
    assert response.status_code == 201
    data = response.get_json()

    assert "game_id" in data
    assert "max_attempts" in data
    assert data["max_attempts"] == 10
    assert "message" in data

def test_valid_guess(client):
    create_res = client.post("/game") #First, create a game
    game_id = create_res.get_json()["game_id"]

    #Make a valid guess
    guess_payload = {"guess": [1,2,3,4]}
    guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)

    assert guess_res.status_code == 200
    data = guess_res.get_json()
    assert "feedback" in data
    assert "correct_numbers" in data["feedback"]
    assert "correct_positions" in data["feedback"]

def test_invalid_guess_length(client):
    game_id = client.post("/game").get_json()["game_id"]

    #Bad guess with 3 numbers
    bad_guess = {"guess": [1,2,3]}
    res = client.post(f"/game/{game_id}/guess", json=bad_guess)
    
    assert res.status_code == 400
    assert "error" in res.get_json()

def test_invalid_data_type(client):
    response = client.post("/game")
    assert response.status_code == 201
    game_id = response.get_json()["game_id"]
    
    #Bad guess with a string
    bad_guess = {"guess": ["a", "b", "c", "d"]}
    guess_response = client.post(f"/game/{game_id}/guess", json=bad_guess)

    assert guess_response.status_code == 400
    data = guess_response.get_json()
    assert "error" in data
    assert "Invalid guess" in data["error"] or "Please enter numbers only" in data["error"]
