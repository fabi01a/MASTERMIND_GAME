def format_table_row(columns: list[str], widths: list[int], sep: str = " | ") -> str:
    """
    Formats a row of text aligned to the given column widths.
    """
    padded = [col.ljust(w) for col, w in zip(columns, widths)]
    return sep.join(padded)


def format_divider(widths: list[int], sep: str = "-+-") -> str:
    return sep.join(["-" * w for w in widths])
