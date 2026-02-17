from app import db
import pytest
from app import create_app
from app.models.game_session import GameSession


TEST_PLAYER_NAME = "TestPlayer"


@pytest.fixture
def client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()

        with app.test_client() as client:
            yield client

        db.drop_all()


def create_test_game(client, player_name=TEST_PLAYER_NAME):
    res = client.post("/game", json={"player_name": TEST_PLAYER_NAME})
    assert res.status_code == 201
    return res.get_json()["game_id"]


def test_create_game(client):
    response = client.post("/game", json={"player_name": TEST_PLAYER_NAME})
    data = response.get_json()

    assert response.status_code == 201
    assert "game_id" in data
    assert "max_attempts" in data
    assert data["max_attempts"] == 10
    assert "message" in data


def test_valid_guess(client):
    game_id = create_test_game(client)

    guess_payload = {"guess": [1, 2, 3, 4]}
    valid_guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)

    assert valid_guess_res.status_code == 200
    data = valid_guess_res.get_json()
    assert "feedback" in data
    assert "correct_numbers" in data["feedback"]
    assert "correct_positions" in data["feedback"]


@pytest.mark.parametrize(
    "bad_guess",
    [
        [1, 2, "a", 4],  # string in guess
        [1, 2, 3],  # too short
        [1, 2, 3, 4, 5],  # too long
        "1234",  # string instead of list
        1234,  # int instead of list
        ["a", "b", "c", "d"],  # all strings
        [None, 1, 2, 3],  # NoneType in guess
        [8, 2, 1, 0],  # number out of range (>7)
        [-1, 2, 3, 4],  # number out of range (<0)
    ],
)
def test_invalid_guess_type(client, bad_guess):
    game_id = create_test_game(client)

    bad_guess_res = client.post(f"/game/{game_id}/guess", json={"guess": bad_guess})
    assert bad_guess_res.status_code == 400

    data = bad_guess_res.get_json()
    assert "error" in data
    assert (
        "Invalid guess" in data["error"]
        or "Please enter numbers only" in data["error"]
        or "Please enter four numbers" in data["error"]
        or "Each number must be between" in data["error"]
    )


def test_winning_game(client):
    game_id = create_test_game(client)

    game = db.session.get(GameSession, game_id)
    game.secret_code = [2, 4, 0, 6]
    db.session.commit()

    guess_payload = {"guess": [2, 4, 0, 6]}
    winning_guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)
    assert winning_guess_res.status_code == 200
    result = winning_guess_res.get_json()

    assert result["feedback"]["correct_positions"] == 4
    assert result["message"].startswith("🥳")

    # Refresh game from DB to check win state
    updated_game = db.session.get(GameSession, game_id)
    assert updated_game.is_over is True
    assert updated_game.win is True


def test_losing_game(client):
    game_id = create_test_game(client)

    from app.models.game_session import GameSession
    from app import db

    game = db.session.get(GameSession, game_id)
    game.secret_code = [2, 4, 0, 6]
    db.session.commit()

    # Submit 10 wrong guesses
    for _ in range(10):
        guess_payload = {"guess": [1, 1, 1, 1]}
        guess_res = client.post(f"/game/{game_id}/guess", json=guess_payload)
        assert guess_res.status_code == 200

    result = guess_res.get_json()
    assert result["message"].startswith("❌")
    assert result["secret_code"] == [2, 4, 0, 6]

    updated_game = db.session.get(GameSession, game_id)
    assert updated_game.is_over is True
    assert updated_game.win is False


def test_guess_after_game_over(client):
    game_id = create_test_game(client)

    from app.models.game_session import GameSession
    from app import db

    game = db.session.get(GameSession, game_id)
    game.is_over = True
    db.session.commit()

    # Try to make a guess after the game is over
    guess_payload = {"guess": [1, 2, 3, 4]}
    guess_after_res = client.post(f"/game/{game_id}/guess", json=guess_payload)
    assert guess_after_res.status_code == 400
    data = guess_after_res.get_json()

    assert "error" in data
    assert "Game Over" in data["error"]


def test_with_invalid_game_id(client):
    fake_game_id = "nonexistent-game-id-1234"
    payload = {"guess": [1, 1, 2, 3]}

    response = client.post(f"/game/{fake_game_id}/guess", json=payload)

    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Game Not Found"
