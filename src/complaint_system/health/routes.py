"""routes for checking:
    /live - checking if the process is up and running
    /ready - checking if downstream dependencies are working
"""


from flask import Blueprint, jsonify
from sqlalchemy import text

from ..extensions import db

health_bp = Blueprint("health", __name__)

@health_bp.get("/live")
def live():
    """checking if Flask app is up and running"""
    return jsonify({"status": "flask is alive"}), 200


@health_bp.get("/ready")
def ready():
    """checking connection with db"""
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "db ready"}), 200
    except Exception:
        return jsonify({"status": "db not ready"}), 503