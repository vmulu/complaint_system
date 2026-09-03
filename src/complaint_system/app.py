"""
Starting point for Flask App
"""

from .customers.routes import customers_bp
from .complaints.routes import complaints_bp
from .health.routes import health_bp
from .analysis.routes import analysis_bp
from .documents.routes import documents_bp
from .extensions import db
from .customers.responses import DuplicateAccountNumberError
from .complaints.responses import DocumentAccountError, NoComplaintFoundError, DocumentUploadError, PIIDetectionError
from .responses import error_response, NoCustomerFoundError

import os
import json, logging, time, uuid # generates random ids for requests
from flask import Flask, request, g
from flask_migrate import Migrate
from pydantic import ValidationError

migrate = Migrate()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_app():
    """

    """
    app = Flask(__name__)

    app.register_blueprint(customers_bp, url_prefix="/api/v1/customers")
    app.register_blueprint(complaints_bp, url_prefix="/api/v1/complaints")
    app.register_blueprint(health_bp, url_prefix="/api/v1/health")

    # test routes for AWS services
    app.register_blueprint(analysis_bp, url_prefix="/api/v1/analysis")
    app.register_blueprint(documents_bp, url_prefix="/api/v1/document")

    # request logging
    @app.before_request
    def start_request():
        """calculating start time of req and getting ID for req"""
        g.start_time = time.perf_counter()
        g.correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    @app.after_request
    def log_request(response):
        duration = time.perf_counter() - g.start_time

        log_data = {
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration": round(duration * 1000, 2),
            "correlation_id": g.correlation_id
        }

        logger.info(json.dumps(log_data))
        response.headers["X-Correlation-ID"] = g.correlation_id

        return response

    # db set up
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    db.init_app(app)
    migrate.init_app(app, db)

    # Global Error Handling
    @app.errorhandler(PIIDetectionError)
    def handle_pii_detection_error(error : PIIDetectionError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(DocumentUploadError)
    def handle_document_upload_error(error : DocumentUploadError):
        return error_response(error.code, error.status, error.detail)

    @app.errorhandler(DocumentAccountError)
    def handle_document_account_error(error : DocumentAccountError):
        return error_response(error.code, error.status, error.detail)

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