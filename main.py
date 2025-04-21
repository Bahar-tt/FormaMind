
from formamind.translator import translate
from formamind.workout import WorkoutEngine
from formamind.mind import MindEngine
from formamind.ai_module import smart_suggest
from formamind.UserLog import UserLog
from formamind.memory import MemoryManager
from formamind.LogAnalyzer import LogAnalyzer


print("Choose your language / زبان مورد نظر را انتخاب کنید:")
print("1. English")
print("2. فارسی")
language = input("Enter 1 or 2: ")

lang = "fa" if language == "2" else "en"

memory = MemoryManager()
logger = UserLog()
analyzer = LogAnalyzer()

print(translate("Hello! Welcome to FormaMind!"))
goal = input(translate("Choose one: body / emotion\n", lang)).strip().lower()
feeling = input(translate("How are you feeling today?", lang)).strip().lower()

memory.save("goal", goal)
memory.save("feeling", feeling)

print("\n" + translate("Your smart suggestion:", lang))
suggestion = smart_suggest(goal, feeling)
print(translate(suggestion, lang))


confirm = input(translate("Do you want to continue with this suggestion? (yes/no)", lang)).strip().lower()
logger.log_interaction(language=lang, goal=goal, feeling=feeling, suggestion=suggestion, confirmed=confirm)

if goal == "body":
    workout = WorkoutEngine(goal)
    plan = workout.get_plan()
    if plan:
        print("\n" + translate("Here is your workout plan: ", lang))
        print(translate(plan, lang))
    else:
        print(translate("No workout plan found for this goal!", lang))

elif goal == "emotion":
    mind = MindEngine(feeling)
    exercise = mind.get_exercise()
    if exercise:
        print("\n" + translate("Her is your mental exercise: ", lang))
        print(translate(exercise, lang))
    else:
        print(translate("No mental exercise found for this feeling!", lang))

else:
    print(translate("Please enter only 'body' or 'emotion'.", lang))

print("\n" + translate("Here is your usage summary so far: ", lang))
summary = analyzer.summarize_logs()
print(translate(summary, lang))

   

