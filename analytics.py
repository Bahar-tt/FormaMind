import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

class Analytics:
    def __init__(self):
        self.data_dir = "analytics_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def generate_progress_report(self, user_id, days=30):
        """Generate a comprehensive progress report"""
        report = {
            "workout_stats": self._analyze_workouts(user_id, days),
            "mood_stats": self._analyze_moods(user_id, days),
            "meditation_stats": self._analyze_meditation(user_id, days),
            "goals_progress": self._analyze_goals(user_id),
            "streaks": self._analyze_streaks(user_id),
            "recommendations": self._generate_recommendations(user_id)
        }
        
        # Save report
        report_file = os.path.join(self.data_dir, f"report_{user_id}_{datetime.now().strftime('%Y%m%d')}.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
        
        return report

    def _analyze_workouts(self, user_id, days):
        """Analyze workout data"""
        try:
            with open('user_profiles.json', 'r', encoding='utf-8') as f:
                profiles = json.load(f)
            
            if user_id not in profiles:
                return {}
            
            workouts = profiles[user_id].get('workout_history', [])
            recent_workouts = [w for w in workouts if 
                             datetime.strptime(w['date'], "%Y-%m-%d %H:%M:%S") >= 
                             datetime.now() - timedelta(days=days)]
            
            stats = {
                "total_workouts": len(recent_workouts),
                "total_duration": sum(w.get('duration', 0) for w in recent_workouts),
                "workout_types": defaultdict(int),
                "weekly_distribution": defaultdict(int),
                "average_duration": 0
            }
            
            for workout in recent_workouts:
                stats["workout_types"][workout['type']] += 1
                stats["weekly_distribution"][datetime.strptime(workout['date'], "%Y-%m-%d %H:%M:%S").strftime("%A")] += 1
            
            if recent_workouts:
                stats["average_duration"] = stats["total_duration"] / len(recent_workouts)
            
            return stats
        except Exception as e:
            print(f"Error analyzing workouts: {e}")
            return {}

    def _analyze_moods(self, user_id, days):
        """Analyze mood data"""
        try:
            with open('journals.json', 'r', encoding='utf-8') as f:
                journals = json.load(f)
            
            if user_id not in journals:
                return {}
            
            entries = journals[user_id]
            recent_entries = [e for e in entries if 
                            datetime.strptime(e['date'], "%Y-%m-%d %H:%M:%S") >= 
                            datetime.now() - timedelta(days=days)]
            
            stats = {
                "mood_distribution": defaultdict(int),
                "mood_trend": [],
                "common_tags": defaultdict(int),
                "gratitude_count": sum(len(e.get('gratitude_list', [])) for e in recent_entries)
            }
            
            for entry in recent_entries:
                stats["mood_distribution"][entry['mood']] += 1
                stats["mood_trend"].append({
                    "date": entry['date'],
                    "mood": entry['mood']
                })
                for tag in entry.get('tags', []):
                    stats["common_tags"][tag] += 1
            
            return stats
        except Exception as e:
            print(f"Error analyzing moods: {e}")
            return {}

    def _analyze_meditation(self, user_id, days):
        """Analyze meditation data"""
        try:
            with open('mind_exercises.json', 'r', encoding='utf-8') as f:
                exercises = json.load(f)
            
            stats = {
                "total_sessions": 0,
                "total_duration": 0,
                "preferred_types": defaultdict(int),
                "preferred_times": defaultdict(int)
            }
            
            # Add meditation tracking logic here
            
            return stats
        except Exception as e:
            print(f"Error analyzing meditation: {e}")
            return {}

    def _analyze_goals(self, user_id):
        """Analyze goals progress"""
        try:
            with open('journals.json', 'r', encoding='utf-8') as f:
                journals = json.load(f)
            
            if user_id not in journals:
                return {}
            
            stats = {
                "total_goals": 0,
                "completed_goals": 0,
                "completion_rate": 0,
                "goals_by_category": defaultdict(int)
            }
            
            for entry in journals[user_id]:
                for goal in entry.get('goals', []):
                    stats["total_goals"] += 1
                    if goal.get('completed', False):
                        stats["completed_goals"] += 1
            
            if stats["total_goals"] > 0:
                stats["completion_rate"] = (stats["completed_goals"] / stats["total_goals"]) * 100
            
            return stats
        except Exception as e:
            print(f"Error analyzing goals: {e}")
            return {}

    def _analyze_streaks(self, user_id):
        """Analyze user streaks"""
        try:
            with open('rewards.json', 'r', encoding='utf-8') as f:
                rewards = json.load(f)
            
            if user_id not in rewards:
                return {}
            
            return rewards[user_id].get('streaks', {})
        except Exception as e:
            print(f"Error analyzing streaks: {e}")
            return {}

    def _generate_recommendations(self, user_id):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Analyze workout patterns
        workout_stats = self._analyze_workouts(user_id, 30)
        if workout_stats.get("total_workouts", 0) < 3:
            recommendations.append("Try to increase your workout frequency to at least 3 times per week")
        
        # Analyze mood patterns
        mood_stats = self._analyze_moods(user_id, 30)
        if mood_stats.get("gratitude_count", 0) < 5:
            recommendations.append("Consider practicing gratitude more often")
        
        # Analyze goals
        goals_stats = self._analyze_goals(user_id)
        if goals_stats.get("completion_rate", 0) < 50:
            recommendations.append("Try setting smaller, more achievable goals")
        
        return recommendations

    def generate_visualizations(self, user_id, days=30):
        """Generate visual representations of user data"""
        # Create visualizations directory
        viz_dir = os.path.join(self.data_dir, "visualizations")
        if not os.path.exists(viz_dir):
            os.makedirs(viz_dir)
        
        # Generate mood trend plot
        mood_stats = self._analyze_moods(user_id, days)
        if mood_stats.get("mood_trend"):
            plt.figure(figsize=(10, 6))
            dates = [datetime.strptime(m["date"], "%Y-%m-%d %H:%M:%S") for m in mood_stats["mood_trend"]]
            moods = [m["mood"] for m in mood_stats["mood_trend"]]
            plt.plot(dates, moods)
            plt.title("Mood Trend")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, f"mood_trend_{user_id}.png"))
            plt.close()
        
        # Generate workout distribution plot
        workout_stats = self._analyze_workouts(user_id, days)
        if workout_stats.get("workout_types"):
            plt.figure(figsize=(10, 6))
            types = list(workout_stats["workout_types"].keys())
            counts = list(workout_stats["workout_types"].values())
            plt.bar(types, counts)
            plt.title("Workout Type Distribution")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, f"workout_distribution_{user_id}.png"))
            plt.close()
        
        # Generate goals progress plot
        goals_stats = self._analyze_goals(user_id)
        if goals_stats.get("total_goals", 0) > 0:
            plt.figure(figsize=(8, 8))
            labels = ['Completed', 'Remaining']
            sizes = [goals_stats["completed_goals"], 
                    goals_stats["total_goals"] - goals_stats["completed_goals"]]
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title("Goals Progress")
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, f"goals_progress_{user_id}.png"))
            plt.close() 