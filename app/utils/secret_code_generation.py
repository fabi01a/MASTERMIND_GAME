# review
import requests
import random


def generate_secret_code(code_length):
    url = "https://www.random.org/integers/"
    params = {
        "num": code_length,
        "min": 0,
        "max": 7,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return [int(line) for line in response.text.strip().splitlines()]
    except requests.RequestException:
        return [random.randint(0, 7) for _ in range(code_length)]
