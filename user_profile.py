from datetime import datetime
import json
import os

class UserProfile:
    def __init__(self):
        self.profile_file = "user_profiles.json"
        self.profiles = self._load_profiles()

    def _load_profiles(self):
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_profiles(self):
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, ensure_ascii=False, indent=4)

    def create_profile(self, user_id, name, age, gender, weight, height, language="en"):
        profile = {
            "name": name,
            "age": age,
            "gender": gender,
            "weight": weight,
            "height": height,
            "language": language,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "workout_history": [],
            "emotion_history": [],
            "goals": [],
            "achievements": []
        }
        self.profiles[user_id] = profile
        self._save_profiles()
        return profile

    def get_profile(self, user_id):
        return self.profiles.get(user_id)

    def update_profile(self, user_id, **kwargs):
        if user_id in self.profiles:
            profile = self.profiles[user_id]
            for key, value in kwargs.items():
                if key in profile:
                    profile[key] = value
            profile["last_updated"] = datetime.now().isoformat()
            self._save_profiles()
            return True
        return False

    def add_workout_record(self, user_id, workout_type, duration, intensity, notes=""):
        if user_id in self.profiles:
            record = {
                "date": datetime.now().isoformat(),
                "type": workout_type,
                "duration": duration,
                "intensity": intensity,
                "notes": notes
            }
            self.profiles[user_id]["workout_history"].append(record)
            self._save_profiles()
            return True
        return False

    def add_emotion_record(self, user_id, emotion, intensity, notes=""):
        if user_id in self.profiles:
            record = {
                "date": datetime.now().isoformat(),
                "emotion": emotion,
                "intensity": intensity,
                "notes": notes
            }
            self.profiles[user_id]["emotion_history"].append(record)
            self._save_profiles()
            return True
        return False

    def get_workout_history(self, user_id):
        if user_id in self.profiles:
            return self.profiles[user_id]["workout_history"]
        return []

    def get_emotion_history(self, user_id):
        if user_id in self.profiles:
            return self.profiles[user_id]["emotion_history"]
        return [] 