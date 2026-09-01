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