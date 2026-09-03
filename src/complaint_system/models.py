"""
Pydantic models for the complaint system.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

AccountType = Literal["residential", "commercial"]
Channel = Literal["email", "web_form", "mail"]
Status = Literal["new", "in_progress", "resolved"]
Priority = Literal["low", "medium", "high", "needs_manual_review"]

class Customer(BaseModel):
    """
    Represents a customer account
    """

    model_config = ConfigDict(from_attributes=True)

    name : str = Field(min_length=2)
    account_number: int = Field(ge=10000, le=99999)
    account_type : AccountType

class SendCustomer(BaseModel):
    """
    Represents a read only customer. Only meant to display complaint count.
    """
    model_config = ConfigDict(from_attributes=True)

    name : str = Field(min_length=2)
    account_number: int = Field(ge=10000, le=99999)
    account_type : AccountType

    complaint_count : int

class CreateCustomerDto(BaseModel):
    """
    DTO for creating a Customer object
    """

    model_config = ConfigDict(extra="forbid")
    name : str = Field(min_length=2)
    account_number: int = Field(ge=10000, le=99999)
    account_type : AccountType

class UpdateCustomerDto(BaseModel):
    """
    DTO for updating a Customer object
    """

    model_config = ConfigDict(extra="forbid")
    name : str | None = None
    account_type : AccountType | None = None

class Complaint(BaseModel):
    """
    Represents a written complaint submitted by a customer.
    """

    model_config = ConfigDict(from_attributes=True)

    id : int
    customer_id : int
    channel : Channel
    status : Status = "new"
    priority : Priority = "low"     # default for now until we connect with AWS
    sentiment: str | None = None
    subject : str = Field(min_length=1, max_length=200)
    body : str = Field(min_length=1, max_length=5000)
    contained_pii: bool = False
    document_text: str | None = None

class CreateComplaintDto(BaseModel):
    """
    DTO for creating a new Complaint object
    """
    model_config = ConfigDict(extra="forbid")

    customer_account_number : int
    channel : Channel
    subject : str = Field(min_length=1, max_length=200)
    body : str = Field(min_length=10, max_length=5000)

class UpdateComplaintDto(BaseModel):
    """
    DTO for updating a Complaint object
    """

    model_config = ConfigDict(extra="forbid")
    status : Status | None = None
    priority : Priority | None = None
    priority_override_reason: str | None = None