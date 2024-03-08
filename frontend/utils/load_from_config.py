import json
def load_config():
    try:
        with open("data/config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty config if no file exists