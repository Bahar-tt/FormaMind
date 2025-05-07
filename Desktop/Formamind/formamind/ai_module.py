def smart_suggest(goal, feeling):
    goal = goal.lower()
    feeling = feeling.lower()

    if goal == "body":
        if feeling in ["tired", "low energy"]:
            return "Try a light stretching or recovery session."
        elif feeling in ["stressed", "anxious"]:
            return "A calming Yoga session can help you relax."
        elif feeling in ["energetic", "motivated"]:
            return "How about a high-intensity cardio or strength workout?"
        
    elif goal == "emotion":
        if feeling in ["sressed", "worried"]:
            return "Try a guided meditation focused on relaxation."
        elif feeling in ["angry", "frustrated"]:
            return "A breathing exercise can help you center yourself."
        elif feeling in ["happy", "greatful"]:
            return "Maybe write in a gratitude journal or do a mindful walk."
    return "No specific suggestion found. Please choose your own plan."
        