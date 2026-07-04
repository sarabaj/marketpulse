"""
Core analysis logic for MarketPulse.

Two layers, deliberately separated:
1. `rating_sentiment()` — a fast, offline sentiment label derived from the
   star rating. Works immediately with zero setup, zero API cost.
2. `extract_topics_ai()` — an optional, deeper layer that uses the Anthropic
   API to read a batch of review texts (Arabic or English) and extract the
   recurring themes/topics customers complain about or praise. This is the
   part that couldn't be done with simple rules — it needs language
   understanding.
"""
import json
import os
from collections import Counter

import pandas as pd


def rating_sentiment(rating: int) -> str:
    """Simple, transparent, offline sentiment bucket based on star rating."""
    if rating >= 4:
        return "positive"
    if rating == 3:
        return "neutral"
    return "negative"


def add_sentiment_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sentiment"] = df["rating"].apply(rating_sentiment)
    return df


TOPIC_PROMPT = """You will see a batch of customer reviews (in Arabic and/or English) for a
company. Identify the 4-6 most common THEMES mentioned across these reviews
(e.g. "slow customer support", "app crashes", "high fees", "great UI").

Return ONLY a JSON array of objects, no other text, in this exact shape:
[{{"topic": "short theme name in English", "mentions": <int count>, "example_sentiment": "positive|negative|mixed"}}]

Reviews:
{reviews}
"""


def extract_topics_ai(reviews: list[str]) -> list[dict]:
    """
    Uses Claude to extract recurring topics from a batch of reviews.
    Requires ANTHROPIC_API_KEY to be set. Falls back to an empty list
    (dashboard shows a friendly message) if the key is missing or the call fails.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return []

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        joined_reviews = "\n".join(f"- {r}" for r in reviews[:60])  # cap batch size

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            messages=[{"role": "user", "content": TOPIC_PROMPT.format(reviews=joined_reviews)}],
        )
        raw = message.content[0].text.strip().replace("```json", "").replace("```", "")
        return json.loads(raw)
    except Exception:
        return []


def top_keywords_offline(reviews: list[str], top_n: int = 10) -> list[tuple[str, int]]:
    """
    A zero-dependency, zero-API fallback: simple word-frequency count,
    useful when no API key is configured, and also as a sanity check
    against the AI topic extraction above.
    """
    stopwords = {
        "the", "and", "is", "to", "a", "of", "it", "i", "in", "for", "my",
        "من", "على", "إلى", "في", "هذا", "هذه", "و", "لا", "أن", "التطبيق",
    }
    counts = Counter()
    for text in reviews:
        for word in text.lower().replace(",", "").replace(".", "").split():
            if word not in stopwords and len(word) > 2:
                counts[word] += 1
    return counts.most_common(top_n)
