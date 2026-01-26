from app import db
from dataclasses import dataclass
from app.models.gameSession import GameSession
from app.models.guess import Guess
from app.models.player import Player
from app.services.player_service import get_or_create_player
from app.services.game_outcome_service import check_game_outcome
from app.utils.difficulty_config import get_difficulty_settings
from app.utils.exceptions import GameNotFoundError, GameOverError
from app.utils.secret_code_generation import generate_secret_code
from app.utils.normalization import normalize_name
from app.utils.validation import validate_guess_input, InvalidGuessError
from app.utils.feedback import generate_feedback_message
from app.utils.guess_evaluation import evaluate_guess

@dataclass
class GameInitResult:
    game: GameSession
    player: Player
    message: str

def initialize_new_game(raw_name: str, difficulty: str) -> GameInitResult:

    normalized_name = normalize_name(raw_name)
    player, is_returning = get_or_create_player(normalized_name)

    settings = get_difficulty_settings(difficulty)
    code_length = settings["code_length"]
    max_attempts = settings["max_attempts"]

    secret_code = generate_secret_code(code_length)
    game_sesh = create_game_session(
        player_id=player.player_id, 
        secret_code=secret_code, 
        code_length=code_length,
        max_attempts=max_attempts,
        difficulty=difficulty
    )

    message = (
        f"Welcome back, {raw_name}! New game created - Good Luck!"
        if is_returning else
        f"New game created - Good Luck {raw_name}!"
    )

    return GameInitResult(game=game_sesh, player=player, message=message)


def create_game_session(player_id: int, secret_code: list[int], code_length: int, max_attempts: int, difficulty: str):
    new_game = GameSession(
        player_id=player_id,
        secret_code=secret_code,
        attempts_remaining=max_attempts,
        code_length=code_length,
        max_attempts=max_attempts,
        difficulty=difficulty
    )
    db.session.add(new_game)
    db.session.commit()
    return new_game


def process_guess(game_id: int, guess: list[int]) -> dict:
    game = db.session.get(GameSession, game_id)

    if not game:
        raise GameNotFoundError()
    
    if game.is_over:
        raise GameOverError()
    
    validate_guess_input(guess, game.code_length)

    result = evaluate_guess(guess, game.secret_code, game.code_length)
    correct_positions = result["correct_positions"]
    correct_numbers = result["correct_numbers"]

    new_guess = Guess(
        game_session_id=game.game_session_id,
        guess_value=guess,
        correct_positions=correct_positions,
        correct_numbers=correct_numbers
    )

    db.session.add(new_guess)
    game.attempts_remaining -= 1

    feedback_message = generate_feedback_message(
        correct_positions=correct_positions,
        correct_numbers=correct_numbers,
        attempts_remaining=game.attempts_remaining,
        player_name=game.player.player_name
    )

    feedback = {
        "user_guess": guess,
        "correct_positions": correct_positions,
        "correct_numbers": correct_numbers
    }

    outcome_response = check_game_outcome(game, correct_positions, feedback)
    if outcome_response:
        return outcome_response

    db.session.commit()

    return {
        "message": feedback_message,
        "feedback": feedback,
        "attempts_remaining": game.attempts_remaining
    }

