import json
from pathlib import Path

#Keeping the progress.json in the project
SAVE_FILE = Path(__file__).resolve().parent.parent / "progress.json"

def load_progress(app):
    if SAVE_FILE.exists():
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            app.exp = data.get("exp", 0)
            app.level = data.get("level", 1)
            app.mission_index = data.get("mission_index", 0)

        except (json.JSONDecodeError, TypeError, ValueError, OSError):
            print("Save file is invalid. Starting fresh.")

def save_progress(app):
    data = {
        "exp": app.exp,
        "level": app.level,
        "mission_index": app.mission_index
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)