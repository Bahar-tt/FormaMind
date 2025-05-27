from datetime import datetime
import json
import os

class RewardSystem:
    def __init__(self):
        self.rewards_file = "rewards.json"
        self.rewards = self._load_rewards()
        self.achievements = {
            "workout_streak": {
                "name": "Workout Warrior",
                "description": "Complete workouts for 7 consecutive days",
                "points": 100
            },
            "emotion_tracking": {
                "name": "Emotion Explorer",
                "description": "Track your emotions for 5 consecutive days",
                "points": 50
            },
            "goal_achieved": {
                "name": "Goal Getter",
                "description": "Achieve a set goal",
                "points": 200
            },
            "perfect_week": {
                "name": "Perfect Week",
                "description": "Complete all planned activities for a week",
                "points": 300
            }
        }

    def _load_rewards(self):
        if os.path.exists(self.rewards_file):
            with open(self.rewards_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_rewards(self):
        with open(self.rewards_file, 'w', encoding='utf-8') as f:
            json.dump(self.rewards, f, ensure_ascii=False, indent=4)

    def initialize_user(self, user_id):
        if user_id not in self.rewards:
            self.rewards[user_id] = {
                "points": 0,
                "level": 1,
                "achievements": [],
                "streaks": {
                    "workout": 0,
                    "emotion": 0
                },
                "last_activity": None
            }
            self._save_rewards()

    def add_points(self, user_id, points):
        if user_id in self.rewards:
            self.rewards[user_id]["points"] += points
            self._check_level_up(user_id)
            self._save_rewards()
            return True
        return False

    def _check_level_up(self, user_id):
        points = self.rewards[user_id]["points"]
        current_level = self.rewards[user_id]["level"]
        new_level = (points // 1000) + 1
        if new_level > current_level:
            self.rewards[user_id]["level"] = new_level
            return True
        return False

    def check_achievement(self, user_id, achievement_type, data=None):
        if user_id not in self.rewards:
            self.initialize_user(user_id)

        if achievement_type == "workout_streak":
            self.rewards[user_id]["streaks"]["workout"] += 1
            if self.rewards[user_id]["streaks"]["workout"] >= 7:
                self._award_achievement(user_id, "workout_streak")
        elif achievement_type == "emotion_tracking":
            self.rewards[user_id]["streaks"]["emotion"] += 1
            if self.rewards[user_id]["streaks"]["emotion"] >= 5:
                self._award_achievement(user_id, "emotion_tracking")
        elif achievement_type == "goal_achieved":
            self._award_achievement(user_id, "goal_achieved")
        elif achievement_type == "perfect_week":
            self._award_achievement(user_id, "perfect_week")

        self._save_rewards()

    def _award_achievement(self, user_id, achievement_type):
        if achievement_type in self.achievements:
            achievement = self.achievements[achievement_type]
            if achievement_type not in self.rewards[user_id]["achievements"]:
                self.rewards[user_id]["achievements"].append(achievement_type)
                self.add_points(user_id, achievement["points"])
                return True
        return False

    def get_user_status(self, user_id):
        if user_id in self.rewards:
            return {
                "points": self.rewards[user_id]["points"],
                "level": self.rewards[user_id]["level"],
                "achievements": [
                    {
                        "name": self.achievements[ach]["name"],
                        "description": self.achievements[ach]["description"],
                        "points": self.achievements[ach]["points"]
                    }
                    for ach in self.rewards[user_id]["achievements"]
                ],
                "streaks": self.rewards[user_id]["streaks"]
            }
        return None 