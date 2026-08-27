import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Add local nltk_data folder to nltk's search path
local_nltk_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "nltk_data")
)
nltk.data.path.append(local_nltk_path)

analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):

    scores = analyzer.polarity_scores(text)

    compound_score = scores["compound"]

    if compound_score >= 0.05:
        return "POSITIVE"

    elif compound_score <= -0.05:
        return "NEGATIVE"

    else:
        return "NEUTRAL"


if __name__ == "__main__":

    while True:

        message = input("Enter your message: ")

        if message.lower() == "exit":
            break

        sentiment = analyze_sentiment(message)

        print("Sentiment:", sentiment)