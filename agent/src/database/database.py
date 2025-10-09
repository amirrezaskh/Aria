"""
Main database module - Industrial-grade modular database architecture.
Orchestrates all database services and provides a unified interface.
"""

from typing import List, Dict, Optional
from .connection import DatabaseConnection
from .schema import SchemaManager
from .embedding_service import EmbeddingService
from .job_repository import JobRepository
from .similarity_service import SimilarityService


class Database:
    """
    Industrial-grade database manager that orchestrates all database services.
    
    This class provides a unified interface to all database operations while
    maintaining separation of concerns through specialized service classes.
    """
    
    def __init__(self):
        # Initialize core services
        self.connection = DatabaseConnection()
        self.schema_manager = SchemaManager(self.connection)
        self.embedding_service = EmbeddingService()
        self.job_repository = JobRepository(self.connection, self.embedding_service)
        self.similarity_service = SimilarityService(self.connection, self.embedding_service)
    
    # Connection Management
    def test_connection(self) -> bool:
        """Test the database connection."""
        return self.connection.test_connection()
    
    def get_connection_info(self) -> dict:
        """Get connection configuration info (without sensitive data)."""
        return self.connection.get_connection_info()
    
    # Schema Management
    def initialize_schema(self) -> bool:
        """Initialize the complete database schema."""
        return self.schema_manager.initialize_schema()
    
    def add_unique_constraint(self) -> bool:
        """Add unique constraint for company_name and position_title."""
        return self.schema_manager.add_unique_constraint()
    
    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        return self.schema_manager.check_table_exists(table_name)
    
    def get_table_info(self, table_name: str) -> Optional[dict]:
        """Get detailed information about a table structure."""
        return self.schema_manager.get_table_info(table_name)
    
    # Job Repository Operations
    def save_job_application(self, company_name: str, position_title: str, 
                           job_description: str, resume_generated: bool = False) -> Optional[int]:
        """Save a new job application with embedding."""
        return self.job_repository.save_job_application(
            company_name, position_title, job_description, resume_generated
        )
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        """Get a job application by its ID."""
        return self.job_repository.get_job_by_id(job_id)
    
    def get_all_job_applications(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """Get all job applications with pagination support."""
        return self.job_repository.get_all_job_applications(limit, offset)
    
    def get_jobs_with_resumes(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all job applications that have generated resumes."""
        return self.job_repository.get_jobs_with_resumes(limit)
    
    def update_job_resume_status(self, job_id: int, resume_generated: bool) -> bool:
        """Update the resume generation status for a job."""
        return self.job_repository.update_job_resume_status(job_id, resume_generated)
    
    def delete_job_application(self, job_id: int) -> bool:
        """Delete a job application."""
        return self.job_repository.delete_job_application(job_id)
    
    def get_job_stats(self) -> Dict:
        """Get statistics about job applications."""
        return self.job_repository.get_job_stats()
    
    # Similarity Operations
    def find_similar_jobs(self, company_name: str, position_title: str, job_description: str, 
                         threshold: float = 0.75, limit: int = 10) -> List[Dict]:
        """Find similar job applications using vector embeddings."""
        return self.similarity_service.find_similar_jobs(
            company_name, position_title, job_description, threshold, limit
        )
    
    def find_similar_jobs_basic(self, company_name: str, position_title: str, 
                               job_description: str, limit: int = 10) -> List[Dict]:
        """Fallback: Find similar job applications using basic text matching."""
        return self.similarity_service.find_similar_jobs_basic(
            company_name, position_title, job_description, limit
        )
    
    def get_job_similarity_matrix(self, job_ids: List[int]) -> Dict[int, Dict[int, float]]:
        """Calculate similarity matrix between multiple jobs."""
        return self.similarity_service.get_job_similarity_matrix(job_ids)
    
    def backfill_embeddings(self) -> bool:
        """Generate embeddings for existing job applications that don't have them."""
        return self.similarity_service.backfill_embeddings()
    
    # Embedding Operations
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate OpenAI embedding for given text."""
        return self.embedding_service.get_embedding(text)
    
    def calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        return self.embedding_service.calculate_cosine_similarity(embedding1, embedding2)
    
    def create_embedding_text(self, company_name: str, position_title: str, job_description: str) -> str:
        """Create standardized text for job embedding generation."""
        return self.embedding_service.create_job_embedding_text(company_name, position_title, job_description)
    
    def get_model_info(self) -> dict:
        """Get information about the current embedding model."""
        return self.embedding_service.get_model_info()
    
    # Utility and Diagnostics
    def get_system_status(self) -> Dict:
        """Get comprehensive system status information."""
        try:
            # Test connection
            connection_ok = self.test_connection()
            
            # Get job statistics
            job_stats = self.get_job_stats()
            
            # Get model info
            model_info = self.get_model_info()
            
            # Get connection info
            connection_info = self.get_connection_info()
            
            return {
                "status": "healthy" if connection_ok else "unhealthy",
                "connection": {
                    "connected": connection_ok,
                    "config": connection_info
                },
                "database": {
                    "jobs": job_stats,
                    "tables": {
                        "job_applications": self.check_table_exists("job_applications")
                    }
                },
                "embedding_service": {
                    "model": model_info,
                    "available": bool(self.embedding_service.openai_client)
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def run_health_check(self) -> bool:
        """Run a comprehensive health check of all services."""
        print("🏥 Running database health check...")
        
        # Test connection
        if not self.test_connection():
            print("❌ Database connection failed")
            return False
        
        # Check schema
        if not self.check_table_exists("job_applications"):
            print("⚠️ Main table 'job_applications' does not exist")
            print("🔧 Initializing schema...")
            if not self.initialize_schema():
                print("❌ Schema initialization failed")
                return False
        
        # Test embedding service
        test_embedding = self.get_embedding("test")
        if not test_embedding:
            print("⚠️ Embedding service not available")
        else:
            print("✅ Embedding service working")
        
        # Get system status
        status = self.get_system_status()
        print(f"📊 System status: {status['status']}")
        
        if status.get('database', {}).get('jobs'):
            job_stats = status['database']['jobs']
            print(f"📈 Jobs: {job_stats.get('total_jobs', 0)} total, {job_stats.get('jobs_with_resumes', 0)} with resumes")
        
        print("✅ Health check completed")
        return True


# Global database instance
db = Database()


# Backward compatibility aliases for existing code
def get_connection():
    """Backward compatibility: Get database connection."""
    return db.connection.get_connection()


def test_connection():
    """Backward compatibility: Test database connection."""
    return db.test_connection()


def initialize_schema():
    """Backward compatibility: Initialize database schema."""
    return db.initialize_schema()