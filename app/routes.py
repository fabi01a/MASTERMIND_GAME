from flask import Blueprint, request, jsonify
from app.services.game_service import (
    initialize_new_game,
    process_guess,
)
from app.services.leaderboard_service import get_top_leaderboard
from app.utils.difficulty_config import InvalidDifficultyError
from app.utils.exceptions import GameNotFoundError, GameOverError, InvalidGuessError

routes = Blueprint("routes", __name__)


@routes.route("/leaderboard", methods=["GET"])
def leaderboard():
    results = get_top_leaderboard()
    leaderboard_data = [
        {
            "player_name": row.player_name,
            "attempts_used": row.attempts_used,
            "difficulty": row.difficulty,
        }
        for row in results
    ]
    return jsonify(leaderboard_data)


@routes.route("/game", methods=["POST"])
def create_game():
    request_body = request.get_json()
    raw_name = request_body["player_name"].strip()
    difficulty = request_body.get("difficulty", "easy").lower()

    try:
        result = initialize_new_game(raw_name, difficulty)
    except InvalidDifficultyError as e:
        return jsonify({"error": str(e)}), 400

    return (
        jsonify(
            {
                "game_id": result.game.game_session_id,
                "max_attempts": result.game.attempts_remaining,
                "number_range": [0, 7],
                "code_length": result.game.code_length,
                "difficulty": difficulty,
                "message": result.message,
            }
        ),
        201,
    )


@routes.route("/game/<game_id>/guess", methods=["POST"])
def player_guess(game_id):
    data = request.get_json()
    guess_input = data.get("guess")

    try:
        result = process_guess(game_id=int(game_id), guess=guess_input)
    except InvalidGuessError as e:
        return jsonify({"error": e.message}), 400
    except GameNotFoundError:
        return jsonify({"error": "Game Not Found"}), 404
    except GameOverError:
        return jsonify({"error": "Game Over - Please start a new game"}), 400
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    return jsonify(result), 200
