import json
import sys
from pathlib import Path

# Add project root to sys.path so 'nlp.*' packages can be imported when running directly
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt

from nlp.intent_classifier.classifier import predict_intent


# Load test data
DATA_PATH = Path(__file__).resolve().parent / "data" / "test_data.json"
with open(DATA_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)


actual_labels = []
predicted_labels = []


# Run predictions
for case in data["test_cases"]:

    text = case["text"]
    actual_intent = case["intent"]

    predicted_intent, confidence = predict_intent(text)

    actual_labels.append(actual_intent)
    predicted_labels.append(predicted_intent)

    print(f"\nMessage: {text}")
    print(f"Actual intent: {actual_intent}")
    print(f"Predicted intent: {predicted_intent}")
    print(f"Confidence: {confidence:.2f}")


# Calculate accuracy
accuracy = accuracy_score(
    actual_labels,
    predicted_labels
)

print("\n========== EVALUATION RESULTS ==========")

print(f"\nAccuracy: {accuracy:.2%}")


# Calculate precision, recall and F1-score
print("\nClassification Report:")

print(
    classification_report(
        actual_labels,
        predicted_labels,
        zero_division=0
    )
)


# Generate confusion matrix
labels = sorted(set(actual_labels) | set(predicted_labels))

matrix = confusion_matrix(
    actual_labels,
    predicted_labels,
    labels=labels
)

print("\nConfusion Matrix:")
print(matrix)


# Display confusion matrix
display = ConfusionMatrixDisplay(
    confusion_matrix=matrix,
    display_labels=labels
)

display.plot(
    xticks_rotation=45,
    values_format="d"
)

plt.tight_layout()
plt.show()