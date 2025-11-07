from app.models.player import Player
from app.models.gameSession import GameSession
from app.models.guess import Guess
from app import db
from flask import Blueprint, request, jsonify
from app.random_api import generate_secret_code
import uuid

routes = Blueprint('routes', __name__)

# games = {} #stores active games
MIN_VALUE = 0
MAX_VALUE = 7
CODE_LENGTH = 4


#Start a new game
@routes.route("/game", methods = ["POST"])
def create_game():
    request_body = request.get_json()
    player_name = request_body["player_name"]
    
    player = Player.query.filter_by(player_name=player_name).first()
    if not player:
        player = Player(player_name=player_name)
        db.session.add(player)
        db.session.commit()
    
    secret_code = generate_secret_code()

    game_sesh = GameSession(
        player_id = player.player_id,
        secret_code = secret_code
    )
    db.session.add(game_sesh)
    db.session.commit ()

    return jsonify({
        "game_id": game_sesh.game_session_id,
        "max_attempts": game_sesh.attempts_remaining,
        "number_range": [0,7],
        "message": "New game created. Good Luck!"
    }), 201


@routes.route("/game/<game_id>/guess", methods = ["POST"])
def player_guess(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game Not Found"}), 404

    if game["is_over"]:
        return jsonify({"error": "Game over. Please start a new game to play again"}), 400
    
    guess = request.get_json() #extracts the json body from incoming POST request and stores in guess
    player_guess = guess.get("guess")

    #Validation***
    def validate_guess_input(player_guess):
        if not isinstance(player_guess, list) or len(player_guess) != CODE_LENGTH:
            return jsonify({"error": "Please enter four numbers"}), 400
        for num in player_guess:
            if not isinstance(num, int):
                return jsonify({"error": "Invalid guess - Please enter numbers only"}), 400
            if not (MIN_VALUE <= num <= MAX_VALUE):
                return jsonify({"error": "Invalid guess - Each number must be between 0 - 7"}), 400

    #Calling validation function
    validate_response = validate_guess_input(player_guess)
    if validate_response:
        return validate_response
            
    #Comparison
    def compare_guess_to_secret(player_guess, secret):
        secret = game["secret_code"]
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
    
        #Feedback
        feedback = {
            "user_guess": player_guess,
            "correct_positions": correct_positions,
            "correct_numbers": correct_numbers
        }
        
        # game["guesses"].append(feedback)
        # game["attempts_remaining"] -= 1

        #End conditions
        # if correct_positions == CODE_LENGTH:
            # game["is_over"] = True
            # game["win"] = True
            # return jsonify({
            #     "message": "🥳 Congrats! You cracked the secret code!!! 🥳",
            #     "feedback": feedback
            #     }), 200

        # elif game["attempts_remaining"] <= 0:
        #     game["is_over"] = True
        #     game["win"] = False
        #     return jsonify({
        #         "message": "❌ Game Over - No more attempts left ❌",
        #         "secret_code": game["secret_code"],
        #         "feedback": feedback
        #         }), 200
        
        #Constructing feedback for ongoing game
        if correct_positions and correct_numbers:
            result_message = (
                f"You have {correct_positions} number(s) in the correct position(s)"
                f"and {correct_numbers} correct number(s) but in the wrong position(s)"
                f"You have {game['attempts_remaining']} attempts remaining"
            )
        elif correct_positions:
            result_message = (
                f"You have {correct_positions} number(s) in the correct position(s). "
                f"You have {game['attempts_remaining']} attempts remaining"
            )
        elif correct_numbers:
            result_message = (
                f"You have {correct_numbers} correct number(s) but in the wrong position(s). "
                f"You have {game['attempts_remaining']} attempts remaining"
            )
        else:
            result_message = (
                f"No correct numbers this time. Try again! "
                f"You have {game['attempts_remaining']} attempts remaining"
            )

        #R eturn compare_guess_to_secret(player_guess, game["secret_code"])
        return jsonify({
            "message": result_message,
            "feedback": feedback,
            "attempts_remaining": game["attempts_remaining"]
        }), 200
    
    return compare_guess_to_secret(player_guess, game["secret_code"])
