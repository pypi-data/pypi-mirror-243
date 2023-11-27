from os.path import expanduser
from tomlkit import parse


DEFAULT_CONFIG_FILE = expanduser("~/.chomp/config")


def get_nutritional_targets():
    try:
        with open(DEFAULT_CONFIG_FILE, "r") as f:
            data = parse(f.read())
        return data.get("nutritional_goals", None)
    except FileNotFoundError:
        return None
