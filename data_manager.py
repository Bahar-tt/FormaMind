import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any

class DataManager:
    def __init__(self, data_path: str = "data/workout_data.json"):
        self.data_path = Path(data_path)
        self.data = self._load_data()
        
    def _load_data(self) -> Dict:
        """بارگذاری داده‌ها از فایل JSON"""
        if not self.data_path.exists():
            return {"workouts": [], "user_feedback": [], "workout_progress": []}
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_data(self) -> None:
        """ذخیره داده‌ها در فایل JSON"""
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
    
    def add_workout(self, workout: Dict) -> None:
        """اضافه کردن یک تمرین جدید"""
        self.data["workouts"].append(workout)
        self.save_data()
    
    def add_user_feedback(self, feedback: Dict) -> None:
        """اضافه کردن بازخورد کاربر"""
        self.data["user_feedback"].append(feedback)
        self.save_data()
    
    def add_workout_progress(self, progress: Dict) -> None:
        """ثبت پیشرفت تمرین"""
        self.data["workout_progress"].append(progress)
        self.save_data()
    
    def get_workouts_df(self) -> pd.DataFrame:
        """تبدیل داده‌های تمرینات به DataFrame"""
        return pd.DataFrame(self.data["workouts"])
    
    def get_user_feedback_df(self) -> pd.DataFrame:
        """تبدیل بازخوردهای کاربر به DataFrame"""
        return pd.DataFrame(self.data["user_feedback"])
    
    def get_workout_progress_df(self) -> pd.DataFrame:
        """تبدیل داده‌های پیشرفت به DataFrame"""
        return pd.DataFrame(self.data["workout_progress"])
    
    def prepare_training_data(self) -> pd.DataFrame:
        """آماده‌سازی داده‌ها برای یادگیری ماشین"""
        workouts_df = self.get_workouts_df()
        feedback_df = self.get_user_feedback_df()
        progress_df = self.get_workout_progress_df()
        
        # اینجا می‌توانیم داده‌ها را برای یادگیری ماشین آماده کنیم
        # مثلاً ترکیب داده‌ها، نرمال‌سازی، و غیره
        return workouts_df 