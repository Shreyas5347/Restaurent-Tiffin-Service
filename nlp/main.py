from nlp.intent_classifier.classifier import predict_intent
from nlp.sentiment_analysis.sentiment import analyze_sentiment


message = input("Enter your message: ")

intent = predict_intent(message)
sentiment = analyze_sentiment(message)

print("Intent:", intent)
print("Sentiment:", sentiment)