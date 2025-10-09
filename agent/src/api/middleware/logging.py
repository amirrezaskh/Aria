"""
Logging configuration and middleware for the Flask application.
"""

import logging
import os
from datetime import datetime
from flask import request, g
import time


def setup_logging(app):
    """
    Setup logging configuration for the Flask application.
    
    Args:
        app (Flask): Flask application instance
    """
    # Configure logging level based on environment
    log_level = logging.DEBUG if app.config.get('DEBUG', False) else logging.INFO
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging format
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'aria_api.log')),
            logging.StreamHandler()
        ]
    )
    
    # Set up request logging middleware
    @app.before_request
    def before_request():
        """Log request information and start timing"""
        g.start_time = time.time()
        app.logger.info(f"🌐 {request.method} {request.path} - {request.remote_addr}")
        
        # Log request data for POST/PUT requests (be careful with sensitive data)
        if request.method in ['POST', 'PUT'] and request.is_json:
            # Don't log sensitive fields
            data = request.get_json() or {}
            safe_data = {k: v for k, v in data.items() 
                        if k.lower() not in ['password', 'token', 'secret', 'key']}
            if safe_data:
                app.logger.debug(f"📝 Request data: {safe_data}")

    @app.after_request
    def after_request(response):
        """Log response information and request duration"""
        duration = time.time() - g.get('start_time', time.time())
        
        # Log response
        status_emoji = "✅" if response.status_code < 400 else "❌"
        app.logger.info(f"{status_emoji} {request.method} {request.path} - "
                       f"{response.status_code} - {duration:.3f}s")
        
        # Log slow requests
        if duration > 2.0:  # More than 2 seconds
            app.logger.warning(f"🐌 Slow request: {request.method} {request.path} "
                             f"took {duration:.3f}s")
        
        return response

    print("✅ Logging middleware configured successfully")


def get_request_logger():
    """
    Get a logger instance for request-specific logging.
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger('aria_api.requests')


def get_database_logger():
    """
    Get a logger instance for database operations.
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger('aria_api.database')


def get_workflow_logger():
    """
    Get a logger instance for workflow operations.
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger('aria_api.workflows')


def log_api_call(endpoint, method, user_id=None, additional_info=None):
    """
    Log an API call with structured information.
    
    Args:
        endpoint (str): API endpoint called
        method (str): HTTP method used
        user_id (str, optional): User identifier
        additional_info (dict, optional): Additional information to log
    """
    logger = get_request_logger()
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "ip_address": request.remote_addr if request else None,
        "user_agent": request.headers.get('User-Agent') if request else None
    }
    
    if additional_info:
        log_data.update(additional_info)
    
    logger.info(f"API Call: {log_data}")


def log_generation_event(event_type, job_title, company, duration=None, success=True):
    """
    Log document generation events.
    
    Args:
        event_type (str): Type of generation (resume, cover_letter, both)
        job_title (str): Job title for the application
        company (str): Company name
        duration (float, optional): Generation duration in seconds
        success (bool): Whether the generation was successful
    """
    logger = get_workflow_logger()
    
    status = "SUCCESS" if success else "FAILED"
    duration_str = f" in {duration:.3f}s" if duration else ""
    
    logger.info(f"📄 {event_type.upper()} Generation {status}: "
               f"{job_title} at {company}{duration_str}")


def log_database_operation(operation, table, record_id=None, success=True, error=None):
    """
    Log database operations.
    
    Args:
        operation (str): Type of operation (insert, update, delete, select)
        table (str): Database table name
        record_id (str, optional): Record identifier
        success (bool): Whether the operation was successful
        error (str, optional): Error message if operation failed
    """
    logger = get_database_logger()
    
    status = "SUCCESS" if success else "FAILED"
    record_info = f" (ID: {record_id})" if record_id else ""
    error_info = f" - Error: {error}" if error else ""
    
    logger.info(f"🗄️ Database {operation.upper()} {status}: "
               f"{table}{record_info}{error_info}")