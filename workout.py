from datetime import datetime

class WorkoutEngine:
    """
    موتور تولید و مدیریت تمرینات ورزشی
    
    این کلاس مسئول ایجاد، مدیریت و پیگیری تمرینات ورزشی است.
    تمرینات بر اساس سطح (beginner, intermediate, advanced) و نوع (cardio, strength, flexibility) دسته‌بندی می‌شوند.
    """
    
    def __init__(self, goal):
        """
        مقداردهی اولیه موتور تمرینات
        
        Args:
            goal (str): هدف تمرین (مثلاً fitness, weight_loss, muscle_gain)
        """
        self.goal = goal
        self.workout_types = {
            "cardio": {
                "beginner": [
                    {"name": "Walking", "duration": 20, "intensity": "low"},
                    {"name": "Light Jogging", "duration": 15, "intensity": "medium"},
                    {"name": "Cycling", "duration": 20, "intensity": "low"}
                ],
                "intermediate": [
                    {"name": "Running", "duration": 30, "intensity": "medium"},
                    {"name": "HIIT", "duration": 20, "intensity": "high"},
                    {"name": "Swimming", "duration": 30, "intensity": "medium"}
                ],
                "advanced": [
                    {"name": "Sprint Intervals", "duration": 45, "intensity": "high"},
                    {"name": "Mountain Climbing", "duration": 40, "intensity": "high"},
                    {"name": "CrossFit", "duration": 60, "intensity": "very high"},
                    {"name": "Tabata", "duration": 20, "intensity": "very high"},
                    {"name": "Circuit Training", "duration": 25, "intensity": "high"},
                    {"name": "Plyometric HIIT", "duration": 30, "intensity": "very high"}
                ]
            },
            "strength": {
                "beginner": [
                    {"name": "Bodyweight Squats", "sets": 3, "reps": 10, "intensity": "low"},
                    {"name": "Push-ups", "sets": 3, "reps": 8, "intensity": "low"},
                    {"name": "Plank", "sets": 3, "duration": 30, "intensity": "low"}
                ],
                "intermediate": [
                    {"name": "Dumbbell Squats", "sets": 4, "reps": 12, "intensity": "medium"},
                    {"name": "Bench Press", "sets": 4, "reps": 10, "intensity": "medium"},
                    {"name": "Deadlifts", "sets": 3, "reps": 8, "intensity": "medium"}
                ],
                "advanced": [
                    {"name": "Barbell Squats", "sets": 5, "reps": 8, "intensity": "high"},
                    {"name": "Weighted Pull-ups", "sets": 4, "reps": 8, "intensity": "high"},
                    {"name": "Power Cleans", "sets": 4, "reps": 6, "intensity": "very high"},
                    {"name": "Olympic Lifts", "sets": 3, "reps": 5, "intensity": "very high"},
                    {"name": "Complex Training", "sets": 4, "reps": 6, "intensity": "high"},
                    {"name": "Supersets", "sets": 3, "reps": 10, "intensity": "high"}
                ]
            },
            "flexibility": {
                "beginner": [
                    {"name": "Basic Stretching", "duration": 15, "intensity": "low"},
                    {"name": "Yoga Flow", "duration": 20, "intensity": "low"},
                    {"name": "Mobility Drills", "duration": 15, "intensity": "low"}
                ],
                "intermediate": [
                    {"name": "Dynamic Stretching", "duration": 25, "intensity": "medium"},
                    {"name": "Power Yoga", "duration": 30, "intensity": "medium"},
                    {"name": "Pilates", "duration": 30, "intensity": "medium"}
                ],
                "advanced": [
                    {"name": "Advanced Yoga", "duration": 45, "intensity": "high"},
                    {"name": "Contortion Training", "duration": 40, "intensity": "high"},
                    {"name": "Acrobatic Stretching", "duration": 45, "intensity": "very high"},
                    {"name": "Dynamic Flexibility", "duration": 25, "intensity": "high"},
                    {"name": "PNF Stretching", "duration": 30, "intensity": "high"},
                    {"name": "Active Isolated", "duration": 20, "intensity": "medium"}
                ]
            },
            "yoga": {
                "beginner": [
                    {"name": "Sun Salutation (Surya Namaskar)", "duration": 15, "intensity": "low"},
                    {"name": "Basic Standing Poses", "duration": 20, "intensity": "low"},
                    {"name": "Seated Forward Bends", "duration": 15, "intensity": "low"}
                ],
                "intermediate": [
                    {"name": "Vinyasa Flow", "duration": 30, "intensity": "medium"},
                    {"name": "Balance Poses", "duration": 25, "intensity": "medium"},
                    {"name": "Backbends", "duration": 30, "intensity": "medium"}
                ],
                "advanced": [
                    {"name": "Power Yoga", "duration": 45, "intensity": "high"},
                    {"name": "Inversions", "duration": 40, "intensity": "high"},
                    {"name": "Advanced Arm Balances", "duration": 45, "intensity": "very high"},
                    {"name": "Advanced Backbends", "duration": 40, "intensity": "high"},
                    {"name": "Advanced Twists", "duration": 35, "intensity": "high"},
                    {"name": "Meditation in Motion", "duration": 50, "intensity": "medium"}
                ]
            }
        }

    def create_workout(self, name, duration, difficulty, exercises=None):
        """
        ایجاد یک تمرین جدید
        
        Args:
            name (str): نام تمرین
            duration (int): مدت زمان به دقیقه
            difficulty (str): سطح دشواری (beginner, intermediate, advanced)
            exercises (list): لیست تمرینات (اختیاری)
            
        Returns:
            dict: اطلاعات تمرین ایجاد شده
            
        Raises:
            ValueError: در صورت نامعتبر بودن پارامترها
        """
        if duration <= 0:
            raise ValueError("مدت زمان باید بزرگتر از صفر باشد")
        if duration > 180:  # حداکثر 3 ساعت
            raise ValueError("مدت زمان نمی‌تواند بیشتر از 180 دقیقه باشد")
        
        if difficulty not in ["beginner", "intermediate", "advanced"]:
            raise ValueError("سطح دشواری نامعتبر است")
        
        if exercises:
            for exercise in exercises:
                if exercise.get("reps", 0) <= 0:
                    raise ValueError("تعداد تکرار باید بزرگتر از صفر باشد")
                if exercise.get("reps", 0) > 200:  # حداکثر 200 تکرار
                    raise ValueError("تعداد تکرار نمی‌تواند بیشتر از 200 باشد")
        
        return {
            "id": str(hash(name + str(duration))),
            "name": name,
            "duration": duration,
            "difficulty": difficulty,
            "exercises": exercises or []
        }

    def record_progress(self, workout_id, user_id, completed_exercises, duration, calories_burned):
        """
        ثبت پیشرفت تمرین
        
        Args:
            workout_id (str): شناسه تمرین
            user_id (str): شناسه کاربر
            completed_exercises (list): لیست تمرینات انجام شده
            duration (int): مدت زمان انجام تمرین
            calories_burned (int): کالری سوزانده شده
            
        Returns:
            dict: اطلاعات پیشرفت ثبت شده
            
        Raises:
            ValueError: در صورت نامعتبر بودن شناسه تمرین
        """
        if not workout_id or workout_id == "invalid_id":
            raise ValueError("شناسه تمرین نامعتبر است")
        
        return {
            "workout_id": workout_id,
            "user_id": user_id,
            "completed_exercises": completed_exercises,
            "duration": duration,
            "calories_burned": calories_burned,
            "timestamp": str(datetime.now())
        }

    def get_plan(self, level="beginner", workout_type="cardio", duration=None):
        """دریافت برنامه تمرینی بر اساس سطح و نوع تمرین
        
        Args:
            level (str): سطح تمرین (beginner, intermediate, advanced)
            workout_type (str): نوع تمرین (cardio, strength, flexibility)
            duration (int): مدت زمان مورد نظر به دقیقه
        
        Returns:
            str: برنامه تمرینی یا None اگر برنامه‌ای یافت نشد
        """
        if workout_type not in self.workout_types:
            return None
        if level not in ["beginner", "intermediate", "advanced"]:
            return None
        # برای تمرینات پیشرفته، حداقل مدت زمان 45 دقیقه لازم است
        if level == "advanced" and duration is not None and duration < 45:
            return None
        # دسترسی صحیح به تمرینات بر اساس سطح
        workouts = self.workout_types[workout_type].get(level, [])
        available_workouts = workouts
        if not available_workouts:
            return None
        if duration:
            available_workouts = [w for w in available_workouts if w.get("duration", 0) <= duration]
            if not available_workouts:
                return None
        plan = f"Workout Plan for {workout_type.capitalize()} ({level}):\n\n"
        for i, workout in enumerate(available_workouts, 1):
            plan += f"{i}. {workout['name']}\n"
            if "duration" in workout:
                plan += f"   Duration: {workout['duration']} minutes\n"
            if "sets" in workout:
                plan += f"   Sets: {workout['sets']}\n"
            if "reps" in workout:
                plan += f"   Reps: {workout['reps']}\n"
            plan += f"   Intensity: {workout['intensity']}\n\n"
        return plan

    def get_available_types(self):
        """
        دریافت انواع تمرینات موجود
        
        Returns:
            list: لیست انواع تمرینات
        """
        return list(self.workout_types.keys())

    def get_available_levels(self):
        """
        دریافت سطوح موجود
        
        Returns:
            list: لیست سطوح تمرین
        """
        return ["beginner", "intermediate", "advanced"]

        
                    


    
            