import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {"sound": True, "car_color": "default", "difficulty": "normal"}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()


def save_settings(s):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(s, f, indent=2)
    except OSError as e:
        print(f"[persistence] Не удалось сохранить настройки: {e}")


def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": score, "distance": int(distance)})
    lb.sort(key=lambda x: x["score"], reverse=True)
    lb = lb[:10]
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(lb, f, indent=2)
    except OSError as e:
        print(f"[persistence] Не удалось сохранить лидерборд: {e}")