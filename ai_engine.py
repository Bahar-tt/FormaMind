import json
import os
from datetime import datetime, timedelta
import random
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class AIEngine:
    def __init__(self):
        self.ai_data_file = "ai_data.json"
        self.ai_data = self._load_ai_data()
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.emotion_patterns = {
            "happy": ["exercise", "social", "creative"],
            "sad": ["rest", "self_care", "social"],
            "stressed": ["meditation", "exercise", "nature"],
            "tired": ["rest", "nutrition", "sleep"],
            "energetic": ["exercise", "creative", "social"]
        }

    def _load_ai_data(self):
        """Load AI data from JSON file"""
        if os.path.exists(self.ai_data_file):
            with open(self.ai_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "user_patterns": {},
            "activity_recommendations": {},
            "weather_adaptations": {},
            "emotion_insights": {}
        }

    def _save_ai_data(self):
        """Save AI data to JSON file"""
        with open(self.ai_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.ai_data, f, ensure_ascii=False, indent=4)

    def learn_user_patterns(self, user_id, activity_data, emotion_data, weather_data):
        """Learn patterns from user's activity and emotion data"""
        if user_id not in self.ai_data["user_patterns"]:
            self.ai_data["user_patterns"][user_id] = {
                "activity_patterns": [],
                "emotion_patterns": [],
                "weather_patterns": []
            }

        # Process activity patterns
        activity_features = self._extract_activity_features(activity_data)
        if activity_features:
            self.ai_data["user_patterns"][user_id]["activity_patterns"].append(activity_features)

        # Process emotion patterns
        emotion_features = self._extract_emotion_features(emotion_data)
        if emotion_features:
            self.ai_data["user_patterns"][user_id]["emotion_patterns"].append(emotion_features)

        # Process weather patterns
        weather_features = self._extract_weather_features(weather_data)
        if weather_features:
            self.ai_data["user_patterns"][user_id]["weather_patterns"].append(weather_features)

        self._save_ai_data()
        return True

    def _extract_activity_features(self, activity_data):
        """Extract features from activity data"""
        if not activity_data:
            return None

        features = {
            "time_of_day": activity_data.get("time_of_day"),
            "duration": activity_data.get("duration"),
            "intensity": activity_data.get("intensity"),
            "type": activity_data.get("type"),
            "location": activity_data.get("location")
        }
        return features

    def _extract_emotion_features(self, emotion_data):
        """Extract features from emotion data"""
        if not emotion_data:
            return None

        features = {
            "emotion": emotion_data.get("emotion"),
            "intensity": emotion_data.get("intensity"),
            "triggers": emotion_data.get("triggers"),
            "time_of_day": emotion_data.get("time_of_day")
        }
        return features

    def _extract_weather_features(self, weather_data):
        """Extract features from weather data"""
        if not weather_data:
            return None

        features = {
            "temperature": weather_data.get("temperature"),
            "condition": weather_data.get("condition"),
            "humidity": weather_data.get("humidity"),
            "time_of_day": weather_data.get("time_of_day")
        }
        return features

    def get_personalized_recommendations(self, user_id, current_emotion, current_weather):
        """Get personalized recommendations based on user patterns"""
        if user_id not in self.ai_data["user_patterns"]:
            return self._get_default_recommendations(current_emotion)

        user_patterns = self.ai_data["user_patterns"][user_id]
        
        # Get activity recommendations based on patterns
        activity_recs = self._get_activity_recommendations(user_patterns, current_emotion)
        
        # Adapt recommendations based on weather
        weather_adapted_recs = self._adapt_to_weather(activity_recs, current_weather)
        
        # Add emotion-specific recommendations
        emotion_recs = self._get_emotion_recommendations(current_emotion)
        
        return {
            "activities": weather_adapted_recs,
            "emotion_support": emotion_recs,
            "weather_considerations": self._get_weather_considerations(current_weather)
        }

    def _get_activity_recommendations(self, user_patterns, current_emotion):
        """Get activity recommendations based on user patterns"""
        recommendations = []
        
        # Analyze activity patterns
        if user_patterns["activity_patterns"]:
            # Use K-means clustering to find common patterns
            features = np.array([list(p.values()) for p in user_patterns["activity_patterns"]])
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            kmeans = KMeans(n_clusters=min(3, len(features_scaled)))
            clusters = kmeans.fit_predict(features_scaled)
            
            # Get most common activities in each cluster
            for cluster in range(kmeans.n_clusters):
                cluster_activities = [p["type"] for i, p in enumerate(user_patterns["activity_patterns"])
                                    if clusters[i] == cluster]
                if cluster_activities:
                    recommendations.append(random.choice(cluster_activities))

        # Add emotion-based recommendations
        if current_emotion in self.emotion_patterns:
            recommendations.extend(self.emotion_patterns[current_emotion])

        return list(set(recommendations))  # Remove duplicates

    def _adapt_to_weather(self, recommendations, weather):
        """Adapt recommendations based on weather conditions"""
        adapted_recs = []
        
        for rec in recommendations:
            if weather["condition"] in ["rain", "snow"]:
                if rec in ["outdoor_exercise", "nature"]:
                    adapted_recs.append("indoor_" + rec)
                else:
                    adapted_recs.append(rec)
            elif weather["temperature"] > 30:  # Hot weather
                if rec in ["intense_exercise", "outdoor_exercise"]:
                    adapted_recs.append("light_" + rec)
                else:
                    adapted_recs.append(rec)
            else:
                adapted_recs.append(rec)
        
        return adapted_recs

    def _get_emotion_recommendations(self, emotion):
        """Get recommendations specific to current emotion"""
        if emotion in self.emotion_patterns:
            return {
                "activities": self.emotion_patterns[emotion],
                "tips": self._get_emotion_tips(emotion)
            }
        return {"activities": [], "tips": []}

    def _get_emotion_tips(self, emotion):
        """Get tips for managing specific emotions"""
        tips = {
            "happy": [
                "Share your positive energy with others",
                "Document what made you happy",
                "Plan activities to maintain this mood"
            ],
            "sad": [
                "Practice self-care activities",
                "Connect with supportive friends",
                "Engage in gentle physical activity"
            ],
            "stressed": [
                "Take deep breaths",
                "Practice mindfulness",
                "Break tasks into smaller steps"
            ],
            "tired": [
                "Ensure adequate sleep",
                "Stay hydrated",
                "Take short breaks throughout the day"
            ],
            "energetic": [
                "Channel energy into productive activities",
                "Try new challenges",
                "Share your enthusiasm with others"
            ]
        }
        return tips.get(emotion, [])

    def _get_weather_considerations(self, weather):
        """Get considerations based on current weather"""
        considerations = []
        
        if weather["condition"] in ["rain", "snow"]:
            considerations.append("Consider indoor activities")
            considerations.append("Stay dry and warm")
        elif weather["temperature"] > 30:
            considerations.append("Stay hydrated")
            considerations.append("Avoid peak sun hours")
        elif weather["temperature"] < 10:
            considerations.append("Dress warmly")
            considerations.append("Consider indoor alternatives")
        
        return considerations

    def _get_default_recommendations(self, emotion):
        """Get default recommendations when no user patterns exist"""
        return {
            "activities": self.emotion_patterns.get(emotion, ["walking", "meditation", "reading"]),
            "emotion_support": self._get_emotion_recommendations(emotion),
            "weather_considerations": []
        }

    def analyze_emotion_patterns(self, user_id, days=30):
        """Analyze emotion patterns over time"""
        if user_id not in self.ai_data["user_patterns"]:
            return None

        emotion_patterns = self.ai_data["user_patterns"][user_id]["emotion_patterns"]
        if not emotion_patterns:
            return None

        # Filter patterns for the specified time period
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        recent_patterns = [p for p in emotion_patterns
                         if start_date <= datetime.strptime(p.get("time_of_day", ""), "%Y-%m-%d %H:%M:%S") <= end_date]

        if not recent_patterns:
            return None

        # Analyze patterns
        analysis = {
            "emotion_frequency": {},
            "common_triggers": {},
            "time_patterns": {},
            "intensity_trends": {}
        }

        for pattern in recent_patterns:
            # Count emotion frequencies
            emotion = pattern.get("emotion")
            if emotion:
                analysis["emotion_frequency"][emotion] = analysis["emotion_frequency"].get(emotion, 0) + 1

            # Analyze triggers
            triggers = pattern.get("triggers", [])
            for trigger in triggers:
                analysis["common_triggers"][trigger] = analysis["common_triggers"].get(trigger, 0) + 1

            # Analyze time patterns
            time = pattern.get("time_of_day")
            if time:
                hour = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").hour
                time_slot = f"{hour:02d}:00"
                analysis["time_patterns"][time_slot] = analysis["time_patterns"].get(time_slot, 0) + 1

            # Track intensity trends
            intensity = pattern.get("intensity")
            if intensity:
                if emotion not in analysis["intensity_trends"]:
                    analysis["intensity_trends"][emotion] = []
                analysis["intensity_trends"][emotion].append(intensity)

        return analysis 