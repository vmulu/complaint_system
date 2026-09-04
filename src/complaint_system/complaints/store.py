"""

Logic for complaints

CRUD operations on data

"""
from complaint_system.models import Complaint, CreateComplaintDto, UpdateComplaintDto, Priority, Status, Channel
from pydantic import TypeAdapter
from sqlalchemy import select
from werkzeug.datastructures import FileStorage
from ..extensions import db
from ..db_models import CustomerComplaint, CustomerRecord
from ..analysis.service import redact_pii, detect_pii, derive_priority, detect_sentiment
from ..documents.service import extract_document_text, upload_to_s3, find_account_number
from ..documents.uploads import read_upload, ALLOWED_EXTENSIONS, MAX_IMAGE_BYTES
from .responses import DocumentAccountError, PIIDetectionError, NoPriorityOverrideReasonError

priorityAdaptor = TypeAdapter(Priority)
statusAdaptor = TypeAdapter(Status)
channelAdaptor = TypeAdapter(Channel)

SORT_ORDERS = {
    "priority": {
        "high": 1,
        "needs_manual_review": 2,
        "medium": 3,
        "low": 4
    },
    "status": {
        "new": 1,
        "in_progress": 2,
        "resolved": 3
    },
    "channel": {
        "email": 1,
        "web_form": 2,
        "mail": 3
    },
    "sentiment": {
        "negative": 1,
        "neutral": 2,
        "positive": 3
    }
}

def _sort_complaints(results : list[Complaint], sort_by : str) -> list[Complaint]:
    """sorts complaint list"""

    if sort_by not in SORT_ORDERS:
        return results

    order = SORT_ORDERS[sort_by]

    results.sort(key=lambda complaint: order[getattr(complaint, sort_by)])

    return results

def list_complaints() -> list[Complaint]:
    """
    Returns all Complaints
    """

    stmt = select(CustomerComplaint).order_by(CustomerComplaint.id)
    records = db.session.execute(stmt).scalars()

    return _sort_complaints([Complaint.model_validate(r) for r in records], sort_by="priority")

def list_complaints_by_query(*, customer_id : int | None = None,
                                priority : str | None = None,
                                status : str | None = None,
                                channel : str | None = None,
                                sentiment : str | None = None,
                                sort_by : str | None = None) -> list[Complaint]:
    """
    Filters support by customer, *sentiment*, derived priority, and status, sorted with the most urgent first.
    """

    stmt = select(CustomerComplaint)

    if customer_id is not None:
        stmt = stmt.where(CustomerComplaint.customer_id == customer_id)
    if priority is not None:
        valid_priority = priorityAdaptor.validate_python(priority)
        stmt = stmt.where(CustomerComplaint.priority == valid_priority)
    if status is not None:
        valid_status = statusAdaptor.validate_python(status)
        stmt = stmt.where(CustomerComplaint.status == valid_status)
    if channel is not None:
        valid_channel = channelAdaptor.validate_python(channel)
        stmt = stmt.where(CustomerComplaint.channel == valid_channel)
    if sentiment is not None:
        stmt = stmt.where(CustomerComplaint.sentiment == sentiment)

    records = db.session.execute(stmt).scalars()
    results = [Complaint.model_validate(r) for r in records]

    if sort_by:
        return _sort_complaints(results, sort_by)

    return results

def list_urgent_and_unresolved_complaints() ->list[Complaint]:

    urgent = list_complaints_by_query(sort_by="priority")

    return [c for c in urgent if c.status != "resolved"]

def create_complaint(complaint : dict, file: FileStorage | None = None) -> Complaint | None:
    """
    Creates a new Complaint object
    """

    document_text = None

    valid_complaint = CreateComplaintDto.model_validate(complaint)

    customer = db.session.execute(select(CustomerRecord).where(CustomerRecord.account_number == valid_complaint.customer_account_number)).scalar_one_or_none()
    if customer is None:
        return None

    pii_check = detect_pii(valid_complaint.body)

    if pii_check is None:
        raise PIIDetectionError(code="pii_detection_failed", status=503, detail="PII detection is currently unavailable.")
    redacted_body = redact_pii(valid_complaint.body, pii_check)
    contained_pii = len(pii_check) > 0

    check_sentiment = detect_sentiment(redacted_body)

    if check_sentiment is None:
        sentiment = None
        priority = "needs_manual_review"
    else:
        sentiment = check_sentiment["sentiment"].lower()
        priority = derive_priority(redacted_body)

    if file is not None:
        attachment, filename = read_upload(
            file,
            allowed_extensions=ALLOWED_EXTENSIONS,
            max_bytes=MAX_IMAGE_BYTES
        )

        s3_key = upload_to_s3(attachment, filename)

        document_text = extract_document_text(s3_key)

        if document_text is not None:
            document_account_number = find_account_number(document_text)

            document_text = "\n".join(document_text)
            pii_in_document = detect_pii(document_text) or []
            document_text = redact_pii(document_text, pii_in_document)

            if document_account_number is not None:
                if document_account_number != customer.account_number:
                    raise DocumentAccountError(code="document_account_mismatch", status=422, detail=f"The account number found in the document is: {document_account_number} \n This does not match the customer's account number: {customer.account_number}.")

    new_complaint = CustomerComplaint(
        customer_id=customer.id,            # type: ignore
        channel=valid_complaint.channel,    # type: ignore
        priority=priority,                  # type: ignore
        sentiment=sentiment,                # type: ignore
        subject=valid_complaint.subject,    # type: ignore
        body=redacted_body,                 # type: ignore
        contained_pii=contained_pii,        # type: ignore
        document_text=document_text         # type: ignore
    )

    db.session.add(new_complaint)
    db.session.commit()

    return Complaint.model_validate(new_complaint)

def update_complaint_status_and_priority(id : int, complaint : dict) -> Complaint | None:
    """
    Updating existing Complaint
    """

    valid_complaint = UpdateComplaintDto.model_validate(complaint)
    record = db.session.get(CustomerComplaint, id)

    if record is None:
        return None

    if valid_complaint.status is not None:
        record.status = valid_complaint.status
    if valid_complaint.priority is not None and valid_complaint.priority_override_reason is not None:
        record.priority = valid_complaint.priority
        record.priority_override_reason = valid_complaint.priority_override_reason
    if (valid_complaint.priority is not None and valid_complaint.priority_override_reason is None) or (valid_complaint.priority is None and valid_complaint.priority_override_reason is not None):
        raise NoPriorityOverrideReasonError(code="priority_override_reason_required", status=422, detail="A reason is required when manually overriding priority.")

    db.session.commit()

    return Complaint.model_validate(record)

def delete_complaint(id : int) -> bool:
    """
    Delete existing Complaint
    """

    record = db.session.get(CustomerComplaint, id)

    if record is None:
        return False

    db.session.delete(record)
    db.session.commit()

    return True