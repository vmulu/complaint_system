"""

Logic for complaints

CRUD operations on data

"""
from complaint_system.models import Complaint, CreateComplaintDto, UpdateComplaintDto, Priority, Status, Channel
from pydantic import TypeAdapter
from sqlalchemy import select
from complaint_system.extensions import db
from complaint_system.db_models import CustomerComplaint, CustomerRecord
from ..analysis.service import redact_pii, detect_pii, derive_priority, detect_sentiment

priorityAdaptor = TypeAdapter(Priority)
statusAdaptor = TypeAdapter(Status)
channelAdaptor = TypeAdapter(Channel)

SORT_ORDERS = {
    "priority": {
        "high": 1,
        "medium": 2,
        "low": 3
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

def sort_complaints(results : list[Complaint], sort_by : str) -> list[Complaint]:
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

    return sort_complaints([Complaint.model_validate(r) for r in records], sort_by="priority")

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
        return sort_complaints(results, sort_by)

    return results

def list_urgent_and_unresolved_complaints() ->list[Complaint]:

    urgent = list_complaints_by_query(sort_by="priority")

    return [c for c in urgent if c.status != "resolved"]

def create_complaint(complaint : dict) -> Complaint | None:
    """
    Creates a new Complaint object
    """

    valid_complaint = CreateComplaintDto.model_validate(complaint)

    customer = db.session.execute(select(CustomerRecord).where(CustomerRecord.account_number == valid_complaint.customer_account_number)).scalar_one_or_none()
    if customer is None:
        return None

    # pii checks
    pii_check = detect_pii(valid_complaint.body)
    redacted_body = redact_pii(valid_complaint.body, pii_check)
    contained_pii = len(pii_check) > 0

    # priority assignment
    sentiment = detect_sentiment(redacted_body)["sentiment"].lower()
    priority = derive_priority(redacted_body)

    new_complaint = CustomerComplaint(
        customer_id=customer.id, # type: ignore
        channel=valid_complaint.channel, # type: ignore
        priority=priority, # type: ignore
        sentiment=sentiment, # type: ignore
        subject=valid_complaint.subject, # type: ignore
        body=redacted_body, # type: ignore
        contained_pii=contained_pii # type: ignore
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
    if valid_complaint.priority is not None:
        record.priority = valid_complaint.priority

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