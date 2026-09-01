"""
SQLAlchemy ORM Models
"""

from .extensions import db
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class CustomerRecord(db.Model):
    """
    """

    __tablename__ = "customers"

    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name : Mapped[str] = mapped_column(String(100), nullable=False)
    account_number : Mapped[int] = mapped_column(nullable=False, unique=True,)
    account_type : Mapped[str] = mapped_column(String(20), nullable=False)

    complaints : Mapped[list["CustomerComplaint"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )

class CustomerComplaint(db.Model):
    """
    """

    __tablename__ = "customer_complaints"

    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    channel : Mapped[str] = mapped_column(String(10), nullable=False)
    status : Mapped[str] = mapped_column(String(20), nullable=False, default="new")     # might change default to 'needs_manual_review' if sentiment fails
    priority : Mapped[str] = mapped_column(String(20), nullable=False, default="low")
    sentiment: Mapped[str | None] = mapped_column(String(20),nullable=True)
    subject : Mapped[str] = mapped_column(Text, nullable=False)
    body : Mapped[str] = mapped_column(Text, nullable=False)

    customer : Mapped["CustomerRecord"] = relationship(
        back_populates="complaints"
    )

