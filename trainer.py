from sklearn.tree import DecisionTreeClassifier
import json
import pickle
from sklearn.feature_extraction.text import  CountVectorizer
from sklearn.preprocessing import LabelEncoder
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

with open("TrainingData.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["goal"] + " " + item["feeling"] for item in data]
suggestions = [item["suggestion"] for item in data]

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(texts)

encoder = LabelEncoder()
y = encoder.fit_transform(suggestions)

model = DecisionTreeClassifier()
model.fit(x, y)

with open("ai_model.pkl", "wb") as f:
    pickle.dump(model, f)

class TrainerManager:
    def __init__(self):
        self.trainers_file = "trainers.json"
        self.sessions_file = "training_sessions.json"
        self.reviews_file = "trainer_reviews.json"
        self._load_data()

    def _load_data(self):
        """Load trainers and sessions data from JSON files"""
        if os.path.exists(self.trainers_file):
            with open(self.trainers_file, 'r', encoding='utf-8') as f:
                self.trainers = json.load(f)
        else:
            self.trainers = {}

        if os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}

        if os.path.exists(self.reviews_file):
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                self.reviews = json.load(f)
        else:
            self.reviews = {}

    def _save_data(self):
        """Save trainers and sessions data to JSON files"""
        with open(self.trainers_file, 'w', encoding='utf-8') as f:
            json.dump(self.trainers, f, ensure_ascii=False, indent=4)
        
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=4)
        
        with open(self.reviews_file, 'w', encoding='utf-8') as f:
            json.dump(self.reviews, f, ensure_ascii=False, indent=4)

    def register_trainer(self, name: str, email: str, specialties: List[str], 
                        certifications: List[str], experience_years: int,
                        languages: List[str], hourly_rate: float) -> str:
        """Register a new trainer"""
        trainer_id = str(uuid.uuid4())
        self.trainers[trainer_id] = {
            "name": name,
            "email": email,
            "specialties": specialties,
            "certifications": certifications,
            "experience_years": experience_years,
            "languages": languages,
            "hourly_rate": hourly_rate,
            "rating": 0.0,
            "total_reviews": 0,
            "availability": {},
            "clients": [],
            "created_at": datetime.now().isoformat()
        }
        self._save_data()
        return trainer_id

    def update_trainer_availability(self, trainer_id: str, 
                                  availability: Dict[str, List[str]]) -> bool:
        """Update trainer's availability schedule"""
        if trainer_id not in self.trainers:
            return False
        
        self.trainers[trainer_id]["availability"] = availability
        self._save_data()
        return True

    def book_session(self, trainer_id: str, client_id: str, 
                    date: str, time: str, duration: int,
                    session_type: str) -> str:
        """Book a training session with a trainer"""
        if trainer_id not in self.trainers:
            return None

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "trainer_id": trainer_id,
            "client_id": client_id,
            "date": date,
            "time": time,
            "duration": duration,
            "session_type": session_type,
            "status": "scheduled",
            "notes": "",
            "created_at": datetime.now().isoformat()
        }

        # Add client to trainer's client list if not already there
        if client_id not in self.trainers[trainer_id]["clients"]:
            self.trainers[trainer_id]["clients"].append(client_id)

        self._save_data()
        return session_id

    def cancel_session(self, session_id: str) -> bool:
        """Cancel a scheduled training session"""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id]["status"] = "cancelled"
        self._save_data()
        return True

    def add_session_notes(self, session_id: str, notes: str) -> bool:
        """Add notes to a training session"""
        if session_id not in self.sessions:
            return False
        
        self.sessions[session_id]["notes"] = notes
        self._save_data()
        return True

    def add_trainer_review(self, trainer_id: str, client_id: str,
                          rating: float, comment: str) -> bool:
        """Add a review for a trainer"""
        if trainer_id not in self.trainers:
            return False

        review_id = str(uuid.uuid4())
        self.reviews[review_id] = {
            "trainer_id": trainer_id,
            "client_id": client_id,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.now().isoformat()
        }

        # Update trainer's average rating
        trainer = self.trainers[trainer_id]
        total_rating = trainer["rating"] * trainer["total_reviews"]
        trainer["total_reviews"] += 1
        trainer["rating"] = (total_rating + rating) / trainer["total_reviews"]

        self._save_data()
        return True

    def get_trainer_profile(self, trainer_id: str) -> Optional[Dict]:
        """Get trainer's profile information"""
        return self.trainers.get(trainer_id)

    def get_trainer_sessions(self, trainer_id: str, 
                           start_date: Optional[str] = None,
                           end_date: Optional[str] = None) -> List[Dict]:
        """Get trainer's sessions within a date range"""
        sessions = []
        for session_id, session in self.sessions.items():
            if session["trainer_id"] == trainer_id:
                if start_date and session["date"] < start_date:
                    continue
                if end_date and session["date"] > end_date:
                    continue
                sessions.append(session)
        return sessions

    def get_trainer_reviews(self, trainer_id: str) -> List[Dict]:
        """Get all reviews for a trainer"""
        return [review for review in self.reviews.values() 
                if review["trainer_id"] == trainer_id]

    def search_trainers(self, specialty: Optional[str] = None,
                       min_rating: Optional[float] = None,
                       max_rate: Optional[float] = None,
                       language: Optional[str] = None) -> List[Dict]:
        """Search for trainers based on criteria"""
        results = []
        for trainer_id, trainer in self.trainers.items():
            if specialty and specialty not in trainer["specialties"]:
                continue
            if min_rating and trainer["rating"] < min_rating:
                continue
            if max_rate and trainer["hourly_rate"] > max_rate:
                continue
            if language and language not in trainer["languages"]:
                continue
            results.append({"id": trainer_id, **trainer})
        return results

    def get_client_trainers(self, client_id: str) -> List[Dict]:
        """Get all trainers associated with a client"""
        trainers = []
        for trainer_id, trainer in self.trainers.items():
            if client_id in trainer["clients"]:
                trainers.append({"id": trainer_id, **trainer})
        return trainers

    def get_upcoming_sessions(self, client_id: str) -> List[Dict]:
        """Get client's upcoming training sessions"""
        upcoming = []
        now = datetime.now()
        for session_id, session in self.sessions.items():
            if session["client_id"] == client_id:
                session_date = datetime.fromisoformat(session["date"])
                if session_date > now and session["status"] == "scheduled":
                    upcoming.append(session)
        return sorted(upcoming, key=lambda x: x["date"])

    def get_session_history(self, client_id: str) -> List[Dict]:
        """Get client's past training sessions"""
        history = []
        now = datetime.now()
        for session_id, session in self.sessions.items():
            if session["client_id"] == client_id:
                session_date = datetime.fromisoformat(session["date"])
                if session_date < now:
                    history.append(session)
        return sorted(history, key=lambda x: x["date"], reverse=True)

    