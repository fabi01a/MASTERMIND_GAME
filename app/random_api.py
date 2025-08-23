import requests

def generate_secret_code():
    url = "https://www.random.org/integers/"
    params = {
        "num": 4,
        "min": 0,
        "max": 7,
        "col": 1,
        "base": 10,
        "format": "plain", 
        "rnd": "new"
    }

    response = requests.get(url, params=params) #sends the get request to the api
    response.raise_for_status()
    return [int(line) for line in response.text.strip().splitlines()]