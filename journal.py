from datetime import datetime, timedelta
import json
import os

class JournalManager:
    def __init__(self):
        self.journal_file = "journals.json"
        self.journals = self._load_journals()

    def _load_journals(self):
        """Load journals from JSON file"""
        if os.path.exists(self.journal_file):
            with open(self.journal_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_journals(self):
        """Save journals to JSON file"""
        with open(self.journal_file, 'w', encoding='utf-8') as f:
            json.dump(self.journals, f, ensure_ascii=False, indent=4)

    def add_entry(self, user_id, mood, content, tags=None):
        """Add a new journal entry"""
        if user_id not in self.journals:
            self.journals[user_id] = []

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood,
            "content": content,
            "tags": tags or [],
            "gratitude_list": [],
            "goals": [],
            "reflections": []
        }

        self.journals[user_id].append(entry)
        self._save_journals()
        return entry

    def add_gratitude(self, user_id, entry_index, item):
        """Add a gratitude item to a journal entry"""
        if user_id in self.journals and self.journals[user_id]:
            if entry_index == -1:  # Add to the latest entry
                self.journals[user_id][-1]["gratitude_list"].append(item)
            else:
                self.journals[user_id][entry_index]["gratitude_list"].append(item)
            self._save_journals()

    def add_goal(self, user_id, entry_index, goal):
        """Add a goal to a journal entry"""
        if user_id in self.journals and self.journals[user_id]:
            if entry_index == -1:  # Add to the latest entry
                self.journals[user_id][-1]["goals"].append({
                    "text": goal,
                    "completed": False,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                self.journals[user_id][entry_index]["goals"].append({
                    "text": goal,
                    "completed": False,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            self._save_journals()

    def add_reflection(self, user_id, entry_index, reflection):
        """Add a reflection to a journal entry"""
        if user_id in self.journals and self.journals[user_id]:
            if entry_index == -1:  # Add to the latest entry
                self.journals[user_id][-1]["reflections"].append(reflection)
            else:
                self.journals[user_id][entry_index]["reflections"].append(reflection)
            self._save_journals()

    def get_entries(self, user_id, days=None, mood=None, tags=None):
        """Get journal entries with optional filters"""
        if user_id not in self.journals:
            return []

        entries = self.journals[user_id]
        
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            entries = [e for e in entries if datetime.strptime(e["date"], "%Y-%m-%d %H:%M:%S") >= cutoff_date]
        
        if mood:
            entries = [e for e in entries if e["mood"].lower() == mood.lower()]
        
        if tags:
            entries = [e for e in entries if any(tag in e["tags"] for tag in tags)]
        
        return entries

    def get_mood_history(self, user_id, days=7):
        """Get mood history for the specified number of days"""
        entries = self.get_entries(user_id, days=days)
        return [{"date": e["date"], "mood": e["mood"]} for e in entries]

    def get_gratitude_history(self, user_id, days=7):
        """Get gratitude history for the specified number of days"""
        entries = self.get_entries(user_id, days=days)
        gratitude_items = []
        for entry in entries:
            for item in entry["gratitude_list"]:
                gratitude_items.append({
                    "date": entry["date"],
                    "item": item
                })
        return gratitude_items

    def get_goals_progress(self, user_id):
        """Get all goals and their progress"""
        if user_id not in self.journals:
            return []

        goals = []
        for entry in self.journals[user_id]:
            for goal in entry["goals"]:
                goals.append({
                    "date": entry["date"],
                    "goal": goal["text"],
                    "completed": goal["completed"]
                })
        return goals

    def mark_goal_completed(self, user_id, goal_index):
        """Mark a goal as completed"""
        if user_id in self.journals:
            for entry in self.journals[user_id]:
                for goal in entry["goals"]:
                    if goal_index == 0:
                        goal["completed"] = True
                        self._save_journals()
                        return 
                    goal_index -= 1 