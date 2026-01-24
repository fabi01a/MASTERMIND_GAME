#removes whitespace and converts name to lowercase
def normalize_name(name: str) -> str:
    return name.strip().lower()
