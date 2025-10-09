"""
Middleware components for the Aria API.
"""

from .error_handlers import (
    register_error_handlers,
    ValidationError,
    DatabaseError,
    FileProcessingError
)
from .logging import (
    setup_logging,
    get_request_logger,
    get_database_logger,
    get_workflow_logger,
    log_api_call,
    log_generation_event,
    log_database_operation
)

__all__ = [
    # Error handling
    'register_error_handlers',
    'ValidationError',
    'DatabaseError', 
    'FileProcessingError',
    
    # Logging
    'setup_logging',
    'get_request_logger',
    'get_database_logger',
    'get_workflow_logger',
    'log_api_call',
    'log_generation_event',
    'log_database_operation'
]