"""
System administration and utility API routes.
"""

import os
import signal
from flask import Blueprint, jsonify

# Create blueprint for system routes
system_routes = Blueprint('system', __name__, url_prefix='/api/system')


@system_routes.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        return jsonify({
            "status": "healthy",
            "message": "Aria API server is running",
            "version": "1.0.0",
            "environment": os.getenv('FLASK_ENV', 'development')
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": str(e)
        }), 500


@system_routes.route('/info', methods=['GET'])
def system_info():
    """Get system information and configuration"""
    try:
        info = {
            "python_version": os.sys.version,
            "working_directory": os.getcwd(),
            "environment_variables": {
                "FLASK_ENV": os.getenv('FLASK_ENV', 'not_set'),
                "FLASK_DEBUG": os.getenv('FLASK_DEBUG', 'not_set'),
                "DATABASE_URL": "***configured***" if os.getenv('DATABASE_URL') else "not_set",
                "OPENAI_API_KEY": "***configured***" if os.getenv('OPENAI_API_KEY') else "not_set"
            },
            "directories": {
                "data_exists": os.path.exists('data'),
                "output_exists": os.path.exists('output'),
                "src_exists": os.path.exists('src')
            }
        }
        
        return jsonify({
            "status": "success",
            "system_info": info
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@system_routes.route('/shutdown', methods=['POST'])
def shutdown_server():
    """Gracefully shutdown the server"""
    try:
        # Note: This should be protected in production
        print("🛑 Server shutdown requested...")
        
        # Give the response time to be sent
        def shutdown():
            os.kill(os.getpid(), signal.SIGTERM)
        
        # Schedule shutdown after response is sent
        from threading import Timer
        Timer(1.0, shutdown).start()
        
        return jsonify({
            "status": "success",
            "message": "Server shutdown initiated"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@system_routes.route('/config', methods=['GET'])
def get_configuration():
    """Get current application configuration"""
    try:
        config = {
            "host": os.getenv('FLASK_HOST', 'localhost'),
            "port": int(os.getenv('FLASK_PORT', 8080)),
            "debug": os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
            "cors_enabled": True,
            "database_configured": bool(os.getenv('DATABASE_URL')),
            "openai_configured": bool(os.getenv('OPENAI_API_KEY')),
            "similarity_threshold": float(os.getenv('SIMILARITY_THRESHOLD', 0.8)),
            "max_similar_jobs": int(os.getenv('MAX_SIMILAR_JOBS', 5))
        }
        
        return jsonify({
            "status": "success",
            "configuration": config
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500