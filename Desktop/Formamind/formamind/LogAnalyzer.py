import json
from collections import Counter

class LogAnalyzer:
    def __init__(self, filename="user_log.json"):
        self.filename = filename

    def summarize_logs(self):
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return "No log data found yet."
    
        if not data:
            return "No log entries to analyze."
        
        goals = [entry["goal"] for entry in data]
        feelings = [entry["feeling"] for entry in data]
        confirmed_count = sum(1 for entry in data if entry["confirmed"] == "Yes")

        goal_summary = Counter(goals)
        feeling_summary = Counter(feelings)

        summery = [
            f"Total entries: {len(data)}", f"Confirmed suggestion: {confirmed_count}", "Goal summary: "
        ]
        for goal, count in goal_summary.items():
            summery.append(f" {goal}: {count} times")

        summery.append("Feeling summary: ")
        for feeling, count in feeling_summary.items():
            summery.append(f" {feeling}: {count} times")
        return "\n".join(summery)
 
    