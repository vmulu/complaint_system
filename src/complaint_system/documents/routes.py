"""used to test s3 and textract connection"""


"""routes for api/vi/documents"""
from flask import Blueprint, request
from . import service
from .uploads import read_upload, MAX_IMAGE_BYTES, ALLOWED_EXTENSIONS

documents_bp = Blueprint("documents", __name__)

# each route that needs to take in a file can use these var name
UPLOAD_FIELD = 'file'

@documents_bp.post("/analyze")
def analyze_attachments():

    file = request.files.get(UPLOAD_FIELD)

    attachment, filename = read_upload(
        file,
        allowed_extensions=ALLOWED_EXTENSIONS,
        max_bytes=MAX_IMAGE_BYTES
    )

    service.upload_to_s3(attachment, filename)

    # passing in only the bytes
    results = service.extract_document_text(attachment)

    return results