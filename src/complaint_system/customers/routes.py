"""

API endpoints for customers

"""

from flask import Blueprint, request, jsonify
from . import store
from .responses import list_envelope, single_envelope, DuplicateAccountNumberError
from ..error_responses import NoCustomerFoundError

customers_bp = Blueprint("customers", __name__)

# GET /api/v1/customers
@customers_bp.get("")
def get_customers():
    """
    Get all Customers or by account type endpoint
    """
    account_type = request.args.get("account_type")

    # if query is given give me all Customers with that account type
    if account_type:
        return list_envelope(store.find_customers_by_account_type(account_type))

    return list_envelope(store.list_customers())

# GET /api/v1/customers/<account_number>
@customers_bp.get("/<int:account_number>")
def get_customer_by_account_number(account_number : int):
    """
    Get Customer by account_number endpoint
    """

    customer = store.find_customer_by_account_number(account_number)

    if customer is None:
        raise NoCustomerFoundError(code="customer_not_found", status=400, detail=f"Customer with account number {account_number} was not found")
    return single_envelope(customer)

# POST /api/v1/customers
@customers_bp.post("")
def create_customer():
    """
    Create Customer endpoint
    """

    body = request.get_json(silent=True) or {}
    new_customer = store.create_customer(body)

    if new_customer is None:
        raise DuplicateAccountNumberError(code="duplicate_account_number", status=400, detail=f"Customer with account number {body["account_number"]} already exists")

    return single_envelope(new_customer)

# PUT /api/v1/customers/<account_number>
@customers_bp.put("/<int:account_number>")
def update_customer(account_number : int):
    """
    Updates existing Customer endpoint
    """

    body = request.get_json(silent=True) or {}

    customer = store.update_customer(account_number, body)

    if customer is None:
        raise NoCustomerFoundError(code="customer_not_found", status=400, detail=f"Customer with account number {account_number} was not found")
    return single_envelope(customer)

# Delete /api/v1/customers/<account_number>
@customers_bp.delete("/<int:account_number>")
def delete_customer(account_number : int):
    """
    Delete existing Customer endpoint
    """

    success = store.delete_customer(account_number)

    if success:
        return jsonify(status="deleted"), 204
    raise NoCustomerFoundError(code="customer_not_found", status=400, detail=f"Customer with account number {account_number} was not found")