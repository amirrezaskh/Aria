#!/usr/bin/env python3
"""
Aria API Server - Main entry point for the Flask application.

This file provides a clean, modular entry point for the Aria API server
using the new component-based architecture.
"""

import os
import sys
from src.api import create_app, get_app_config


def main():
    """
    Main entry point for the Aria API server.
    """
    try:
        # Create the Flask application using the application factory
        app = create_app()
        
        # Get configuration
        config = get_app_config()
        
        print("🚀 Starting Aria API Server...")
        
        # Start the Flask development server
        app.run(
            host=config['host'],
            port=config['port'],
            debug=config['debug'],
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n👋 Server shutdown requested by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()