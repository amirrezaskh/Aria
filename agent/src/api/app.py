"""
Flask application factory and configuration.
"""

import os
import concurrent.futures
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .routes import register_blueprints
from .middleware.error_handlers import register_error_handlers
from .middleware.logging import setup_logging


def create_app(config_name='development'):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): Configuration environment name
        
    Returns:
        Flask: Configured Flask application instance
    """
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register all blueprints
    register_blueprints(app)
    
    # Create thread pool executor for async operations
    app.config['EXECUTOR'] = concurrent.futures.ThreadPoolExecutor(3)
    
    return app


def get_app_config():
    """Get application configuration based on environment."""
    return {
        'host': os.getenv('FLASK_HOST', 'localhost'),
        'port': int(os.getenv('FLASK_PORT', 8080)),
        'debug': os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    }