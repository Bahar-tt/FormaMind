from sklearn.tree import DecisionTreeClassifier
import json
import pickle
from sklearn.feature_extraction.text import  CountVectorizer
from sklearn.preprocessing import LabelEncoder

with open("TrainingData.json", "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["goal"] + " " + item["feeling"] for item in data]
suggestions = [item["suggestion"] for item in data]

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(texts)

encoder = LabelEncoder()
y = encoder.fit_transform(suggestions)

model = DecisionTreeClassifier()
model.fit(x, y)

with open("ai_model.pkl", "wb") as f:
    pickle.dump(model, f)

    