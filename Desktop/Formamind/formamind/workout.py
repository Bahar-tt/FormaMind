class WorkoutEngine:
        def __init__(self, goal):
            self.goal = goal.lower()
            self.plans = {
                  "tired": "Do light stretching or yoga for 15 minutes to recover.",
                  "low energy": "Try a short walk or gentle yoga to boost your energy.",
                  "energetic": "Do a HIIT session: 3 set of 5 exercise for 30 seconds each.",
                  "motivated": "Full-body strength training with dumbbells or bodyweight exercises",
                  "stressed": "20 minute relaxing yoga with focus on breath and posture.",
                  "anxious": "Try a slowpaced walk in nature or 10 minute yoga."
            }

        def get_plan(self):
              if self.goal in self.plans:
                    return self.plans[self.goal]
              else:
                    return "Sorry, No workout plan found for this goal!"

        
                    


    
            