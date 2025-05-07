class MindEngine:
    def __init__(self, feeling):
        self.feeling = feeling.lower()
        self.exercises = {
            "stressed": "Try a 10-minute guided meditation to calm yor mind.",
            "worried": "practice breathing: inhale 4s, hold 4s, exhale 4s, repeat for 5 mins.",
            "angry": "Try a grounding exercise: name 5 things you see, 4 you feel, 3 you hear.",
            "frustrated": "write down your feelings in a journal without filtering.",
            "happy": "Write a gratitude list of 5 things you're thankful for.",
            "greattful": "Take a mindful walk and focus on your senses and surroundings."
        }

    def get_exercise(self):
       if self.feeling in self.exercises:
           return self.exercises[self.feeling]
       else:
           return "Sorry, I misread your feeling!"
          