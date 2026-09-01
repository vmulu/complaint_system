"""used to test aws services"""

from flask import Blueprint, request
from complaint_system.analysis.service import detect_pii, redact_pii

analysis_bp = Blueprint("analysis", __name__)


@analysis_bp.post("/pii")
def check_pii():
    data = request.get_json()

    body = data.get("body")

    if not body:
        return {"error": "body is required"}, 400

    result = detect_pii(body)

    if result is None:
        return {"no_pii_found": body}, 400

    return redact_pii(body, result), 200 # type: ignore

