"""
Pydantic models for the complaint system.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

AccountType = Literal["residential", "commercial"]
IntakeChannel = Literal["email", "web_form", "mail"]

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

    intake_channel : IntakeChannel
    subject : str = Field(min_length=1, max_length=200)
    body : str = Field(min_length=1, max_length=5000)

