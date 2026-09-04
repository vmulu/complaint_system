"""
Handling globe error responses
"""
from flask import jsonify

class NoCustomerFoundError(Exception):
    """
    Raised when client is looking for a Customer that cannot be found
    """

    def __init__(self, code : str, status : int, detail : str | None = None) -> None:

        super().__init__(detail or code)
        self.code = code
        self.status = status
        self.detail = detail


def error_response(code : str, status : int, detail : str | None = None):
    """error response formatting"""
    return jsonify(error=code, detail=detail), status