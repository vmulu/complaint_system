"""

Logic for complaints

CRUD operations on data

"""

from complaint_system.data import COMPLAINTS
from complaint_system.models import Complaint, CreateComplaintDto, UpdateComplaintDto, Priority, Status, Channel
from pydantic import TypeAdapter
from complaint_system.customers import store as customer_store
from sqlalchemy import select
from complaint_system.extensions import db
from complaint_system.db_models import CustomerComplaint, CustomerRecord

priorityAdaptor = TypeAdapter(Priority)
statusAdaptor = TypeAdapter(Status)
channelAdaptor = TypeAdapter(Channel)


def list_complaints() -> list[Complaint]:
    """
    Returns all Complaints
    """

    stmt = select(CustomerComplaint).order_by(CustomerComplaint.id)
    records = db.session.execute(stmt).scalars()

    return [Complaint.model_validate(r) for r in records]

# missing sentiment comes later
def list_complaints_by_query(*, customer_id : int | None = None, priority : str | None = None, status : str | None = None, channel : str | None = None) -> list[Complaint]:
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

    records = db.session.execute(stmt).scalars()
    results = [Complaint.model_validate(r) for r in records]

    # sorting results by priority
    PRIORITY_ORDER = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    results.sort(key=lambda complaint: PRIORITY_ORDER[complaint.priority])

    return results

def create_complaint(complaint : dict) -> Complaint | None:
    """
    Creates a new Complaint object
    """

    valid_complaint = CreateComplaintDto.model_validate(complaint)

    # find if customer exists
    customer = db.session.execute(select(CustomerRecord).where(CustomerRecord.account_number == valid_complaint.customer_account_number)).scalar_one_or_none()
    if customer is None:
        # return None and trigger exception if no customer exists with tht id
        return None

    new_complaint = CustomerComplaint(
        customer_id=customer.id, # type: ignore
        channel=valid_complaint.channel, # type: ignore
        subject=valid_complaint.subject, # type: ignore
        body=valid_complaint.body, # type: ignore
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