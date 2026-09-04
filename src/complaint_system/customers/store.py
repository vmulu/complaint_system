"""

Logic for customers

CRUD operations on data

"""

from complaint_system.models import Customer, SendCustomer, CreateCustomerDto, UpdateCustomerDto, AccountType
from pydantic import TypeAdapter
from sqlalchemy import select
from complaint_system.extensions import db
from complaint_system.db_models import CustomerRecord

accountTypeAdaptor = TypeAdapter(AccountType)

def list_customers() -> list[SendCustomer]:
    """
    Returns all Customers
    """

    stmt = select(CustomerRecord).order_by(CustomerRecord.id)
    records = db.session.execute(stmt).scalars()

    return [
        SendCustomer(
            name=r.name,
            account_number=r.account_number,
            account_type=r.account_type,        # type: ignore
            complaint_count=len(r.complaints)
        )
        for r in records
    ]

def find_customers_by_account_type(account_type : str) -> list[SendCustomer]:
    """
    Returns all Customers who have this account_type
    """

    valid_account_type = accountTypeAdaptor.validate_python(account_type)

    stmt = select(CustomerRecord).where(CustomerRecord.account_type == valid_account_type)
    records = db.session.execute(stmt).scalars()

    return [
        SendCustomer(
            name=r.name,
            account_number=r.account_number,
            account_type=r.account_type, # type: ignore
            complaint_count=len(r.complaints)
        )
        for r in records
    ]

def find_customer_by_account_number(account_number : int) -> SendCustomer | None:
    """
    Returns Customer that has given account_number
    """

    stmt = select(CustomerRecord).where(CustomerRecord.account_number == account_number)
    record = db.session.execute(stmt).scalar_one_or_none()

    return SendCustomer(
            name=record.name,
            account_number=record.account_number,
            account_type=record.account_type, # type: ignore
            complaint_count=len(record.complaints)
        ) if record is not None else None

def create_customer(customer : dict) -> Customer | None:
    """
    Creates a new Customer object
    """

    valid_customer = CreateCustomerDto.model_validate(customer)
    existing_customer = find_customer_by_account_number(valid_customer.account_number)

    # if a customer exists with this account number return None and catch in routes
    if existing_customer is not None:
        return None

    new_customer = CustomerRecord(**valid_customer.model_dump())

    db.session.add(new_customer)
    db.session.commit()

    return Customer.model_validate(new_customer)

def update_customer(account_number : int, customer : dict) -> Customer | None:
    """
    Updating an existing Customer
    """

    valid_customer = UpdateCustomerDto.model_validate(customer)
    stmt = select(CustomerRecord).where(CustomerRecord.account_number == account_number)
    record = db.session.execute(stmt).scalar_one_or_none()

    if record is None:
        return None

    if valid_customer.name is not None:
        record.name = valid_customer.name
    if valid_customer.account_type is not None:
        record.account_type = valid_customer.account_type

    db.session.commit()

    return Customer.model_validate(record)

def delete_customer(account_number : int) -> bool:
    """
    Delete an existing Customer
    """

    stmt = select(CustomerRecord).where(CustomerRecord.account_number == account_number)
    record = db.session.execute(stmt).scalar_one_or_none()

    if record is None:
        return False

    db.session.delete(record)
    db.session.commit()

    return True