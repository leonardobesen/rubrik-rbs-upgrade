import json

def read_config(CONFIG_PATH: str) -> dict:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config
