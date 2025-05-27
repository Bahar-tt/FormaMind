from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from typing import Dict, Any

class WorkoutLevelPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        
    def _prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """آماده‌سازی ویژگی‌ها برای مدل"""
        # کپی داده‌ها برای جلوگیری از تغییر داده‌های اصلی
        df = data.copy()
        
        # تبدیل متغیرهای کیفی به عددی
        categorical_columns = ['type', 'equipment_needed']
        for col in categorical_columns:
            if col in df.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col])
                else:
                    df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def train(self, data: pd.DataFrame) -> None:
        """آموزش مدل"""
        # آماده‌سازی داده‌ها
        X = self._prepare_features(data)
        y = data['level']
        
        # آموزش مدل
        self.model.fit(X, y)
    
    def predict(self, features: Dict[str, Any]) -> str:
        """پیش‌بینی سطح مناسب تمرین"""
        # تبدیل ویژگی‌ها به DataFrame
        df = pd.DataFrame([features])
        
        # آماده‌سازی ویژگی‌ها
        X = self._prepare_features(df)
        
        # پیش‌بینی
        prediction = self.model.predict(X)[0]
        
        return prediction
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
        """ارزیابی مدل"""
        X_test_prepared = self._prepare_features(X_test)
        score = self.model.score(X_test_prepared, y_test)
        
        return {
            'accuracy': score
        } 