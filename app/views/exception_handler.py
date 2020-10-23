from app.model.exceptions import ValidationException
from flask import Blueprint, jsonify

app_error_handler = Blueprint('app_error_handler', __name__)


@app_error_handler.app_errorhandler(ValidationException)
def handle_error_validation(ex):
    return jsonify({'message': str(ex)}), 400


@app_error_handler.app_errorhandler(Exception)
def handle_error_generic(ex):
    return jsonify({'message': "failed"}), 500
