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
        "complaint_id": 1,
        "customer_account_number": 10001,
        "channel": "web_form",
        "status": "in_progress",
        "priority": "high",
        "subject": "Unexpectedly high water bill",
        "body": "My water bill this month is much higher than usual and I would like someone to review the charges.",
    },
    {
        "complaint_id": 2,
        "customer_account_number": 10001,
        "channel": "email",
        "status": "new",
        "priority": "medium",
        "subject": "Unexpectedly high water bill",
        "body": "My water bill this month is much higher than usual and I would like someone to review the charges.",
    },
    {
        "complaint_id": 3,
        "customer_account_number": 10002,
        "channel": "web_form",
        "status": "new",
        "priority": "high",
        "subject": "Water service interruption",
        "body": "Our building has been without water since this morning and we need assistance restoring service.",
    },
    {
        "complaint_id": 4,
        "customer_account_number": 10003,
        "channel": "web_form",
        "status": "in_progress",
        "priority": "medium",
        "subject": "Incorrect billing charge",
        "body": "I was charged for a service that I did not request and would like the charge investigated.",
    },
    {
        "complaint_id": 5,
        "customer_account_number": 10004,
        "channel": "email",
        "status": "resolved",
        "priority": "low",
        "subject": "Duplicate billing charge",
        "body": "Our business account appears to have been charged twice for the same invoice.",
    },
    {
        "complaint_id": 6,
        "customer_account_number": 10005,
        "channel": "mail",
        "status": "new",
        "priority": "high",
        "subject": "Service connection problem",
        "body": "My service has not been restored even though my payment was processed several days ago.",
    },
]