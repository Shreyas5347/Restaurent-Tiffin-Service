import json
import sys
from pathlib import Path

# Ensure project root is in sys.path when script is executed directly
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from nlp.preprocessing.preprocess import preprocess_text


# Load training data
data_file = Path(__file__).resolve().parent.parent / "data" / "intents.json"
with open(data_file, "r", encoding="utf-8") as file:
    data = json.load(file)


texts = []
labels = []


# Extract examples and their intents
for intent in data["intents"]:
    for example in intent["examples"]:
        texts.append(example)
        labels.append(intent["intent"])


# Preprocess text
processed_texts = [
    " ".join(preprocess_text(text))
    for text in texts
]


# Convert text into numerical vectors
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(processed_texts)


# Create classifier
model = LogisticRegression()

# Train model
model.fit(X, labels)


def predict_intent(text):
    processed_text = " ".join(preprocess_text(text))

    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)

    return prediction[0]
    
if __name__ == "__main__":
    while True:
        message = input("Enter your message: ")

        if message.lower() == "exit":
            break

        intent = predict_intent(message)

        print("Intent:", intent)