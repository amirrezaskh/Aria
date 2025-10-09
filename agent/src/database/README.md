# Database Architecture Documentation

## Overview

This directory contains the modular, industrial-grade database architecture for the Aria application. The architecture has been refactored from a monolithic `database.py` into specialized, focused modules for better maintainability, testability, and scalability.

## Architecture

### 🏗️ Modular Design

```
src/database/
├── __init__.py                 # Package exports and imports
├── connection.py              # Database connection management
├── schema.py                  # Schema and table management
├── embedding_service.py       # OpenAI embedding operations
├── job_repository.py          # Job CRUD operations
├── similarity_service.py      # Similarity search and matching
├── database_v2.py            # Main orchestrating class
├── database.py               # Legacy monolithic implementation
├── migrate_to_modular.py     # Migration testing tool
└── README.md                 # This documentation
```

### 🎯 Separation of Concerns

Each module has a single, well-defined responsibility:

1. **Connection Management** (`connection.py`) - Database connections and configuration
2. **Schema Management** (`schema.py`) - Table creation, migrations, constraints
3. **Embedding Service** (`embedding_service.py`) - Vector operations and OpenAI integration
4. **Job Repository** (`job_repository.py`) - Job application CRUD operations
5. **Similarity Service** (`similarity_service.py`) - Similarity search and matching
6. **Main Database** (`database_v2.py`) - Orchestrates all services

## Usage

### Quick Start

```python
# New modular approach (recommended)
from src.database import db_v2 as db

# Test connection
if db.test_connection():
    print("Connected!")

# Save a job
job_id = db.save_job_application(
    company_name="Google",
    position_title="Software Engineer",
    job_description="Develop AI systems...",
    resume_generated=True
)

# Find similar jobs
similar_jobs = db.find_similar_jobs(
    company_name="Apple",
    position_title="Software Engineer", 
    job_description="Build mobile applications..."
)
```

### Advanced Usage

```python
# Use individual services for fine-grained control
from src.database import DatabaseConnection, EmbeddingService, JobRepository

# Initialize services
connection = DatabaseConnection()
embedding_service = EmbeddingService()
job_repo = JobRepository(connection, embedding_service)

# Direct service usage
embedding = embedding_service.get_embedding("AI Engineer role")
job = job_repo.get_job_by_id(123)
```

## API Reference

### Main Database Class (DatabaseV2)

#### Connection & Health
- `test_connection() -> bool` - Test database connectivity
- `run_health_check() -> bool` - Comprehensive system health check  
- `get_system_status() -> Dict` - Detailed system status information

#### Job Operations
- `save_job_application(company, position, description, resume_generated=False) -> int`
- `get_job_by_id(job_id) -> Dict` 
- `get_all_job_applications(limit=None, offset=0) -> List[Dict]`
- `get_jobs_with_resumes(limit=None) -> List[Dict]`
- `update_job_resume_status(job_id, resume_generated) -> bool`
- `delete_job_application(job_id) -> bool`
- `get_job_stats() -> Dict`

#### Similarity & Search
- `find_similar_jobs(company, position, description, threshold=0.75, limit=10) -> List[Dict]`
- `find_similar_jobs_basic(company, position, description, limit=10) -> List[Dict]`
- `get_job_similarity_matrix(job_ids) -> Dict[int, Dict[int, float]]`
- `backfill_embeddings() -> bool`

#### Embedding Operations
- `get_embedding(text) -> List[float]`
- `calculate_cosine_similarity(emb1, emb2) -> float`
- `create_embedding_text(company, position, description) -> str`
- `get_model_info() -> Dict`

### Individual Services

#### DatabaseConnection
```python
connection = DatabaseConnection()
conn = connection.get_connection()
connection.test_connection()
```

#### EmbeddingService
```python
embedding_service = EmbeddingService()
embedding = embedding_service.get_embedding("text")
similarity = embedding_service.calculate_cosine_similarity(emb1, emb2)
```

#### JobRepository
```python
job_repo = JobRepository(connection, embedding_service)
job_id = job_repo.save_job_application("Google", "SWE", "Description")
job = job_repo.get_job_by_id(job_id)
```

#### SimilarityService
```python
similarity_service = SimilarityService(connection, embedding_service)
similar = similarity_service.find_similar_jobs("Apple", "Engineer", "iOS dev")
```

## Migration Guide

### From Legacy to Modular

1. **Test Current Setup**
   ```bash
   python src/database/migrate_to_modular.py
   ```

2. **Update Imports Gradually**
   ```python
   # Old way
   from src.database import db
   
   # New way  
   from src.database import db_v2 as db
   ```

3. **Verify Functionality**
   - All existing API methods are preserved
   - Enhanced error handling and logging
   - Additional utility methods available

4. **Clean Up** (when confident)
   - Remove `database.py` (legacy file)
   - Update all import statements
   - Remove legacy compatibility aliases

### Backward Compatibility

The new architecture maintains full backward compatibility:

```python
# Both work identically
from src.database import db        # Legacy
from src.database import db_v2     # New modular

# Same API
job_id = db.save_job_application("Company", "Role", "Description")
jobs = db.find_similar_jobs("Company", "Role", "Description")
```

## Configuration

### Environment Variables

```bash
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aria
DB_USER=your_username
DB_PASSWORD=your_password

# OpenAI configuration
OPENAI_API_KEY=your_api_key
```

### Database Setup

```sql
-- PostgreSQL with pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Tables are auto-created by schema manager
-- Run: db.initialize_schema()
```

## Testing

### Health Check
```python
# Comprehensive health check
status = db_v2.run_health_check()
print(f"System healthy: {status}")

# Detailed status
system_status = db_v2.get_system_status()
print(system_status)
```

### Migration Testing
```bash
# Run migration comparison tool
python src/database/migrate_to_modular.py

# Interactive testing mode available
```

## Performance Optimizations

### Database Indexes
- `idx_company_position` - For uniqueness and fast lookups
- `idx_created_at` - For chronological queries  
- `idx_resume_generated` - For filtering jobs with resumes

### Vector Operations
- Batch embedding generation for efficiency
- Cosine similarity using optimized NumPy operations
- Embedding validation and error handling

### Connection Management
- Connection pooling ready (extend DatabaseConnection)
- Proper connection cleanup and error handling
- Configuration-driven connection parameters

## Monitoring & Diagnostics

### System Status
```python
status = db.get_system_status()
# Returns comprehensive system health information
```

### Job Statistics
```python
stats = db.get_job_stats()
# Returns: total_jobs, jobs_with_resumes, jobs_with_embeddings, unique_companies
```

### Embedding Service Info
```python
model_info = db.get_model_info()
# Returns: model, dimension, max_tokens, description
```

## Error Handling

### Graceful Degradation
- Vector similarity falls back to text-based search
- Connection failures are logged and handled
- Invalid embeddings are detected and skipped

### Comprehensive Logging
- All operations include success/failure logging
- Error details for debugging
- Progress tracking for long operations

## Best Practices

### Service Usage
```python
# Use the main Database class for most operations
db = db_v2

# Use individual services for specialized needs
embedding_service = EmbeddingService()
job_repo = JobRepository(connection, embedding_service)
```

### Error Handling
```python
# Always check return values
job_id = db.save_job_application(company, position, description)
if job_id:
    print(f"Job saved with ID: {job_id}")
else:
    print("Failed to save job")
```

### Connection Management
```python
# Use the orchestrated Database class (handles connections internally)
# Or manage connections manually if needed
connection = DatabaseConnection()
if connection.test_connection():
    # Proceed with operations
```

## Future Enhancements

### Planned Features
- [ ] Connection pooling for high-traffic scenarios
- [ ] Database migration versioning system  
- [ ] Metrics and monitoring integration
- [ ] Caching layer for frequent queries
- [ ] Async operation support

### Extensibility Points
- Add new repository classes for other entities
- Extend embedding service for different models
- Add custom similarity algorithms
- Implement additional database backends

## Support

### Troubleshooting
1. Run health check: `db.run_health_check()`
2. Check system status: `db.get_system_status()`
3. Test migration: `python src/database/migrate_to_modular.py`
4. Verify environment variables are set correctly

### Common Issues
- **Connection failures**: Check DB credentials and PostgreSQL service
- **Embedding failures**: Verify OPENAI_API_KEY is valid
- **Schema issues**: Run `db.initialize_schema()` 
- **Migration concerns**: Use migration tool for side-by-side testing

---

This modular architecture provides a solid foundation for scalable, maintainable database operations while preserving full backward compatibility with existing code.