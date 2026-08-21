# loading fake data

import random
from faker import Faker

from .app import create_app
from .extensions import db
from .db_models import CustomerComplaint, CustomerRecord

fake = Faker()
random.seed(11)

ACCOUNT_TYPE = ["residential", "commercial"]
CHANNEL = ["email", "web_form", "mail"]
STATUS = ["new", "in_progress", "resolved"]
PRIORITY = ["low", "medium", "high"]

def build_customers(count: int = 30) -> list[CustomerRecord]:
    return [
        CustomerRecord(
            name=fake.name(),
            account_number=fake.unique.random_int(min=10000, max=99999),
            account_type=random.choice(ACCOUNT_TYPE),
        )
        for _ in range(count)
    ]

def build_complaints(
    customers: list[CustomerRecord],
) -> list[CustomerComplaint]:

    return [
        CustomerComplaint(
            customer_id=customer.id,
            channel=random.choice(CHANNEL),
            status=random.choice(STATUS),
            priority=random.choice(PRIORITY),
            subject=fake.sentence(nb_words=6).rstrip("."),
            body=fake.paragraph(nb_sentences=3),
        )
        for customer in customers
        for _ in range(random.randint(0, 3))
    ]

def main():
    app = create_app()

    # db.session needs an active Flask application context.
    with app.app_context():

        if db.session.query(CustomerRecord).first() is not None:
            print("customers table is not empty — skipping seed")
            return

        customers = build_customers()

        try:
            db.session.add_all(customers)

            # flush() sends the customers to Postgres and populates
            # their auto-generated IDs without committing yet.
            # This allows build_complaints() to use the real customer IDs.
            db.session.flush()

            complaints = build_complaints(customers)
            db.session.add_all(complaints)

            # Commit customers and complaints together as one transaction.
            db.session.commit()

        except Exception:
            # If anything fails, roll back the entire transaction.
            db.session.rollback()
            raise

        print(
            f"seeded {len(customers)} customers "
            f"and {len(complaints)} complaints"
        )


if __name__ == "__main__":
    main()