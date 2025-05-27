import json
import os
from datetime import datetime, timedelta
import random

class NutritionManager:
    def __init__(self):
        self.nutrition_data_file = "nutrition_data.json"
        self.meals_data_file = "meals_data.json"
        self.nutrition_data = self._load_nutrition_data()
        self.meals_data = self._load_meals_data()

    def _load_nutrition_data(self):
        """Load nutrition data from JSON file"""
        if os.path.exists(self.nutrition_data_file):
            with open(self.nutrition_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}}

    def _load_meals_data(self):
        """Load meals data from JSON file"""
        if os.path.exists(self.meals_data_file):
            with open(self.meals_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "snacks": []
        }

    def _save_nutrition_data(self):
        """Save nutrition data to JSON file"""
        with open(self.nutrition_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.nutrition_data, f, ensure_ascii=False, indent=4)

    def _save_meals_data(self):
        """Save meals data to JSON file"""
        with open(self.meals_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.meals_data, f, ensure_ascii=False, indent=4)

    def add_meal(self, meal_type, name, calories, protein, carbs, fat, ingredients, instructions):
        """Add a new meal to the database"""
        meal = {
            "name": name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "ingredients": ingredients,
            "instructions": instructions,
            "type": meal_type
        }
        self.meals_data[meal_type].append(meal)
        self._save_meals_data()
        return True

    def get_meal_plan(self, user_id, days=7, preferences=None):
        """Generate a meal plan for a user"""
        if preferences is None:
            preferences = {}
        
        meal_plan = []
        for day in range(days):
            daily_meals = {
                "date": (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                "breakfast": self._select_meal("breakfast", preferences),
                "lunch": self._select_meal("lunch", preferences),
                "dinner": self._select_meal("dinner", preferences),
                "snacks": [self._select_meal("snacks", preferences) for _ in range(2)]
            }
            meal_plan.append(daily_meals)
        
        return meal_plan

    def _select_meal(self, meal_type, preferences):
        """Select a meal based on preferences"""
        available_meals = self.meals_data[meal_type]
        if not available_meals:
            return None
        
        # Filter meals based on preferences
        filtered_meals = available_meals
        if "calories" in preferences:
            filtered_meals = [m for m in filtered_meals if m["calories"] <= preferences["calories"]]
        if "dietary_restrictions" in preferences:
            filtered_meals = [m for m in filtered_meals if not any(r in m["ingredients"] for r in preferences["dietary_restrictions"])]
        
        return random.choice(filtered_meals) if filtered_meals else random.choice(available_meals)

    def log_meal(self, user_id, meal_type, meal_name, date=None):
        """Log a meal for a user"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if user_id not in self.nutrition_data["users"]:
            self.nutrition_data["users"][user_id] = {"meals": []}
        
        meal_entry = {
            "date": date,
            "type": meal_type,
            "name": meal_name
        }
        self.nutrition_data["users"][user_id]["meals"].append(meal_entry)
        self._save_nutrition_data()
        return True

    def get_nutrition_summary(self, user_id, days=7):
        """Get nutrition summary for a user"""
        if user_id not in self.nutrition_data["users"]:
            return None
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        meals = [m for m in self.nutrition_data["users"][user_id]["meals"]
                if start_date <= datetime.strptime(m["date"], "%Y-%m-%d") <= end_date]
        
        summary = {
            "total_meals": len(meals),
            "meals_by_type": {},
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }
        
        for meal in meals:
            meal_type = meal["type"]
            if meal_type not in summary["meals_by_type"]:
                summary["meals_by_type"][meal_type] = 0
            summary["meals_by_type"][meal_type] += 1
            
            # Find meal details
            meal_details = next((m for m in self.meals_data[meal_type] if m["name"] == meal["name"]), None)
            if meal_details:
                summary["calories"] += meal_details["calories"]
                summary["protein"] += meal_details["protein"]
                summary["carbs"] += meal_details["carbs"]
                summary["fat"] += meal_details["fat"]
        
        return summary

    def get_meal_suggestions(self, user_id, meal_type, preferences=None):
        """Get meal suggestions based on user preferences"""
        if preferences is None:
            preferences = {}
        
        available_meals = self.meals_data[meal_type]
        if not available_meals:
            return []
        
        # Filter meals based on preferences
        filtered_meals = available_meals
        if "calories" in preferences:
            filtered_meals = [m for m in filtered_meals if m["calories"] <= preferences["calories"]]
        if "dietary_restrictions" in preferences:
            filtered_meals = [m for m in filtered_meals if not any(r in m["ingredients"] for r in preferences["dietary_restrictions"])]
        
        # Sort by calories
        filtered_meals.sort(key=lambda x: x["calories"])
        
        return filtered_meals[:5]  # Return top 5 suggestions

    def update_user_preferences(self, user_id, preferences):
        """Update user's nutrition preferences"""
        if user_id not in self.nutrition_data["users"]:
            self.nutrition_data["users"][user_id] = {"meals": [], "preferences": {}}
        
        self.nutrition_data["users"][user_id]["preferences"] = preferences
        self._save_nutrition_data()
        return True

    def get_user_preferences(self, user_id):
        """Get user's nutrition preferences"""
        if user_id not in self.nutrition_data["users"]:
            return {}
        return self.nutrition_data["users"][user_id].get("preferences", {}) 