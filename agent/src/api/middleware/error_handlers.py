"""
Error handling middleware for the Flask application.
"""

from flask import jsonify
import traceback


def register_error_handlers(app):
    """
    Register error handlers for the Flask application.
    
    Args:
        app (Flask): Flask application instance
    """
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors"""
        return jsonify({
            "status": "error",
            "error_code": 404,
            "message": "Resource not found",
            "details": "The requested endpoint does not exist"
        }), 404

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors"""
        return jsonify({
            "status": "error",
            "error_code": 400,
            "message": "Bad request",
            "details": str(error.description) if hasattr(error, 'description') else "Invalid request format"
        }), 400

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed errors"""
        return jsonify({
            "status": "error",
            "error_code": 405,
            "message": "Method not allowed",
            "details": "The request method is not allowed for this endpoint"
        }), 405

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server Error"""
        # Log the full traceback for debugging
        app.logger.error(f"Internal server error: {error}")
        app.logger.error(traceback.format_exc())
        
        return jsonify({
            "status": "error",
            "error_code": 500,
            "message": "Internal server error",
            "details": "An unexpected error occurred on the server"
        }), 500

    @app.errorhandler(413)
    def handle_request_entity_too_large(error):
        """Handle 413 Request Entity Too Large errors"""
        return jsonify({
            "status": "error",
            "error_code": 413,
            "message": "Request entity too large",
            "details": "The uploaded file is too large"
        }), 413

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle custom validation errors"""
        return jsonify({
            "status": "error",
            "error_code": 422,
            "message": "Validation error",
            "details": str(error)
        }), 422

    @app.errorhandler(DatabaseError)
    def handle_database_error(error):
        """Handle database-related errors"""
        app.logger.error(f"Database error: {error}")
        return jsonify({
            "status": "error",
            "error_code": 503,
            "message": "Database error",
            "details": "A database operation failed"
        }), 503

    @app.errorhandler(FileNotFoundError)
    def handle_file_not_found(error):
        """Handle file not found errors"""
        return jsonify({
            "status": "error",
            "error_code": 404,
            "message": "File not found",
            "details": str(error)
        }), 404

    print("✅ Error handlers registered successfully")


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class DatabaseError(Exception):
    """Custom exception for database errors"""
    pass


class FileProcessingError(Exception):
    """Custom exception for file processing errors"""
    pass