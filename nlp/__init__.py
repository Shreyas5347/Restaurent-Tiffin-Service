import sys
from pathlib import Path

# Add project root to sys.path so imports work from anywhere
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from nlp.intent_classifier import predict_intent
from nlp.sentiment_analysis import analyze_sentiment
from nlp.entity_extraction import extract_entities

__all__ = [
    "predict_intent",
    "analyze_sentiment",
    "extract_entities",
]
