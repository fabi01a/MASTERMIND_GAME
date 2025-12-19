from blessed import Terminal

term = Terminal()

def flush_input():
    """Drain any pending key presses."""
    while term.inkey(timeout=0):
        pass
