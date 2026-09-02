"""
    Textract and S3 services
"""


from ..aws import get_client
from ..config import BUCKET_NAME
import uuid

def upload_to_s3(file_bytes: bytes, filename: str) -> None:
    """ uploads file to S3 bucket """

    name, extension = filename.rsplit(".", 1)

    new_filename = f"{name}-{uuid.uuid4().hex}.{extension}"

    get_client("s3").put_object(
        Bucket=BUCKET_NAME,
        Key=new_filename,
        Body=file_bytes
    )

def extract_document_text(doc_bytes: bytes) -> list[str]:
    """ use Textract to return the document's text"""

    response = get_client("textract").detect_document_text(Document={"Bytes": doc_bytes})

    return [block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"]