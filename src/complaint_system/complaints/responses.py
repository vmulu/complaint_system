"""

"""

from flask import jsonify
from complaint_system.models import Complaint

def list_envelope(customers: list[Complaint]):
    """

    """
    return jsonify(count=len(customers), items=[row.model_dump() for row in customers])

def single_envelope(customer: Complaint):
    """

    """
    return jsonify(customer.model_dump(mode="json"))