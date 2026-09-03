""" test suite for testing Customers
        Full CRUD operations covered
"""

import pytest
from unittest.mock import patch
import random
account_number = random.randint(10000, 99999)

def test_get_customers(client):
    """ testing get endpoint working """

    response = client.get("/api/v1/customers")

    assert response.status_code == 200

def test_get_customers_by_account_type(client):
    """ testing get endpoint with query"""

    response = client.get(
        "/api/v1/customers?account_type=residential"
    )

    assert response.status_code == 200

@pytest.mark.parametrize(
    "customer_data, expected_status",
    [
        (
            {
                "name": "Victoria",
                "account_number": account_number,
                "account_type": "residential"
            },
            200,
        ),
        (
            {
                "name": "",
                "account_number": 12345,
                "account_type": "residential"
            },
            422,
        ),
        (
            {
                "name": "Victoria",
                "account_number": 12345,
                "account_type": "invalid"
            },
            422,
        ),
    ],
)
def test_create_customer(client, customer_data, expected_status):
    """ testing post endpoint working """

    response = client.post("/api/v1/customers", json=customer_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize(
    "account_number, expected_status",
    [
        (account_number, 204),
        (999999, 404),
    ],
)
def test_delete_customer(client, account_number, expected_status):
    """ testing delete endpoint working """

    response = client.delete(f"/api/v1/customers/{account_number}")

    assert response.status_code == expected_status
