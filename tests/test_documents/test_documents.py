"""
Test suite for testing AWS Textract & S3
"""

from unittest.mock import patch
from complaint_system.documents.service import upload_to_s3, extract_document_text

def test_upload_to_s3():
    """ testing S3 upload """

    with patch("complaint_system.documents.service.get_client") as mock_get_client:

        mock_get_client.return_value.put_object.return_value = {}

        result = upload_to_s3(b"fake file contents", "test.jpg")

        assert result.startswith("attachments/")
        mock_get_client.return_value.put_object.assert_called_once()

def test_extract_document_text():
    """ testing Textract successfully extracts text """

    fake_response = {
        "Blocks": [
            {
                "BlockType": "PAGE"
            },
            {
                "BlockType": "LINE",
                "Text": "My bill is too high"
            }
        ]
    }

    with patch("complaint_system.documents.service.get_client") as mock_get_client:

        mock_get_client.return_value.detect_document_text.return_value = fake_response

        result = extract_document_text("attachments/test.jpg")

        assert result == ["My bill is too high"]