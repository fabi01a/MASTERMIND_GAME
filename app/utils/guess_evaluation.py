from app.models.gameSession import GameSession


def get_exact_matches(player_guess, secret_code, code_length):
    secret_matched = [False] * code_length
    guess_matched = [False] * code_length
    correct_positions = 0
    for i in range(code_length):
        if player_guess[i] == secret_code[i]:
            correct_positions += 1
            secret_matched[i] = True
            guess_matched[i] = True
    return correct_positions, secret_matched, guess_matched


def get_partial_matches(player_guess, secret_code, secret_matched, guess_matched, code_length):
    correct_numbers = 0
    for i in range(code_length):
        if guess_matched[i]:
            continue
        for j in range(code_length):
            if not secret_matched[j] and player_guess[i] == secret_code[j]:
                correct_numbers += 1
                secret_matched[j] = True
                guess_matched[i] = True
                break
    return correct_numbers


def evaluate_guess(player_guess, secret_code, code_length):
    correct_positions, secret_matched, guess_matched  = get_exact_matches(player_guess, secret_code, code_length)
    correct_numbers = get_partial_matches(
        player_guess, secret_code, secret_matched, guess_matched, code_length
        )

    return {
        "correct_positions": correct_positions,
        "correct_numbers": correct_numbers
    }
