"""

"""

from flask import jsonify
from complaint_system.models import Customer


class NoCustomerFoundError(Exception):
    """
    Raised when client is looking for a Customer that cannot be found
    """

    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail

def list_envelope(customers: list[Customer]):
    """

    """
    return jsonify(count=len(customers), items=[row.model_dump() for row in customers])

def single_envelope(customer: Customer):
    """

    """
    return jsonify(customer.model_dump(mode="json"))