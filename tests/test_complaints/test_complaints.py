""" test suite for testing Complaints
        Full CRUD operations covered
"""

import pytest
from unittest.mock import patch
from complaint_system.models import Complaint

def test_get_complaints(client):
    """ testing get endpoint working """

    response = client.get("/api/v1/complaints")

    assert response.status_code == 200

@pytest.mark.parametrize(
    "complaint_data, expected_status",
    [
        (
            {
                "customer_account_number": 44636,
                "channel": "email",
                "subject": "High bill",
                "body": "My bill is much higher than usual."
            },
            200,
        ),
        (
            {
                "customer_account_number": 44636,
                "channel": "invalid",
                "subject": "High bill",
                "body": "My bill is much higher than usual."
            },
            422,
        ),
        (
            {
                "customer_account_number": 44636,
                "channel": "email",
                "subject": "",
                "body": "My bill is much higher than usual."
            },
            422,
        ),
        (
            {
                "customer_account_number": 44636,
                "channel": "email",
                "subject": "High bill",
                "body": ""
            },
            422,
        ),
    ],
)
def test_create_complaint(client, complaint_data, expected_status):
    """ testing post endpoint working """

    response = client.post("/api/v1/complaints", json=complaint_data)

    assert response.status_code == expected_status

@pytest.mark.parametrize(
    "complaint_data",
    [
        {"priority": "high"},
        {"priority_override_reason": "Urgent issue"},
    ],
)
def test_update_complaint_requires_override_reason(client, complaint_data):
    """ testing put endpoint working """

    response = client.put("/api/v1/complaints/3", json=complaint_data)

    assert response.status_code == 422

@pytest.mark.parametrize(
    "confirm, expected_status",
    [
        (None, 400),
        ("false", 400),
        ("true", 204),
    ],
)
def test_delete_complaint_confirmation(client, confirm, expected_status):
    """ testing delete endpoint working """

    with patch("complaint_system.complaints.routes.store.delete_complaint", return_value=True):

        if confirm is None:
            response = client.delete("/api/v1/complaints/admin/1")
        else:
            response = client.delete(f"/api/v1/complaints/admin/1?confirm={confirm}")

    assert response.status_code == expected_status