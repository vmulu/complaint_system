"""
Handling globe error responses
"""
from flask import jsonify

def error_response(code : str, status : int, detail : str | None = None):
    return jsonify(error=code, detail=detail), status