"""
    calling AWS Comprehend
       - PII Detection & Redaction
       - Sentiment Analysis
"""

from ..aws import get_client

def detect_pii(body : str) -> list[dict] | None:
    """detects pii in complaint body using AWS Comprehend """

    try:

        response = get_client("comprehend").detect_pii_entities(
            Text=body,
            LanguageCode="en"
        )

        return response["Entities"]
    except Exception:
        return None

def redact_pii(body : str, entities : list[dict]) -> str:
    """redacts pii info from body of complaint"""

    redacted = body

    for entity in reversed(entities):
        start = entity["BeginOffset"]
        end = entity["EndOffset"]

        redacted = (redacted[:start]+ "[REDACTED]"+ redacted[end:])

    return redacted

def detect_sentiment(body: str) -> dict | None:
    """ use AWS comprehend to determine overall tone of text"""

    try:
        response = get_client("comprehend").detect_sentiment(
            Text=body,
            LanguageCode="en"
        )

        return {
            "sentiment" : response["Sentiment"],
            "scores" : {k : round(v, 3) for k, v in response["SentimentScore"].items()}
        }
    except Exception:
        return None

def derive_priority(body : str):
    """use the determined sentiment to decide ticket priority level"""
    result = detect_sentiment(body)

    if result is None:
        return "needs_manual_review"

    if result["sentiment"] == "NEGATIVE" and result["scores"]["Negative"] > 0.7:
        return "high"

    if result["sentiment"] == "MIXED":
        return "medium"

    return "low"
