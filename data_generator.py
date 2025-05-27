import numpy as np
import pandas as pd
from typing import List, Dict
import random
from datetime import datetime, timedelta

class WorkoutDataGenerator:
    def __init__(self):
        # تعریف مقادیر پایه برای تولید داده
        self.workout_types = ['cardio', 'strength', 'flexibility', 'hiit', 'yoga']
        self.levels = ['beginner', 'intermediate', 'advanced']
        self.equipment = ['none', 'dumbbells', 'resistance_band', 'yoga_mat', 'full_gym']
        
    def generate_workout(self) -> Dict:
        """تولید یک تمرین ورزشی تصادفی"""
        workout_type = np.random.choice(self.workout_types)
        level = np.random.choice(self.levels)
        
        # تولید مدت زمان تمرین با توزیع نرمال
        duration = int(np.random.normal(45, 15))  # میانگین 45 دقیقه، انحراف معیار 15
        duration = max(20, min(120, duration))  # محدود کردن بین 20 تا 120 دقیقه
        
        # تولید کالری سوزانده شده بر اساس نوع و سطح تمرین
        base_calories = {
            'cardio': 300,
            'strength': 200,
            'flexibility': 150,
            'hiit': 400,
            'yoga': 180
        }
        
        level_multiplier = {
            'beginner': 0.8,
            'intermediate': 1.0,
            'advanced': 1.2
        }
        
        calories = int(base_calories[workout_type] * level_multiplier[level] * (duration/45))
        
        # تولید تجهیزات مورد نیاز
        num_equipment = np.random.binomial(len(self.equipment), 0.3)  # احتمال 30% برای هر تجهیزات
        equipment_needed = np.random.choice(self.equipment, num_equipment, replace=False).tolist()
        if not equipment_needed:
            equipment_needed = ['none']
            
        # تولید تمرینات
        exercises = self._generate_exercises(workout_type, level, duration)
        
        return {
            "id": f"w{random.randint(1000, 9999)}",
            "name": f"{workout_type.capitalize()} Workout - {level.capitalize()}",
            "type": workout_type,
            "level": level,
            "duration": duration,
            "calories_burn": calories,
            "equipment_needed": equipment_needed,
            "exercises": exercises,
            "tags": [workout_type, level] + equipment_needed,
            "benefits": self._generate_benefits(workout_type)
        }
    
    def _generate_exercises(self, workout_type: str, level: str, total_duration: int) -> List[Dict]:
        """تولید لیست تمرینات برای یک برنامه ورزشی"""
        exercises = []
        remaining_duration = total_duration
        
        # تعداد تمرینات بر اساس نوع و سطح
        num_exercises = {
            'beginner': np.random.randint(3, 5),
            'intermediate': np.random.randint(4, 6),
            'advanced': np.random.randint(5, 8)
        }[level]
        
        for i in range(num_exercises):
            if remaining_duration <= 0:
                break
                
            # توزیع مدت زمان تمرینات
            if i == num_exercises - 1:
                duration = remaining_duration
            else:
                duration = min(remaining_duration, int(np.random.normal(10, 3)))
                duration = max(5, duration)
            
            remaining_duration -= duration
            
            intensity = np.random.choice(['low', 'medium', 'high'], p=[0.3, 0.4, 0.3])
            
            exercises.append({
                "name": f"Exercise {i+1}",
                "duration": duration,
                "intensity": intensity,
                "description": f"{intensity.capitalize()} intensity exercise for {duration} minutes"
            })
        
        return exercises
    
    def _generate_benefits(self, workout_type: str) -> List[str]:
        """تولید مزایای تمرین بر اساس نوع آن"""
        all_benefits = {
            'cardio': ['افزایش استقامت', 'سوزاندن کالری', 'بهبود سلامت قلب', 'افزایش انرژی'],
            'strength': ['افزایش قدرت', 'ساخت عضله', 'بهبود متابولیسم', 'تقویت استخوان‌ها'],
            'flexibility': ['افزایش انعطاف‌پذیری', 'کاهش درد مفاصل', 'بهبود تعادل', 'کاهش استرس'],
            'hiit': ['سوزاندن چربی', 'افزایش متابولیسم', 'بهبود استقامت', 'صرفه‌جویی در زمان'],
            'yoga': ['کاهش استرس', 'بهبود تمرکز', 'افزایش انعطاف‌پذیری', 'تعادل ذهن و بدن']
        }
        
        num_benefits = np.random.randint(2, 4)
        return np.random.choice(all_benefits[workout_type], num_benefits, replace=False).tolist()
    
    def generate_dataset(self, size: int = 100) -> List[Dict]:
        """تولید مجموعه داده با اندازه مشخص"""
        return [self.generate_workout() for _ in range(size)]
    
    def generate_user_feedback(self, workout_id: str) -> Dict:
        """تولید بازخورد کاربر برای یک تمرین"""
        return {
            "workout_id": workout_id,
            "rating": np.random.randint(1, 6),  # امتیاز 1 تا 5
            "difficulty": np.random.choice(['too_easy', 'just_right', 'too_hard']),
            "completion_time": np.random.normal(45, 10),  # زمان تکمیل با توزیع نرمال
            "date": (datetime.now() - timedelta(days=np.random.randint(0, 30))).isoformat(),
            "comments": "Generated feedback for testing"
        }
    
    def generate_progress_data(self, workout_id: str) -> Dict:
        """تولید داده‌های پیشرفت برای یک تمرین"""
        return {
            "workout_id": workout_id,
            "calories_burned": np.random.normal(200, 50),  # کالری سوزانده شده
            "heart_rate_avg": np.random.normal(140, 20),  # ضربان قلب متوسط
            "duration": np.random.normal(45, 5),  # مدت زمان واقعی
            "date": (datetime.now() - timedelta(days=np.random.randint(0, 30))).isoformat()
        } 