# Written Complaint Triage System

## Overview

The Written Complaint Triage System is a Flask REST API for managing customers
and their complaints. Complaints are analyzed using Amazon Comprehend to detect
PII and determine sentiment, which is then used to assign a priority.

The system also accepts image/PDF attachments, stores them in Amazon S3, and
uses Amazon Textract to extract text and check whether an account number found
in the document matches the customer associated with the complaint.

The application is backed by PostgreSQL and can be run locally using Docker
Compose.

## Technologies

- Python 3.14
- Flask
- Pydantic v2
- PostgreSQL
- SQLAlchemy
- Flask-Migrate
- boto3
- Amazon Comprehend
- Amazon Textract
- Amazon S3
- pytest
- Docker
- Docker Compose

## Set Up

### Installation

`pip install -e .`

### Running with Docker

`docker compose up --build`

The API is available at:

`http://localhost:5001`

### Testing

`pytest tests -v`

## API Endpoints

### Customers

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/customers` | List all customers |
| GET | `/api/v1/customers?account_type=residential` | Filter customers by account type |
| GET | `/api/v1/customers/<account_number>` | Get a customer |
| POST | `/api/v1/customers` | Create a customer |
| PUT | `/api/v1/customers/<account_number>` | Update a customer |
| DELETE | `/api/v1/customers/<account_number>` | Delete a customer |

### Complaints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/complaints` | List complaints |
| GET | `/api/v1/complaints/urgent` | List unresolved urgent complaints |
| POST | `/api/v1/complaints` | Create a complaint |
| PUT | `/api/v1/complaints/<complaint_id>` | Update complaint status/priority |
| DELETE | `/api/v1/complaints/admin/<complaint_id>` | Delete a complaint |

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health/live` | Check whether the API is running |
| GET | `/api/v1/health/ready` | Check database readiness |

## Data Model

The database consists of two primary entities: `Customer` and `Complaint`.

The ERD documents each entity's fields, primary/foreign keys, and relationship
cardinality.

A customer can have many complaints, while each complaint belongs to one
customer.

**Relationship: Customer 1 → many Complaints**

The ERD is located at:

`docs/ERD.png`

## AWS Services

### Amazon Comprehend

Amazon Comprehend is used for:

- PII detection
- Sentiment analysis

PII detection happens before a complaint is stored. Detected PII is replaced
with `[REDACTED]`.

Sentiment is used to derive complaint priority.

### Amazon S3

Uploaded complaint attachments are stored in an S3 bucket.

### Amazon Textract

Textract extracts text from uploaded image/PDF attachments. The extracted
text is checked for an account number and compared against the customer's
account number.


## Edge Case Handling

### Comprehend Unavailable

If PII detection fails, the complaint is not stored because the system cannot
guarantee that the stored complaint body is free of PII.

If sentiment analysis fails, the complaint is still stored, but its sentiment
is set to null and its priority is set to `needs_manual_review`.

This prevents a failed AI service from silently causing a complaint to receive
a low priority.

### PII Detected

Detected PII is redacted before the complaint body is stored.

The `contained_pii` field is set to `true` when PII is detected.

This allows the system to preserve the complaint while avoiding storage of
sensitive information in the complaint archive.

### Manual Priority Override

Staff can manually override the AI-derived priority.

A `priority_override_reason` is required whenever a priority is manually
overridden.

The manual override remains in place rather than being automatically
recalculated.

### Empty or Short Complaints

Pydantic validation prevents empty complaint subjects and bodies.

The subject and body fields have minimum and maximum length constraints.

This prevents invalid input from reaching Amazon Comprehend and keeps
complaints meaningful enough for analysis.

### Textract Unavailable

If Textract fails or cannot extract any text, the complaint itself is still
processed and stored.

Attachment text extraction is treated as an additional feature and does not
prevent the complaint's own PII and sentiment analysis.

### Invalid Attachments

Only supported image/PDF file types are accepted.

Uploads that do not meet the allowed file type or maximum file size
requirements are rejected with a 422 response.

### Account Number Mismatch

If Textract extracts an account number that does not match the customer
associated with the complaint, the complaint is rejected with a
`document_account_mismatch` error.

The system does not automatically change the customer associated with the
complaint because the mismatch should be reviewed by staff.

### Customer Deletion

Customers use a cascading relationship with complaints.

Deleting a customer therefore deletes the complaints associated with that
customer.

### Concurrent Behavior

- **Two staff members update the same complaint at the same time:**
  Both requests are processed as database transactions. The update that commits last determines the final value stored for the fields being updated. The current system does not use version tracking or optimistic locking to prevent conflicting updates.

- **A customer is deleted while one of their complaints is being analyzed:**
  Customer deletion cascades to their associated complaints because the customer-to-complaint relationship uses `cascade="all, delete-orphan"`. If the complaint is deleted while analysis is occurring, the complaint will ultimately be removed from the database and will not be recreated by the application.

## AWS Configuration

AWS configuration is provided through environment variables.

AWS credentials and secrets are not committed to the repository.

The application uses a dedicated AWS identity with permissions limited to
the services required by the application. IAM policy can be found in:

`docs/iam-policy.json`

## Development Process

Development was organized using a Kanban board with prioritized tasks for
customer management, complaint management, API functionality, AWS integration,
testing, and containerization.

The board was used to track work from development through completion: [Kanban Board](https://trello.com/invite/b/6a9465df12454af7cf26c08e/ATTIe11b0f6965bd907c555beeb883bab6c90992892D/complaint-system-project-board)