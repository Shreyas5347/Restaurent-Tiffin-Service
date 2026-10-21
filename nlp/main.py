import sys
from pathlib import Path

# Ensure project root is in sys.path so 'nlp' package is resolvable
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from nlp.intent_classifier.classifier import predict_intent
from nlp.sentiment_analysis.sentiment import analyze_sentiment
from nlp.entity_extraction.entities import extract_entities

# Temporary menu for testing.
# Later, we'll load menu items from your restaurant database.
MENU_ITEMS = [
    "paneer pizza",
    "margherita pizza",
    "chicken burger",
    "veg burger",
    "paneer tikka",
    "chicken biryani"
]


def process_message(message):

    # Step 1: Identify the user's intent
    intent, confidence = predict_intent(message)

    # Step 2: Extract entities from the message
    entities = extract_entities(
        message,
        MENU_ITEMS
    )

    # Step 3: Analyze sentiment
    sentiment = analyze_sentiment(message)

    # Step 4: Combine the results
    result = {
        "message": message,
        "intent": intent,
        "confidence": round(float(confidence), 3),
        "entities": entities,
        "sentiment": sentiment
    }

    return result


if __name__ == "__main__":

    print("Restaurant NLP Assistant")
    print("Type 'exit' to stop.\n")

    while True:

        message = input("You: ").strip()

        if message.lower() == "exit":
            break

        if not message:
            print("Please enter a message.\n")
            continue

        result = process_message(message)

        print("\nNLP Result:")

        for key, value in result.items():
            print(f"{key}: {value}")

        print()