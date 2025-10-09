"""
Database schema management module.
Handles table creation, migrations, and constraints.
"""

from typing import Optional
from .connection import DatabaseConnection


class SchemaManager:
    """Manages database schema, tables, and constraints."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
    
    def initialize_schema(self) -> bool:
        """Initialize the complete database schema."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Create job_applications table with embedding column
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_applications (
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    position_title VARCHAR(255) NOT NULL,
                    job_description TEXT NOT NULL,
                    embedding_text TEXT NOT NULL,
                    embedding FLOAT8[] NULL,
                    resume_generated BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT unique_company_position UNIQUE (company_name, position_title)
                );
            """)
            
            # Create indexes for performance
            self._create_indexes(cursor)
            
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Database schema initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing schema: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def _create_indexes(self, cursor) -> None:
        """Create database indexes for performance optimization."""
        indexes = [
            ("idx_company_position", "job_applications(company_name, position_title)"),
            ("idx_created_at", "job_applications(created_at)"),
            ("idx_resume_generated", "job_applications(resume_generated)"),
        ]
        
        for index_name, index_definition in indexes:
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS {index_name} ON {index_definition};
            """)
    
    def add_unique_constraint(self) -> bool:
        """Add unique constraint for company_name and position_title if it doesn't exist."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Check if the constraint already exists
            cursor.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'job_applications' 
                AND constraint_type = 'UNIQUE' 
                AND constraint_name = 'unique_company_position';
            """)
            
            existing_constraint = cursor.fetchone()
            
            if not existing_constraint:
                print("🔧 Adding unique constraint for company_name and position_title...")
                
                cursor.execute("""
                    ALTER TABLE job_applications 
                    ADD CONSTRAINT unique_company_position 
                    UNIQUE (company_name, position_title);
                """)
                
                conn.commit()
                print("✅ Unique constraint added successfully!")
            else:
                print("✅ Unique constraint already exists")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error adding unique constraint: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            
            exists = cursor.fetchone()['exists']
            cursor.close()
            conn.close()
            return exists
            
        except Exception as e:
            print(f"❌ Error checking table existence: {e}")
            if conn:
                conn.close()
            return False
    
    def get_table_info(self, table_name: str) -> Optional[dict]:
        """Get detailed information about a table structure."""
        conn = self.db_connection.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            
            # Get column information
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cursor.fetchall()
            
            # Get constraints
            cursor.execute("""
                SELECT constraint_name, constraint_type
                FROM information_schema.table_constraints
                WHERE table_name = %s;
            """, (table_name,))
            
            constraints = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return {
                "columns": [dict(col) for col in columns],
                "constraints": [dict(const) for const in constraints]
            }
            
        except Exception as e:
            print(f"❌ Error getting table info: {e}")
            if conn:
                conn.close()
            return None