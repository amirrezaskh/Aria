"""
Database management API routes.
"""

from flask import Blueprint, jsonify
from src.database import db

# Create blueprint for database routes
db_routes = Blueprint('database', __name__, url_prefix='/api/db')


@db_routes.route('/test', methods=['GET'])
def test_database():
    """Test database connection"""
    try:
        if db.test_connection():
            return jsonify({
                "status": "success", 
                "message": "Database connected successfully"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to connect to database"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@db_routes.route('/init', methods=['POST'])
def initialize_database():
    """Initialize database schema"""
    try:
        if db.initialize_schema():
            return jsonify({
                "status": "success", 
                "message": "Database schema initialized successfully"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to initialize database schema"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@db_routes.route('/backfill', methods=['POST'])
def backfill_embeddings():
    """Generate embeddings for existing jobs that don't have them"""
    try:
        if db.backfill_embeddings():
            return jsonify({
                "status": "success", 
                "message": "Embeddings backfilled successfully"
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to backfill embeddings"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500