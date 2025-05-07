import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

class SmartAI:
    def __init__(self, model_path="ai_model.pkl", training_data_path="TrainingData.json"):
        self.model_path = model_path
        self.training_data_path = training_data_path
        self.model = None
        self.vectorizer = CountVectorizer()
        self.encoder = LabelEncoder()
        self._load()

        def _load(self):
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)

            with open(self.training_data_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            texts = [item["goal"] + " " + item["feeling"] for item in data]
            suggestions = [item["suggestion"] for item in data]

            self.vectorizer.fit(texts)
            self.encoder.fit(suggestions)

        def predict(self, goal, feeling):
            input_text = goal + " " + feeling
            x = self.vectorizor.transform([input_text])
            pred_encoded = self.model.predict(x)
            suggestion = self.encoder.inverse_transform(pred_encoded)
            return suggestion[0]
          
        