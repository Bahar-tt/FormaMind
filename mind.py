from datetime import datetime
import json
import os
import random

class MindEngine:
    def __init__(self, feeling):
        self.feeling = feeling
        self.exercises = self._load_exercises()
        self.meditation_types = {
            "breathing": {
                "beginner": [
                    {
                        "name": "Box Breathing",
                        "duration": 5,
                        "steps": [
                            "Breathe in for 4 counts",
                            "Hold for 4 counts",
                            "Exhale for 4 counts",
                            "Hold for 4 counts"
                        ]
                    },
                    {
                        "name": "Deep Breathing",
                        "duration": 3,
                        "steps": [
                            "Take a deep breath through your nose",
                            "Feel your belly expand",
                            "Exhale slowly through your mouth"
                        ]
                    }
                ],
                "intermediate": [
                    {
                        "name": "4-7-8 Breathing",
                        "duration": 7,
                        "steps": [
                            "Inhale through nose for 4 counts",
                            "Hold for 7 counts",
                            "Exhale through mouth for 8 counts"
                        ]
                    }
                ],
                "advanced": [
                    {
                        "name": "Alternate Nostril Breathing",
                        "duration": 10,
                        "steps": [
                            "Close right nostril and inhale through left",
                            "Close left nostril and exhale through right",
                            "Repeat"
                        ]
                    }
                ]
            },
            "mindfulness": {
                "beginner": [
                    {
                        "name": "Body Scan",
                        "duration": 10,
                        "steps": [
                            "Lie down comfortably",
                            "Focus on each part of your body",
                            "Notice sensations without judgment"
                        ]
                    }
                ],
                "intermediate": [
                    {
                        "name": "Walking Meditation",
                        "duration": 15,
                        "steps": [
                            "Walk slowly and mindfully",
                            "Focus on each step",
                            "Notice your surroundings"
                        ]
                    }
                ],
                "advanced": [
                    {
                        "name": "Open Monitoring Meditation",
                        "duration": 20,
                        "steps": [
                            "Sit comfortably",
                            "Observe thoughts and sensations",
                            "Let them pass without judgment"
                        ]
                    }
                ]
            }
        }

    def _load_exercises(self):
        try:
            with open('mind_exercises.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Provide default exercises for tests
            return {
                "mood_tracking": {
                    "suggested_activities": [
                        "Take a nature walk",
                        "Practice deep breathing",
                        "Listen to calming music",
                        "Do some gentle stretching",
                        "Practice relaxation",
                        "Practice breathing exercises"
                    ],
                    "journal_prompts": [
                        "What triggered my anxiety today?",
                        "What coping strategies worked for me?",
                        "What am I looking forward to?",
                        "What can I do to take care of myself?"
                    ]
                },
                "cognitive_techniques": [
                    "Cognitive restructuring",
                    "Thought challenging"
                ]
            }

    def create_meditation_session(self, user_id, duration, type, level):
        """ایجاد جلسه مدیتیشن با اعتبارسنجی"""
        if duration <= 0:
            raise ValueError("مدت زمان باید بزرگتر از صفر باشد")
        if type not in self.meditation_types:
            raise ValueError("نوع مدیتیشن نامعتبر است")
        if level not in self.meditation_types[type]:
            raise ValueError("سطح مدیتیشن نامعتبر است")
        # انتخاب یک تمرین مناسب
        session = random.choice(self.meditation_types[type][level])
        return {
            "user_id": user_id,
            "duration": duration,
            "type": type,
            "level": level,
            "name": session["name"],
            "steps": session["steps"]
        }

    def get_exercise(self, exercise_type="meditation", level="beginner"):
        """Get a random exercise of the specified type and level"""
        if exercise_type == "meditation":
            # Provide a default meditation if not found
            for t in self.meditation_types:
                if level in self.meditation_types[t]:
                    return random.choice(self.meditation_types[t][level])
            return None
        if exercise_type in self.exercises and level in self.exercises[exercise_type]:
            exercises = self.exercises[exercise_type][level]
            return random.choice(exercises)
        return None

    def get_mood_tracking(self):
        """Get mood tracking information"""
        return self.exercises.get("mood_tracking", {})

    def get_cognitive_techniques(self):
        """Get cognitive techniques"""
        return self.exercises.get("cognitive_techniques", [])

    def get_suggested_activities(self):
        activities = {
            "anxious": [
                "Take a nature walk",
                "Practice deep breathing",
                "Listen to calming music",
                "Do some gentle stretching",
                "Practice relaxation",
                "Practice breathing exercises"
            ],
            "stressed": [
                "Take a warm bath",
                "Practice progressive muscle relaxation",
                "Do some light exercise",
                "Listen to guided meditation",
                "Practice relaxation",
                "Practice breathing exercises"
            ],
            "sad": [
                "Connect with a friend",
                "Practice gratitude",
                "Do something creative",
                "Get some sunlight"
            ],
            "angry": [
                "Go for a run",
                "Write in a journal",
                "Practice deep breathing",
                "Listen to energetic music"
            ]
        }
        return activities.get(self.feeling, self.exercises.get("mood_tracking", {}).get("suggested_activities", []))

    def _get_journal_prompts(self):
        prompts = {
            "anxious": [
                "What triggered my anxiety today?",
                "What coping strategies worked for me?",
                "What am I looking forward to?",
                "What can I do to take care of myself?"
            ],
            "stressed": [
                "What are my main stressors right now?",
                "What would help me feel more relaxed?",
                "What boundaries do I need to set?",
                "What self-care activities can I do today?"
            ],
            "sad": [
                "What made me smile today?",
                "What am I grateful for?",
                "What would I like to do for myself?",
                "What positive changes can I make?"
            ],
            "angry": [
                "What triggered my anger?",
                "How can I express this emotion constructively?",
                "What boundaries do I need to set?",
                "What would help me feel calmer?"
            ]
        }
        return prompts.get(self.feeling, self.exercises.get("mood_tracking", {}).get("journal_prompts", []))
          