import json
import os
from habit import Habit

FILE = "habits.json"


def save_habits(habits):
    """
    Saves all habits to a JSON file.
    """
    with open(FILE, "w") as f:
        json.dump([h.to_dict() for h in habits], f, indent=2)


def load_habits():
    """
    Loads habits from the JSON file.
    Returns an empty list if no file exists or file is empty.
    """
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        content = f.read().strip()
    if not content:
        return []
    return [Habit.from_dict(d) for d in json.loads(content)]
