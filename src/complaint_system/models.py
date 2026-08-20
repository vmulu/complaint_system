"""
Pydantic models for the complaint system.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

AccountType = Literal["residential", "commercial"]
Channel = Literal["email", "web_form", "mail"]
Status = Literal["new", "in_progress", "resolved"]
Priority = Literal["low", "medium", "high"]

class Customer(BaseModel):
    """
    Represents a customer account
    """

    name : str
    account_number : int
    account_type : AccountType

class CreateCustomerDto(BaseModel):
    """
    DTO for creating a Customer object
    """

    model_config = ConfigDict(extra="forbid")
    name : str
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

    # eventually we need to add customer field that links Complaint -> Customer
    #   have one for now 'customer_account_number' possibly changes when we connect with db

    complaint_id : int
    customer_account_number : int
    channel : Channel
    status : Status = "new"
    priority : Priority = "low"     # default for now until we connect with AWS
    subject : str = Field(min_length=1, max_length=200)
    body : str = Field(min_length=1, max_length=5000)

class CreateComplaintDto(BaseModel):
    """
    DTO for creating a new Complaint object
    """
    model_config = ConfigDict(extra="forbid")

    customer_account_number : int
    channel : Channel
    subject : str = Field(min_length=1, max_length=200)
    body : str = Field(min_length=1, max_length=5000)

class UpdateComplaintDto(BaseModel):
    """
    DTO for updating a Complaint object
    """

    model_config = ConfigDict(extra="forbid")
    status : Status | None = None
    priority : Priority | None = None