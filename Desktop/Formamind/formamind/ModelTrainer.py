import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import joblib

with open("TrainingData.json", "r", encoding="utf-8") as file:
    data = json.load(file)

X_text = [f"{item['goal']}{item['feeling']}" for item in data]
Y_text = [item['suggestion'] for item in data]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_text)

label_encoder = LabelEncoder()
Y = label_encoder.fit_transform(Y_text)

model = DecisionTreeClassifier()
model.fit(X, Y)

joblib.dump(model, "ai_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("Model trained and saved successfully.")
 