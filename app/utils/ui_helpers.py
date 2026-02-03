def generate_horizontal_border(term, char: str = "X") -> str:
    return char * term.width

def render_screen_title(term, title: str, border_char: str = "X"):
    horizontal_border = generate_horizontal_border(term, border_char)
    print(term.bright_green + term.bold(horizontal_border))
    print(term.olivedrab1 + term.bold(term.center(title)))
    print(term.bright_green + term.bold(horizontal_border))
