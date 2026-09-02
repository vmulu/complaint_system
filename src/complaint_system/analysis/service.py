"""
    calling AWS Comprehend with boto3
       - PII Detection & Redaction
       - Sentiment Analysis
"""

import json
from ..aws import get_client

def detect_pii(body : str) -> list[dict]:
    """detects pii in complaint body using AWS Comprehend """

    response = get_client("comprehend").detect_pii_entities(
        Text=body,
        LanguageCode="en"
    )

    return response["Entities"]

def redact_pii(body : str, entities : list[dict]) -> str:
    """redacts pii info from body of complaint"""

    redacted = body

    for entity in reversed(entities):
        start = entity["BeginOffset"]
        end = entity["EndOffset"]

        redacted = (redacted[:start]+ "[REDACTED]"+ redacted[end:])

    return redacted

def detect_sentiment(body: str) -> dict:
    """ use AWS comprehend to determine overall tone of text"""

    response = get_client("comprehend").detect_sentiment(
        Text=body,
        LanguageCode="en"
    )

    return {
        "sentiment" : response["Sentiment"],
        "scores" : {k : round(v, 3) for k, v in response["SentimentScore"].items()}
    }

def derive_priority(body : str):
    """use the determined sentiment to decide ticket priority level"""
    result = detect_sentiment(body)

    if result["sentiment"] == "NEGATIVE" and result["scores"]["Negative"] > 0.7:
        return "high"

    if result["sentiment"] == "MIXED":
        return "medium"

    return "low"
