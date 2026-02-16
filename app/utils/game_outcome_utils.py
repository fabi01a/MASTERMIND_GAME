def interpret_game_outcome(result: dict) -> str:
    """
    Determines outcome from backend response.
    Returns: "win" | "lose" | "continue"
    """
    message = result.get("message", "")
    if message.startswith("🥳"):
        return "win"
    elif message.startswith("❌"):
        return "lose"
    return "continue"
