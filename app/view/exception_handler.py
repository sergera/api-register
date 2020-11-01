from flask import Blueprint, jsonify

from app.model.exceptions import ValidationException
from app.repository.exceptions import (CouldNotGetDocumentException,
                                       CouldNotGetDocumentsException,
                                       CouldNotInsertDocumentException,
                                       ExistingDocumentException,
	                                   CouldNotDeleteDocumentException,
                                       CouldNotDeleteDocumentsException,
                               	       CouldNotDropDatabaseException,
                                       CouldNotDropCollectionException)

app_error_handler = Blueprint("app_error_handler", __name__)

@app_error_handler.app_errorhandler(ValidationException)
def handle_error_validation(ex):
	return jsonify({"message": str(ex)}), 400

@app_error_handler.app_errorhandler(CouldNotGetDocumentException)
def handle_error_get_document(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotGetDocumentsException)
def handle_error_get_documents(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotInsertDocumentException)
def handle_error_insert_document(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(ExistingDocumentException)
def handle_error_existing_document(ex):
	return jsonify({"message": str(ex)}), 409

@app_error_handler.app_errorhandler(CouldNotDeleteDocumentException)
def handle_error_delete_document(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotDeleteDocumentsException)
def handle_error_delete_documents(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotDropCollectionException)
def handle_error_drop_collection(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(CouldNotDropDatabaseException)
def handle_error_drop_database(ex):
	return jsonify({"message": str(ex)}), 500

@app_error_handler.app_errorhandler(Exception)
def handle_error_generic(ex):
	return jsonify({"message": str(ex)}), 500