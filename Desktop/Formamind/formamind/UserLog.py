import json
from datetime import datetime

class UserLog:
    def __init__(self, filename="user_log.json"):
        self.filename = filename

    def log_interaction(self, language, goal, feeling, suggestion, confirmed):
        log_entry = {
            "timestamp":
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "languagae": language,
            "goal": goal,
            "feeling": feeling,
            "suggestion": suggestion,
            "confirmed": confirmed
        }
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(log_entry)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)