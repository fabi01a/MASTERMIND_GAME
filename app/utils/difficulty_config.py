# utility/difficulty_config.py


class InvalidDifficultyError(ValueError):
    """Raised when an invalid difficulty level is provided"""

    pass


DIFFICULTY_SETTINGS = {
    "easy": {"code_length": 4, "max_attempts": 10},
    "hard": {"code_length": 6, "max_attempts": 10},
}


def get_difficulty_settings(difficulty):
    """
    Returns the settings for a given difficulty level.

    Args:
        difficulty (str): Difficulty level like "easy" or "hard".

    Returns:
        dict: Dictionary with code_length and max_attempts.

    Raises:
        InvalidDifficultyError: If the difficulty is not supported.
    """
    normalized = difficulty.lower()
    if normalized not in DIFFICULTY_SETTINGS:
        raise InvalidDifficultyError(
            f"Unsupported difficulty: '{difficulty}'. Valid options are: {', '.join(DIFFICULTY_SETTINGS)}"
        )
    return DIFFICULTY_SETTINGS[normalized]
