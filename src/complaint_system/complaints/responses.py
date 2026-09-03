"""

"""

from flask import jsonify
from complaint_system.models import Complaint

class DocumentAccountError(Exception):
    """Raised when a customer account number already exists."""
    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

class PIIDetectionError(Exception):
    """Raised when PII Detection Fails."""
    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

class DocumentUploadError(Exception):
    """
    Raised when a document is upload has an issue
    """

    def __init__(self, code: str, status: int, detail: str | None = None):

        # Flask expects specific values for "code"
        #   ex: "not_found" "internal" "validation_failed"

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail


class NoComplaintFoundError(Exception):
    """
    Raised when client is looking for a Complaint that cannot be found
    """

    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def list_envelope(customers: list[Complaint]):
    """

    """
    return jsonify(count=len(customers), items=[row.model_dump() for row in customers])

def single_envelope(customer: Complaint):
    """

    """
    return jsonify(customer.model_dump(mode="json"))