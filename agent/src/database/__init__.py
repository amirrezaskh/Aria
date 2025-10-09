"""
Database package for Aria application.
"""

from .database import db, Database
from .connection import DatabaseConnection
from .schema import SchemaManager
from .embedding_service import EmbeddingService
from .job_repository import JobRepository
from .similarity_service import SimilarityService


default_db = db

__all__ = [
    # New modular architecture
    'db', 'Database', 'default_db',
    'DatabaseConnection', 'SchemaManager', 'EmbeddingService', 
    'JobRepository', 'SimilarityService',
    
    # Legacy interface
    'db', 'Database'
]