from flask import Blueprint, request, jsonify
from app import db
from app.models.gameSession import GameSession
from app.models.guess import Guess
from app.random_api import generate_secret_code
from app.services.game_outcome_service import check_game_outcome
from app.services.game_service import create_game_session
from app.services.player_service import get_or_create_player
from app.utils.feedback import generate_feedback_message
from app.utils.guess_evaluation import evaluate_guess
from app.utils.validation import validate_guess_input, InvalidGuessError


routes = Blueprint('routes', __name__)

@routes.route("/game", methods = ["POST"])
def create_game():
    request_body = request.get_json()
    raw_name = request_body["player_name"].strip()
    code_length = request_body.get("code_length", 4)

    #initialize core game components
    player, is_returning = get_or_create_player(raw_name)
    if is_returning:
        message = f"Welcome back, {raw_name}! New game created - Good Luck!"
    else:
        message = f"New game created - Good Luck {raw_name}!"

    secret_code = generate_secret_code(code_length)
    game_sesh = create_game_session(player.player_id, secret_code, code_length)

    return jsonify({
        "game_id": game_sesh.game_session_id,
        "max_attempts": game_sesh.attempts_remaining,
        "number_range": [0,7],
        "code_length": game_sesh.code_length,
        "message": message
    }), 201


@routes.route("/game/<game_id>/guess", methods = ["POST"])
def player_guess(game_id):
    game = db.session.get(GameSession, game_id)
    player = game.player
    
    if not game:
        return jsonify({"error": "Game Not Found"}), 404
    if game.is_over:
        return jsonify({"error": "Game over - Please start a new game to play again"}), 400
    
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

    feedback_message = generate_feedback_message(
        correct_positions=correct_positions,
        correct_numbers=correct_numbers,
        attempts_remaining=game.attempts_remaining,
        player_name=player.player_name
    )

    feedback = {
        "user_guess": player_guess,
        "correct_positions": correct_positions,
        "correct_numbers": correct_numbers
    }

    outcome_response = check_game_outcome(game, correct_positions, feedback)
    if outcome_response:
        return jsonify(outcome_response), 200

    return jsonify({
        "message": feedback_message,
        "feedback": feedback,
        "attempts_remaining": game.attempts_remaining
    }), 200

