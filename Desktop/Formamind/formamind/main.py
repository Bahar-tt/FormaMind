from workout import WorkoutEngine
from mind import MindEngine
from SmartAI import SmartAI
from translator import translate
from memory import MemoryManager
from UserLog import UserLog


print("Choose your language / زبان خود را انتخاب کنید:")
print("1. English")
print("2. فارسی")
language_input = input("Enter 1 or 2: ")
lang = "fa" if language_input == "2" else "en"

memory = MemoryManager()
logger = UserLog()
ai = SmartAI()

goal = input(translate("Do you want a plan for your Body or Emotion? ", lang)).lower()
feeling = input(translate("How are you feeling today? ", lang)).lower()

memory.save("goal", goal)
memory.save("feeling", feeling)

suggestion = ai.smart_suggest(goal, feeling)
print("\n" + translate("Your smart suggestion:", lang))
print(translate(suggestion, lang))

confirm = input(translate("Do you want to continue with this suggestion? (yes/no) ", lang)).lower()

logger.log_interaction(lang, goal, feeling, suggestion, confirm)

if goal == "body":
    workout = WorkoutEngine(goal)
    plan = workout.get_plan()
    if plan:
        print("\n" + translate("Here is your workout plan:", lang))
        print(translate(plan, lang))
    else:
        print(translate("No workout plan found for this goal.", lang))

elif goal == "emotion":
    mind = MindEngine(feeling)
    exercise = mind.get_exercise()
    if exercise:
        print("\n" + translate("Here is your mental exercise:", lang))
        print(translate(exercise, lang))
    else:
        print(translate("No mental exercise found for this feeling.", lang))

else:
    print(translate("Please enter only 'Body' or 'Emotion'.", lang))
