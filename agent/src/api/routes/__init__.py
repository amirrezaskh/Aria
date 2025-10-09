"""
Blueprint registration for all API routes.
"""

from .database import db_routes
from .jobs import jobs_routes
from .generation import generation_routes
from .resumes import resumes_routes
from .context import context_routes
from .system import system_routes


def register_blueprints(app):
    """
    Register all API blueprints with the Flask application.
    
    Args:
        app (Flask): Flask application instance
    """
    # Database management routes
    app.register_blueprint(db_routes)
    
    # Job application routes
    app.register_blueprint(jobs_routes)
    
    # Document generation routes
    app.register_blueprint(generation_routes)
    
    # Resume serving routes
    app.register_blueprint(resumes_routes)
    
    # Context/vector store routes
    app.register_blueprint(context_routes)
    
    # System administration routes
    app.register_blueprint(system_routes)
    
    print("✅ All API blueprints registered successfully")


def get_registered_routes(app):
    """
    Get a list of all registered routes for debugging.
    
    Args:
        app (Flask): Flask application instance
        
    Returns:
        list: List of route information dictionaries
    """
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "path": str(rule),
            "blueprint": rule.endpoint.split('.')[0] if '.' in rule.endpoint else None
        })
    return routes