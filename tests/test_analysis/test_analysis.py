"""
Test suite for testing AWS Comprehend PII detection
"""

import pytest
from unittest.mock import patch
from complaint_system.analysis.service import detect_pii, redact_pii, detect_sentiment, derive_priority


def test_detect_pii_success():
    """ testing if detect_pii works correctly"""

    fake_response = {
        "Entities": [
            {
                "Type": "SSN",
                "BeginOffset": 11,
                "EndOffset": 22
            }
        ]
    }

    with patch("complaint_system.analysis.service.get_client") as mock_get_client:

        mock_get_client.return_value.detect_pii_entities.return_value = fake_response

        result = detect_pii("My SSN is 123-45-6789")

    assert result == fake_response["Entities"]

    mock_get_client.return_value.detect_pii_entities.assert_called_once_with(
        Text="My SSN is 123-45-6789",
        LanguageCode="en"
    )

def test_redact_pii():
    """tests if redact_pii works correctly"""

    body = "My SSN is 123-45-6789"

    entities = [
        {
            "Type": "SSN",
            "BeginOffset": 10,
            "EndOffset": 21
        }
    ]

    result = redact_pii(body, entities)

    assert result == "My SSN is [REDACTED]"

def test_detect_sentiment_success():
    """ tests if detect_sentiment behaves correctly"""

    fake_response = {
        "Sentiment": "NEGATIVE",
        "SentimentScore": {
            "Positive": 0.01,
            "Negative": 0.95,
            "Neutral": 0.03,
            "Mixed": 0.01
        }
    }

    with patch("complaint_system.analysis.service.get_client") as mock_get_client:

        mock_get_client.return_value.detect_sentiment.return_value = fake_response

        result = detect_sentiment("I am extremely frustrated with my bill.")

    assert result == {
        "sentiment": "NEGATIVE",
        "scores": {
            "Positive": 0.01,
            "Negative": 0.95,
            "Neutral": 0.03,
            "Mixed": 0.01
        }
    }

    mock_get_client.return_value.detect_sentiment.assert_called_once_with(
        Text="I am extremely frustrated with my bill.",
        LanguageCode="en"
    )

@pytest.mark.parametrize(
    "sentiment_result, expected_priority",
    [
        (
            {
                "sentiment": "NEGATIVE",
                "scores": {"Negative": 0.90}
            },
            "high",
        ),
        (
            {
                "sentiment": "MIXED",
                "scores": {"Negative": 0.30}
            },
            "medium",
        ),
        (
            {
                "sentiment": "NEUTRAL",
                "scores": {"Negative": 0.10}
            },
            "low",
        ),
        (
            None,
            "needs_manual_review",
        ),
    ],
)

def test_derive_priority(sentiment_result, expected_priority):
    """parametrized tests for derive_priority"""

    with patch("complaint_system.analysis.service.detect_sentiment", return_value=sentiment_result,):
        result = derive_priority("test complaint")

    assert result == expected_priority