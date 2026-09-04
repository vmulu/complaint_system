"""
Error responses for Complaint entities
"""

from flask import jsonify
from complaint_system.models import Complaint

class DeleteConfirmationRequiredError(Exception):
    """Raised when delete confirmation is no given."""
    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

class NoPriorityOverrideReasonError(Exception):
    """Raised when no reason for priority change given."""
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

class DocumentAccountError(Exception):
    """Raised when a customer account number already exists."""
    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

class DocumentUploadError(Exception):
    """ Raised when a document is upload has an issue """

    def __init__(self, code: str, status: int, detail: str | None = None):

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail


class NoComplaintFoundError(Exception):
    """ Raised when client is looking for a Complaint that cannot be found """

    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def list_envelope(customers: list[Complaint]):
    """ formats API response for list of entities """
    return jsonify(count=len(customers), items=[row.model_dump() for row in customers])

def single_envelope(customer: Complaint):
    """ formats API response for single entity """
    return jsonify(customer.model_dump(mode="json"))