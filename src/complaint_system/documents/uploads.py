"""shared validation for multipart file upload"""

from ..complaints.responses import DocumentUploadError
from werkzeug.datastructures import FileStorage

MAX_IMAGE_BYTES = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png", "pdf"}

def read_upload(file_storage : FileStorage | None,
                allowed_extensions : set[str],
                max_bytes : int) -> tuple[bytes, str]:

    """validate one uploaded file and return its bytes"""

    # validate that we received a file
    if file_storage is None or  not file_storage.filename:
        raise DocumentUploadError("validation_failed", 422, "no file uploaded - multi-part/form-data expected")

    # validate the file extension
    extension = file_storage.filename.rsplit(".", maxsplit=1)[-1].lower()
    if extension not in allowed_extensions:
        raise DocumentUploadError(
            "unsupported_media_type",
            415,
            f".{extension} is not supported. expected one of the following : {[e for e in allowed_extensions]}"
        )

    # reads in all the bytes from the file
    content = file_storage.read()

    # validate that the file is within the allowed num of bytes
    if len(content) > max_bytes:
        raise DocumentUploadError(
            "payload_too_large",
            413,
            f"file is {len(content)} bytes; max allowed is {max_bytes} bytes"
        )

    # validate the file actually has data
    if not content:
        raise DocumentUploadError("validation_failed", 422, "uploaded file is empty")

    return content, file_storage.filename