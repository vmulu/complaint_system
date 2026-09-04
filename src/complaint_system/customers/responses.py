"""
Error responses for Customer entities
"""

from flask import jsonify
from complaint_system.models import Customer, SendCustomer

class DuplicateAccountNumberError(Exception):
    """Raised when a customer account number already exists."""
    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def list_envelope(customers: list[Customer] | list[SendCustomer]):
    """ formats API response for list of entities """
    return jsonify(count=len(customers), items=[row.model_dump() for row in customers])

def single_envelope(customer: Customer | SendCustomer):
    """ formats API response for single entities """
    return jsonify(customer.model_dump(mode="json"))