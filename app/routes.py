from app import db
from app.game_settings import MIN_VALUE, MAX_VALUE
from app.models.gameSession import GameSession
from app.models.guess import Guess
from app.models.player import Player
from app.random_api import generate_secret_code
from app.services.game_service import create_game_session
from app.services.player_service import get_or_create_player
from app.utils.guess_evaluation import get_exact_matches, get_partial_matches, evaluate_guess
from app.utils.validation import validate_guess_input, InvalidGuessError
from flask import Blueprint, request, jsonify
import uuid

routes = Blueprint('routes', __name__)

@routes.route("/game", methods = ["POST"])
def create_game():
    request_body = request.get_json()
    player_name = request_body["player_name"]
    code_length = request_body.get("code_length", 4)

    #initialize core game components
    player = get_or_create_player(player_name)
    secret_code = generate_secret_code(code_length)
    game_sesh = create_game_session(player.player_id, secret_code, code_length)

    return jsonify({
        "game_id": game_sesh.game_session_id,
        "max_attempts": game_sesh.attempts_remaining,
        "number_range": [0,7],
        "code_length": game_sesh.code_length,
        "message": f"New game created. Good Luck {player_name}!"
    }), 201


@routes.route("/game/<game_id>/guess", methods = ["POST"])
def player_guess(game_id):
    game = db.session.get(GameSession, game_id)
    if not game:
        return jsonify({"error": "Game Not Found"}), 404
    if game.is_over:
        return jsonify({"error": "Game over. Please start a new game to play again"}), 400
    
    data = request.get_json() 
    player_guess = data.get("guess")
    code_length = game.code_length

    try:
        validate_guess_input(player_guess, game.code_length)
    except InvalidGuessError as e:
        return jsonify({"error": e.message}), 400

    result = evaluate_guess(player_guess, game.secret_code, code_length)
    correct_positions = result["correct_positions"]
    correct_numbers = result["correct_numbers"]

    new_guess = Guess(
        game_session_id=game.game_session_id,
        guess_value=player_guess,
        correct_positions=correct_positions,
        correct_numbers=correct_numbers
    )
    db.session.add(new_guess)

    game.attempts_remaining -= 1

    feedback = {
        "user_guess": player_guess,
        "correct_positions": new_guess.correct_positions,
        "correct_numbers": new_guess.correct_numbers
    }

    if correct_positions == game.code_length:
        game.is_over = True
        game.win = True
        db.session.commit()
        return jsonify({
            "message": "🥳 Congrats! You cracked the secret code!!! 🥳",
            "feedback": feedback
        }), 200

    if game.attempts_remaining <= 0:
        game.is_over = True
        game.win = False
        db.session.commit()
        return jsonify({
            "message": "❌ Game Over - No more attempts left ❌",
            "secret_code": game.secret_code,
            "feedback": feedback
        }), 200
    
    db.session.commit()

    if correct_positions and correct_numbers:
        result_message = (
            f"You have {correct_positions} number(s) in the correct position(s)"
            f"and {correct_numbers} correct number(s) but in the wrong position(s)"
            f"You have {game.attempts_remaining} attempts remaining"
        )
    elif correct_positions:
        result_message = (
            f"You have {correct_positions} number(s) in the correct position(s). "
            f"You have {game.attempts_remaining} attempts remaining"
        )
    elif correct_numbers:
        result_message = (
            f"You have {correct_numbers} correct number(s) but in the wrong position(s). "
            f"You have {game.attempts_remaining} attempts remaining"
        )
    else:
        result_message = (
            f"No correct numbers this time. Try again! "
            f"You have {game.attempts_remaining} attempts remaining"
        )

    return jsonify({
        "message": result_message,
        "feedback": feedback,
        "attempts_remaining": game.attempts_remaining
    }), 200

