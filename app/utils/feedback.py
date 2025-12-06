from app import db

def generate_feedback_message(correct_positions: int, correct_numbers: int, attempts_remaining: int) -> str:
    if correct_positions and correct_numbers:
        return (
            f"You have {correct_positions} number(s) in the correct position(s)"
            f"and {correct_numbers} correct number(s) but in the wrong position(s)"
            f"You have {attempts_remaining} attempts remaining"
        )
    elif correct_positions:
        return (
            f"You have {correct_positions} number(s) in the correct position(s)"
            f"You have {attempts_remaining} attempts remaining"
        )
    elif correct_numbers:
        return (
            f"You have {correct_numbers} correct number(s) but in the wrong position(s)"
            f"You have {attempts_remaining} attempts remaining"
        )
    else:
        return (
            f"No correct numbers this time - Try again! "
            f"You have {attempts_remaining} attempts remaining"
        )
