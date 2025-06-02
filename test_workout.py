from workout import WorkoutEngine

def main():
    # Create a workout engine instance
    engine = WorkoutEngine(goal="fitness")
    
    # Test getting available types
    print("Available workout types:", engine.get_available_types())
    print("\n" + "="*50 + "\n")
    
    # Test getting a cardio workout plan
    cardio_plan = engine.get_plan(level="intermediate", workout_type="cardio", duration=30)
    print("Cardio Workout Plan:")
    print(cardio_plan)
    print("\n" + "="*50 + "\n")
    
    # Test getting a strength workout plan
    strength_plan = engine.get_plan(level="beginner", workout_type="strength")
    print("Strength Workout Plan:")
    print(strength_plan)
    print("\n" + "="*50 + "\n")
    
    # Test creating a custom workout
    custom_workout = engine.create_workout(
        name="Custom HIIT",
        duration=45,
        difficulty="intermediate",
        exercises=[
            {"name": "Jumping Jacks", "reps": 20, "sets": 3},
            {"name": "Push-ups", "reps": 15, "sets": 3},
            {"name": "Squats", "reps": 25, "sets": 3}
        ]
    )
    print("Custom Workout Created:")
    print(custom_workout)
    print("\n" + "="*50 + "\n")
    
    # Test recording progress
    progress = engine.record_progress(
        workout_id=custom_workout["id"],
        user_id="user123",
        completed_exercises=custom_workout["exercises"],
        duration=40,
        calories_burned=350
    )
    print("Workout Progress Recorded:")
    print(progress)

if __name__ == "__main__":
    main() 