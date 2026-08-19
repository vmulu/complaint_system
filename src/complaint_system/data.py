"""
fake data to test my endpoints
"""

CUSTOMERS = [
    {
        "name": "John Smith",
        "account_number": 10001,
        "account_type": "residential",
    },
    {
        "name": "Green Valley Apartments",
        "account_number": 10002,
        "account_type": "commercial",
    },
    {
        "name": "Sarah Johnson",
        "account_number": 10003,
        "account_type": "residential",
    },
    {
        "name": "Boston Market LLC",
        "account_number": 10004,
        "account_type": "commercial",
    },
    {
        "name": "Michael Brown",
        "account_number": 10005,
        "account_type": "residential",
    },
]


COMPLAINTS = [
    {
        "id": 1,
        "customer_account_number": 10001,
        "intake_channel": "email",
        "subject": "Unexpectedly high water bill",
        "body": "My water bill this month is much higher than usual.",
        "status": "open",
    },
    {
        "id": 2,
        "customer_account_number": 10002,
        "intake_channel": "phone",
        "subject": "Water service interruption",
        "body": "Our building has been without water since this morning.",
        "status": "open",
    },
    {
        "id": 3,
        "customer_account_number": 10003,
        "intake_channel": "web",
        "subject": "Incorrect billing charge",
        "body": "I was charged for a service that I did not request.",
        "status": "in_progress",
    },
    {
        "id": 4,
        "customer_account_number": 10004,
        "intake_channel": "email",
        "subject": "Business account issue",
        "body": "Our account appears to have been charged twice for the same invoice.",
        "status": "resolved",
    },
    {
        "id": 5,
        "customer_account_number": 10005,
        "intake_channel": "phone",
        "subject": "Service connection problem",
        "body": "My service has not been restored even though my payment was processed.",
        "status": "open",
    },
]