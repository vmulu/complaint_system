"""

Logic for customers

CRUD operations on data

"""

from complaint_system.data import CUSTOMERS
from complaint_system.models import Customer, CreateCustomerDto, UpdateCustomerDto, AccountType
from pydantic import TypeAdapter

accountTypeAdaptor = TypeAdapter(AccountType)

# will be removed once we connect to DB
#   turning list into Customer objects
_customers : list[Customer] = [Customer.model_validate(row) for row in CUSTOMERS]

def list_customers() -> list[Customer]:
    """
    Returns all Customers
    """
    return _customers

def find_customers_by_account_type(account_type : str) -> list[Customer]:
    """
    Returns all Customers who have this account_type
    """

    valid_account_type = accountTypeAdaptor.validate_python(account_type)

    results = []

    for customer in _customers:
        if customer.account_type == valid_account_type:
            results.append(customer)

    return results

def find_customer_by_account_number(account_number : int) -> Customer | None:
    """
    Returns Customer that has given account_number
    """

    for customer in _customers:
        if customer.account_number == account_number:
            return customer

    return None

def create_customer(customer : dict) -> Customer:
    """
    Creates a new Customer object
    """

    valid_customer = CreateCustomerDto.model_validate(customer)

    # simulate DB creating a new account_number
    account_number = _customers[-1].account_number + 1
    new_customer = Customer(account_number=account_number, **valid_customer.model_dump())

    # simulate saving to DB
    _customers.append(new_customer)

    return new_customer

def update_customer(account_number : int, customer : dict) -> Customer | None:
    """
    Updating an existing Customer
    """

    valid_customer = UpdateCustomerDto.model_validate(customer)

    for c in _customers:
        if c.account_number == account_number:
            if valid_customer.name is not None:
                c.name = valid_customer.name
            if valid_customer.account_type is not None:
                c.account_type = valid_customer.account_type

            return c
    return None

def delete_customer(account_number : int):
    """
    Delete an existing Customer
    """

    for customer in _customers:
        if customer.account_number == account_number:
            _customers.remove(customer)
            return True
    return False