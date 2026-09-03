"""

API endpoints for complaints

"""

from flask import Blueprint, request, jsonify
from .responses import list_envelope, single_envelope, NoComplaintFoundError, DocumentUploadError
from ..responses import NoCustomerFoundError
from . import store

complaints_bp = Blueprint("complaints", __name__)

# GET /api/v1/complaints
@complaints_bp.get("")
def get_complaints():
    """
    Get all Complaints or by query
    """

    customer_id = request.args.get("customer_id", type=int)
    priority = request.args.get("priority")
    status = request.args.get("status")
    channel = request.args.get("channel")
    sentiment = request.args.get("sentiment")
    sort_by = request.args.get("sort_by")

    if customer_id or priority or status or channel:
        return list_envelope(store.list_complaints_by_query(customer_id=customer_id,
                                                            priority=priority,
                                                            status=status,
                                                            channel=channel,
                                                            sentiment=sentiment,
                                                            sort_by=sort_by))

    return list_envelope(store.list_complaints())

# GET /api/v1/complaints/urgent
@complaints_bp.get("/urgent")
def get_urgent_complaints():
    """urgent endpoint that lists all unresolved urgent complaints"""

    return list_envelope(store.list_urgent_and_unresolved_complaints())

# POST /api/v1/complaints
@complaints_bp.post("")
def create_complaint():
    """
    Create new Complaint endpoint
    """

    if request.content_type.startswith("multipart/form-data"):
        file = request.files.get("file")

        body = {
            "body": request.form.get("body"),
            "channel": request.form.get("channel"),
            "customer_account_number": request.form.get("customer_account_number"),
            "subject": request.form.get("subject")
        }
    else:
        file = None
        body = request.get_json(silent=True) or {}

    new_complaint = store.create_complaint(body, file)

    if new_complaint is None:
        raise NoCustomerFoundError(code="customer_not_found", status=404, detail=f"Customer with account number {body["customer_account_number"]} was not found")

    return single_envelope(new_complaint)

# PUT /api/v1/complaints/<complaint_id>
@complaints_bp.put("/<int:complaint_id>")
def update_complaint(complaint_id : int):
    """
    Update Complaint endpoint
    """

    body = request.get_json(silent=True) or {}

    complaint = store.update_complaint_status_and_priority(complaint_id, body)

    if complaint is None:
        raise NoComplaintFoundError(code="no_complaint_found", status=404, detail=f"Complaint with id {complaint_id} was not found")

    return single_envelope(complaint)

# DELETE /api/v1/complaints/<complaint_id>
@complaints_bp.delete("/<int:complaint_id>")
def delete_complaint(complaint_id : int):
    """
    Delete Complaint endpoint
    """

    success = store.delete_complaint(complaint_id)

    if success:
        return jsonify(status="deleted"), 204
    raise NoComplaintFoundError(code="no_complaint_found", status=404, detail=f"Complaint with id {complaint_id} was not found")