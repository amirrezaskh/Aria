"""
Database connection management module.
Handles PostgreSQL connections and configuration.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Manages database connections and configuration."""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'aria')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        
    def get_connection(self) -> Optional[psycopg2.extensions.connection]:
        """Get a database connection with RealDictCursor."""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            return conn
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test the database connection and return status."""
        conn = self.get_connection()
        if not conn:
            print("❌ Failed to connect to database")
            return False
            
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Database connected successfully!")
            print(f"PostgreSQL version: {version['version']}")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error testing connection: {e}")
            if conn:
                conn.close()
            return False
    
    def get_connection_info(self) -> dict:
        """Get connection configuration info (without sensitive data)."""
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password_set": bool(self.password)
        }