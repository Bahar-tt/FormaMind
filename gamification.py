import json
import os
from datetime import datetime, timedelta
import random

class GamificationEngine:
    def __init__(self):
        self.gamification_data_file = "gamification_data.json"
        self.gamification_data = self._load_gamification_data()
        self.achievements = {
            "workout": {
                "beginner": [
                    {"name": "First Steps", "description": "Complete your first workout", "points": 50},
                    {"name": "Consistency", "description": "Complete 5 workouts in a week", "points": 100},
                    {"name": "Endurance", "description": "Complete a 30-minute workout", "points": 75}
                ],
                "intermediate": [
                    {"name": "Power Builder", "description": "Complete 10 strength workouts", "points": 150},
                    {"name": "Cardio Master", "description": "Complete 5 cardio sessions", "points": 150},
                    {"name": "Flexibility Pro", "description": "Complete 7 flexibility sessions", "points": 150}
                ],
                "advanced": [
                    {"name": "Workout Warrior", "description": "Complete 20 workouts in a month", "points": 300},
                    {"name": "Intensity King", "description": "Complete 5 high-intensity workouts", "points": 250},
                    {"name": "Variety Seeker", "description": "Try 5 different types of workouts", "points": 200}
                ]
            },
            "mindfulness": {
                "beginner": [
                    {"name": "Mindful Start", "description": "Complete your first meditation", "points": 50},
                    {"name": "Daily Practice", "description": "Meditate for 5 days in a row", "points": 100},
                    {"name": "Emotion Explorer", "description": "Track your mood for 7 days", "points": 75}
                ],
                "intermediate": [
                    {"name": "Zen Master", "description": "Complete 10 meditation sessions", "points": 150},
                    {"name": "Journal Journey", "description": "Write 5 journal entries", "points": 150},
                    {"name": "Emotion Expert", "description": "Track 10 different emotions", "points": 150}
                ],
                "advanced": [
                    {"name": "Mindfulness Guru", "description": "Meditate for 30 days straight", "points": 300},
                    {"name": "Deep Reflection", "description": "Write 20 journal entries", "points": 250},
                    {"name": "Emotion Master", "description": "Track emotions for 30 days", "points": 200}
                ]
            },
            "nutrition": {
                "beginner": [
                    {"name": "Healthy Start", "description": "Log your first meal", "points": 50},
                    {"name": "Meal Tracker", "description": "Log meals for 3 days", "points": 100},
                    {"name": "Water Champion", "description": "Track water intake for 5 days", "points": 75}
                ],
                "intermediate": [
                    {"name": "Nutrition Expert", "description": "Log meals for 7 days", "points": 150},
                    {"name": "Healthy Choices", "description": "Log 10 healthy meals", "points": 150},
                    {"name": "Hydration Hero", "description": "Meet water goals for 7 days", "points": 150}
                ],
                "advanced": [
                    {"name": "Nutrition Master", "description": "Log meals for 30 days", "points": 300},
                    {"name": "Meal Planner", "description": "Follow meal plan for 14 days", "points": 250},
                    {"name": "Healthy Lifestyle", "description": "Maintain healthy habits for 30 days", "points": 200}
                ]
            }
        }
        self.badges = {
            "workout": [
                {"name": "Early Bird", "description": "Complete a workout before 8 AM", "icon": "🌅"},
                {"name": "Night Owl", "description": "Complete a workout after 8 PM", "icon": "🌙"},
                {"name": "Weekend Warrior", "description": "Complete workouts on both weekend days", "icon": "🏆"}
            ],
            "mindfulness": [
                {"name": "Zen Master", "description": "Complete 5 meditation sessions", "icon": "🧘"},
                {"name": "Emotion Explorer", "description": "Track 5 different emotions", "icon": "😊"},
                {"name": "Journal Keeper", "description": "Write 5 journal entries", "icon": "📝"}
            ],
            "nutrition": [
                {"name": "Healthy Eater", "description": "Log 5 healthy meals", "icon": "🥗"},
                {"name": "Water Lover", "description": "Meet water goals for 5 days", "icon": "💧"},
                {"name": "Meal Planner", "description": "Follow meal plan for 5 days", "icon": "📋"}
            ]
        }
        self.levels = [
            {"level": 1, "points_required": 0, "title": "Beginner"},
            {"level": 2, "points_required": 500, "title": "Enthusiast"},
            {"level": 3, "points_required": 1000, "title": "Regular"},
            {"level": 4, "points_required": 2000, "title": "Dedicated"},
            {"level": 5, "points_required": 3500, "title": "Expert"},
            {"level": 6, "points_required": 5000, "title": "Master"},
            {"level": 7, "points_required": 7500, "title": "Elite"},
            {"level": 8, "points_required": 10000, "title": "Legend"}
        ]

    def _load_gamification_data(self):
        """Load gamification data from JSON file"""
        if os.path.exists(self.gamification_data_file):
            with open(self.gamification_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}

    def _save_gamification_data(self):
        """Save gamification data to JSON file"""
        with open(self.gamification_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.gamification_data, f, ensure_ascii=False, indent=4)

    def initialize_user(self, user_id):
        """Initialize gamification data for a new user"""
        if user_id not in self.gamification_data["users"]:
            self.gamification_data["users"][user_id] = {
                "points": 0,
                "level": 1,
                "achievements": [],
                "badges": [],
                "streaks": {
                    "workout": 0,
                    "mindfulness": 0,
                    "nutrition": 0
                },
                "daily_challenges": [],
                "rewards": []
            }
            self._save_gamification_data()
            return True
        return False

    def add_points(self, user_id, points, category):
        """Add points to user's total and check for level up"""
        if user_id not in self.gamification_data["users"]:
            self.initialize_user(user_id)

        user_data = self.gamification_data["users"][user_id]
        user_data["points"] += points

        # Check for level up
        current_level = user_data["level"]
        for level in self.levels:
            if user_data["points"] >= level["points_required"]:
                current_level = level["level"]

        if current_level > user_data["level"]:
            user_data["level"] = current_level
            self._add_reward(user_id, f"Level {current_level} Achieved!", "level_up")

        self._save_gamification_data()
        return user_data["points"]

    def check_achievement(self, user_id, category, action, level="beginner"):
        """Check if user has earned an achievement"""
        if user_id not in self.gamification_data["users"]:
            return None

        user_data = self.gamification_data["users"][user_id]
        achievements = self.achievements.get(category, {}).get(level, [])

        for achievement in achievements:
            if achievement["name"] not in [a["name"] for a in user_data["achievements"]]:
                # Check achievement conditions based on action
                if self._check_achievement_conditions(user_id, category, achievement, action):
                    user_data["achievements"].append(achievement)
                    self.add_points(user_id, achievement["points"], category)
                    self._add_reward(user_id, f"Achievement Unlocked: {achievement['name']}", "achievement")
                    return achievement

        return None

    def _check_achievement_conditions(self, user_id, category, achievement, action):
        """Check if achievement conditions are met"""
        # This is a simplified version - in a real app, you'd have more complex conditions
        if achievement["name"] == "First Steps" and category == "workout":
            return True
        elif achievement["name"] == "Consistency" and category == "workout":
            return self._check_streak(user_id, "workout", 5)
        elif achievement["name"] == "Daily Practice" and category == "mindfulness":
            return self._check_streak(user_id, "mindfulness", 5)
        return False

    def _check_streak(self, user_id, category, required_days):
        """Check if user has maintained a streak for required days"""
        user_data = self.gamification_data["users"][user_id]
        return user_data["streaks"][category] >= required_days

    def update_streak(self, user_id, category):
        """Update user's streak for a category"""
        if user_id not in self.gamification_data["users"]:
            return 0

        user_data = self.gamification_data["users"][user_id]
        user_data["streaks"][category] += 1

        # Check for streak achievements
        if user_data["streaks"][category] in [5, 10, 30]:
            self._add_reward(user_id, f"{category.capitalize()} Streak: {user_data['streaks'][category]} days!", "streak")

        self._save_gamification_data()
        return user_data["streaks"][category]

    def get_daily_challenge(self, user_id):
        """Generate a daily challenge for the user"""
        if user_id not in self.gamification_data["users"]:
            return None

        user_data = self.gamification_data["users"][user_id]
        user_level = user_data["level"]

        # Generate challenge based on user level
        if user_level <= 3:
            challenge = self._generate_beginner_challenge()
        elif user_level <= 6:
            challenge = self._generate_intermediate_challenge()
        else:
            challenge = self._generate_advanced_challenge()

        user_data["daily_challenges"].append(challenge)
        self._save_gamification_data()
        return challenge

    def _generate_beginner_challenge(self):
        """Generate a beginner-level challenge"""
        challenges = [
            {"type": "workout", "description": "Complete a 15-minute workout", "points": 50},
            {"type": "mindfulness", "description": "Meditate for 5 minutes", "points": 50},
            {"type": "nutrition", "description": "Log your meals for the day", "points": 50}
        ]
        return random.choice(challenges)

    def _generate_intermediate_challenge(self):
        """Generate an intermediate-level challenge"""
        challenges = [
            {"type": "workout", "description": "Complete a 30-minute workout", "points": 100},
            {"type": "mindfulness", "description": "Meditate for 10 minutes", "points": 100},
            {"type": "nutrition", "description": "Log 3 healthy meals", "points": 100}
        ]
        return random.choice(challenges)

    def _generate_advanced_challenge(self):
        """Generate an advanced-level challenge"""
        challenges = [
            {"type": "workout", "description": "Complete a 45-minute high-intensity workout", "points": 150},
            {"type": "mindfulness", "description": "Meditate for 20 minutes", "points": 150},
            {"type": "nutrition", "description": "Follow your meal plan perfectly", "points": 150}
        ]
        return random.choice(challenges)

    def _add_reward(self, user_id, description, reward_type):
        """Add a reward to user's rewards list"""
        if user_id not in self.gamification_data["users"]:
            return

        reward = {
            "description": description,
            "type": reward_type,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.gamification_data["users"][user_id]["rewards"].append(reward)
        self._save_gamification_data()

    def get_user_stats(self, user_id):
        """Get user's gamification statistics"""
        if user_id not in self.gamification_data["users"]:
            return None

        user_data = self.gamification_data["users"][user_id]
        current_level = next(level for level in self.levels if level["level"] == user_data["level"])
        next_level = next((level for level in self.levels if level["level"] == user_data["level"] + 1), None)

        return {
            "points": user_data["points"],
            "level": user_data["level"],
            "level_title": current_level["title"],
            "points_to_next_level": next_level["points_required"] - user_data["points"] if next_level else 0,
            "achievements": user_data["achievements"],
            "badges": user_data["badges"],
            "streaks": user_data["streaks"],
            "rewards": user_data["rewards"]
        }

    def get_leaderboard(self, category=None):
        """Get leaderboard for all users or specific category"""
        users = self.gamification_data["users"]
        leaderboard = []

        for user_id, user_data in users.items():
            entry = {
                "user_id": user_id,
                "points": user_data["points"],
                "level": user_data["level"],
                "achievements": len(user_data["achievements"]),
                "streaks": user_data["streaks"]
            }
            leaderboard.append(entry)

        # Sort by points
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        return leaderboard[:10]  # Return top 10 users 