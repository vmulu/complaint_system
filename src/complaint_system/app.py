"""


"""

from flask import Flask
from .customers.routes import customers_bp
from .complaints.routes import complaints_bp
from pydantic import ValidationError
from .customers.responses import DuplicateAccountNumberError
from .error_responses import error_response, NoCustomerFoundError, NoComplaintFoundError
import os
from .extensions import db
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    """

    """
    app = Flask(__name__)

    app.register_blueprint(customers_bp, url_prefix="/api/v1/customers")
    app.register_blueprint(complaints_bp, url_prefix="/api/v1/complaints")

    # db set up
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    db.init_app(app)
    migrate.init_app(app, db)

    # Global Error Handling
    @app.errorhandler(DuplicateAccountNumberError)
    def handle_duplicate_account_number_error(error : DuplicateAccountNumberError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(NoCustomerFoundError)
    def handle_no_customer_error(error : NoCustomerFoundError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(NoComplaintFoundError)
    def handle_no_complaint_error(error : NoComplaintFoundError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(ValidationError)
    def handle_validation_error(error : ValidationError):

        first_error = error.errors()[0]
        detail_str = f"{first_error['loc']} : {first_error['msg']}"

        return error_response("validation_failed", 422, detail_str)


    return app