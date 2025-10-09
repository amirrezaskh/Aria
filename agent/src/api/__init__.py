"""
API package for Aria Flask application.

This package contains the modular API structure with organized routes,
middleware, and utilities for the Aria resume generation platform.
"""

from .app import create_app, get_app_config

__version__ = "1.0.0"
__author__ = "Aria Development Team"

__all__ = [
    'create_app',
    'get_app_config'
]