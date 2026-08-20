"""

Logic for complaints

CRUD operations on data

"""

from complaint_system.data import COMPLAINTS
from complaint_system.models import Complaint, CreateComplaintDto, UpdateComplaintDto, Priority, Status, Channel
from pydantic import TypeAdapter
from complaint_system.customers import store as customer_store

priorityAdaptor = TypeAdapter(Priority)
statusAdaptor = TypeAdapter(Status)
channelAdaptor = TypeAdapter(Channel)

# will be removed once we connect to DB
#   turning list into Complaint objects
_complaints : list[Complaint] = [Complaint.model_validate(row) for row in COMPLAINTS]

def list_complaints() -> list[Complaint]:
    """
    Returns all Customers
    """

    return _complaints

# missing sentiment comes later
def list_complaints_by_query(*, customer_account_number : str | None = None, priority : str | None = None, status : str | None = None, channel : str | None = None) -> list[Complaint]:
    """
    Filters support by customer, *sentiment*, derived priority, and status, sorted with the most urgent first.
    """

    results = _complaints

    if customer_account_number is not None:
        new_num = int(customer_account_number)
        results = [c for c in results if c.customer_account_number == new_num]
    if priority is not None:
        valid_priority = priorityAdaptor.validate_python(priority)
        results = [c for c in results if c.priority == valid_priority]
    if status is not None:
        valid_status = statusAdaptor.validate_python(status)
        results = [c for c in results if c.status == valid_status]
    if channel is not None:
        valid_channel = channelAdaptor.validate_python(channel)
        results = [c for c in results if c.channel == valid_channel]

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
    customer_exists = customer_store.find_customer_by_account_number(valid_complaint.customer_account_number)

    if customer_exists is None:
        # return None and trigger exception if no customer exists with tht id
        return None

    # simulate DB creating a new complaint_id
    complaint_id = _complaints[-1].complaint_id + 1
    new_complaint = Complaint(complaint_id=complaint_id, **valid_complaint.model_dump())

    # simulate saving to DB
    _complaints.append(new_complaint)

    return new_complaint

def update_complaint_status_and_priority(complaint_id : int, complaint : dict) -> Complaint | None:
    """
    Updating existing Complaint
    """

    valid_complaint = UpdateComplaintDto.model_validate(complaint)

    for c in _complaints:
        if c.complaint_id == complaint_id:
            if valid_complaint.status is not None:
                c.status = valid_complaint.status
            if valid_complaint.priority is not None:
                c.priority = valid_complaint.priority

            return c

    return None

def delete_complaint(complaint_id : int) -> bool:
    """
    Delete existing Complaint
    """

    for complaint in _complaints:
        if complaint.complaint_id == complaint_id:
            _complaints.remove(complaint)
            return True

    return False