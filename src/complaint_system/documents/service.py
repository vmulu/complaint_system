"""
    Textract and S3 services
"""


from ..aws import get_client
from ..config import BUCKET_NAME
import uuid
import re

def upload_to_s3(file_bytes: bytes, filename: str) -> str:
    """ uploads file to S3 bucket """

    name, extension = filename.rsplit(".", 1)

    new_filename = f"{name}-{uuid.uuid4().hex}.{extension}"

    get_client("s3").put_object(
        Bucket=BUCKET_NAME,
        Key=new_filename,
        Body=file_bytes
    )

    return new_filename

def extract_document_text(s3_key: str) -> list[str]:
    """ use Textract to return the document's text thats stored in S3"""

    response = get_client("textract").detect_document_text(
        Document={
            "S3Object":
            {
                "Bucket": BUCKET_NAME,
                "Name": s3_key
            }
        }
    )

    return [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]

def find_account_number(document_text: list[str]) -> int | None:
    """ Finds the account number from Textract text. """

    text = " ".join(document_text)

    match = re.search(
        r"account\s*(?:number|#|no\.?)?\s*[:\-]?\s*(\d{5})",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None