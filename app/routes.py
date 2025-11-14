from app.game_settings import MIN_VALUE, MAX_VALUE, CODE_LENGTH
from app.models.player import Player
from app.models.gameSession import GameSession
from app.models.guess import Guess
from app.services.player_service import get_or_create_player
from app.services.game_service import create_game_session
from app.utils.validation import validate_guess_input, InvalidGuessError
from app import db
from flask import Blueprint, request, jsonify
from app.random_api import generate_secret_code
import uuid

routes = Blueprint('routes', __name__)

@routes.route("/game", methods = ["POST"])
def create_game():
    request_body = request.get_json()
    player_name = request_body["player_name"]
    
    #initialize core game components
    player = get_or_create_player(player_name)
    secret_code = generate_secret_code()
    game_sesh = create_game_session(player.player_id, secret_code)

    return jsonify({
        "game_id": game_sesh.game_session_id,
        "max_attempts": game_sesh.attempts_remaining,
        "number_range": [0,7],
        "message": "New game created. Good Luck!"
    }), 201

@routes.route("/game/<game_id>/guess", methods = ["POST"])
def player_guess(game_id):
    game = db.session.get(GameSession, game_id)
    if not game:
        return jsonify({"error": "Game Not Found"}), 404
    if game.is_over:
        return jsonify({"error": "Game over. Please start a new game to play again"}), 400
    
    guess = request.get_json() #extracts the json body from incoming POST request and stores in guess
    player_guess = guess.get("guess")

    try:
        validate_guess_input(player_guess)
    except InvalidGuessError as e:
        return jsonify({"error": e.message}), 400
            
    #Comparison
    def compare_guess_to_secret(player_guess, secret):
        secret = game.secret_code
        correct_positions = 0
        correct_numbers = 0

        #Temp lists to track matched indexes
        secret_used = [False] * CODE_LENGTH
        guess_used = [False] * CODE_LENGTH
            
        #First pass: Exact matches
        for index, value in enumerate(player_guess):
            if value == secret[index]:
                correct_positions += 1
                secret_used[index] = True
                guess_used[index] = True

        #Second pass: Partial matches        
        for index, value in enumerate(player_guess):
            if guess_used[index]:
                continue #already counted (as a bool) in exact match check, so lets skip it

            for j, secret_val in enumerate(secret): #if not, lets look for a partial match
                if not secret_used[j] and value == secret_val:
                    correct_numbers += 1
                    secret_used[j] = True
                    break #stop checking omce guess checked 
        
        #Save Guess to DB
        new_guess = Guess(
            game_session_id=game.game_session_id,
            guess_value=player_guess,
            correct_positions=correct_positions,
            correct_numbers=correct_numbers
        )
        db.session.add(new_guess)

        #updating game state
        game.attempts_remaining -= 1

        feedback = {
            "user_guess":player_guess,
            "correct_positions": new_guess.correct_positions,
            "correct_numbers": new_guess.correct_numbers
        }
        print("Correct positions:", correct_positions)
        print("Winning guess detected? ", correct_positions == CODE_LENGTH)


        # End conditions
        if correct_positions == CODE_LENGTH:
            game.is_over = True
            game.win = True
            db.session.commit()
            return jsonify({
                "message": "🥳 Congrats! You cracked the secret code!!! 🥳",
                "feedback": feedback
                }), 200

        elif game.attempts_remaining <= 0:
            game.is_over = True
            game.win = False
            db.session.commit()
            return jsonify({
                "message": "❌ Game Over - No more attempts left ❌",
                "secret_code": game.secret_code,
                "feedback": feedback
                }), 200
        
        # #Constructing feedback for ongoing game
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

        #Return compare_guess_to_secret(player_guess, game["secret_code"])
        return jsonify({
            "message": result_message,
            "feedback": feedback,
            "attempts_remaining": game.attempts_remaining
        }), 200
    
    return compare_guess_to_secret(player_guess, game.secret_code)
