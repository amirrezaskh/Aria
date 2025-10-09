"""
Job repository module.
Handles CRUD operations for job applications.
"""

from typing import List, Dict, Optional
from datetime import datetime
from .connection import DatabaseConnection
from .embedding_service import EmbeddingService


class JobRepository:
    """Handles database operations for job applications."""
    
    def __init__(self, db_connection: DatabaseConnection, embedding_service: EmbeddingService):
        self.db_connection = db_connection
        self.embedding_service = embedding_service
    
    def save_job_application(self, company_name: str, position_title: str, job_description: str, resume_generated: bool = False) -> Optional[int]:
        """Save a new job application with embedding."""
        conn = self.db_connection.get_connection()
        if not conn:
            return None
        
        try:
            # Create embedding text and generate embedding
            embedding_text = self.embedding_service.create_job_embedding_text(
                company_name, position_title, job_description
            )
            embedding = self.embedding_service.get_embedding(embedding_text)
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job_applications (company_name, position_title, job_description, embedding_text, embedding, resume_generated)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (company_name, position_title, job_description, embedding_text, embedding, resume_generated))
            
            job_id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            conn.close()
            
            resume_status = "with resume" if resume_generated else "without resume"
            print(f"✅ Job application saved with ID: {job_id} ({resume_status})")
            return job_id
            
        except Exception as e:
            print(f"❌ Error saving job application: {e}")
            
            # Handle unique constraint violation
            if self._is_duplicate_job_error(str(e)):
                print(f"⚠️ Job application for {position_title} at {company_name} already exists")
                existing_id = self._get_existing_job_id(conn, company_name, position_title)
                if existing_id:
                    print(f"📋 Returning existing job ID: {existing_id}")
                    conn.close()
                    return existing_id
            
            conn.rollback()
            conn.close()
            return None
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        """Get a job application by its ID."""
        conn = self.db_connection.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, company_name, position_title, job_description, 
                       embedding_text, resume_generated, created_at, updated_at
                FROM job_applications
                WHERE id = %s;
            """, (job_id,))
            
            job = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return dict(job) if job else None
            
        except Exception as e:
            print(f"❌ Error fetching job by ID {job_id}: {e}")
            if conn:
                conn.close()
            return None
    
    def get_all_job_applications(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """Get all job applications with pagination support."""
        conn = self.db_connection.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT id, company_name, position_title, job_description, 
                       embedding_text, resume_generated, created_at, updated_at
                FROM job_applications
                ORDER BY created_at DESC
            """
            
            params = []
            if limit:
                query += " LIMIT %s OFFSET %s"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [dict(job) for job in jobs]
            
        except Exception as e:
            print(f"❌ Error fetching job applications: {e}")
            if conn:
                conn.close()
            return []
    
    def get_jobs_with_resumes(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all job applications that have generated resumes."""
        conn = self.db_connection.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT id, company_name, position_title, job_description, 
                       embedding, resume_generated, created_at, updated_at
                FROM job_applications
                WHERE resume_generated = TRUE AND embedding IS NOT NULL
                ORDER BY created_at DESC
            """
            
            params = []
            if limit:
                query += " LIMIT %s"
                params.append(limit)
            
            cursor.execute(query, params)
            jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [dict(job) for job in jobs]
            
        except Exception as e:
            print(f"❌ Error fetching jobs with resumes: {e}")
            if conn:
                conn.close()
            return []
    
    def update_job_resume_status(self, job_id: int, resume_generated: bool) -> bool:
        """Update the resume generation status for a job."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE job_applications 
                SET resume_generated = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s;
            """, (resume_generated, job_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                status = "generated" if resume_generated else "not generated"
                print(f"✅ Updated job {job_id} resume status to: {status}")
                return True
            else:
                print(f"⚠️ No job found with ID: {job_id}")
                return False
            
        except Exception as e:
            print(f"❌ Error updating job resume status: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def delete_job_application(self, job_id: int) -> bool:
        """Delete a job application."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM job_applications WHERE id = %s;", (job_id,))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            if rows_affected > 0:
                print(f"✅ Deleted job application with ID: {job_id}")
                return True
            else:
                print(f"⚠️ No job found with ID: {job_id}")
                return False
            
        except Exception as e:
            print(f"❌ Error deleting job application: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def get_job_stats(self) -> Dict:
        """Get statistics about job applications."""
        conn = self.db_connection.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get various statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_jobs,
                    COUNT(CASE WHEN resume_generated = TRUE THEN 1 END) as jobs_with_resumes,
                    COUNT(CASE WHEN embedding IS NOT NULL THEN 1 END) as jobs_with_embeddings,
                    COUNT(DISTINCT company_name) as unique_companies
                FROM job_applications;
            """)
            
            stats = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return dict(stats) if stats else {}
            
        except Exception as e:
            print(f"❌ Error getting job statistics: {e}")
            if conn:
                conn.close()
            return {}
    
    def _is_duplicate_job_error(self, error_message: str) -> bool:
        """Check if the error is due to duplicate job application."""
        error_lower = error_message.lower()
        return ("unique_company_position" in error_lower or 
                "duplicate key" in error_lower)
    
    def _get_existing_job_id(self, conn, company_name: str, position_title: str) -> Optional[int]:
        """Get the ID of an existing job application."""
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM job_applications 
                WHERE company_name = %s AND position_title = %s;
            """, (company_name, position_title))
            
            existing_job = cursor.fetchone()
            cursor.close()
            
            return existing_job['id'] if existing_job else None
        except Exception:
            return None