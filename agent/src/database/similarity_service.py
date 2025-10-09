"""
Similarity service module.
Handles job similarity search and matching operations.
"""

from typing import List, Dict, Optional
from urllib.parse import quote
from .connection import DatabaseConnection
from .embedding_service import EmbeddingService


class SimilarityService:
    """Handles job similarity search using vector embeddings and fallback methods."""
    
    def __init__(self, db_connection: DatabaseConnection, embedding_service: EmbeddingService):
        self.db_connection = db_connection
        self.embedding_service = embedding_service
    
    def find_similar_jobs(self, company_name: str, position_title: str, job_description: str, 
                         threshold: float = 0.75, limit: int = 10) -> List[Dict]:
        """Find similar job applications using vector embeddings (only jobs with resumes)."""
        conn = self.db_connection.get_connection()
        if not conn:
            return []
        
        try:
            # Generate embedding for the query job
            query_text = self.embedding_service.create_job_embedding_text(
                company_name, position_title, job_description
            )
            query_embedding = self.embedding_service.get_embedding(query_text)
            
            if not query_embedding:
                print("❌ Failed to generate embedding for query")
                return self._fallback_similarity_search(company_name, position_title, job_description, limit)
            
            cursor = conn.cursor()
            
            # Get only jobs with embeddings AND resume_generated = true
            cursor.execute("""
                SELECT id, company_name, position_title, job_description, 
                       embedding, resume_generated, created_at
                FROM job_applications
                WHERE embedding IS NOT NULL AND resume_generated = TRUE
                ORDER BY created_at DESC;
            """)
            
            existing_jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if not existing_jobs:
                print("📝 No jobs with generated resumes found for comparison")
                return []
            
            # Calculate similarities and filter
            similar_jobs = self._calculate_job_similarities(
                query_embedding, existing_jobs, threshold
            )
            
            # Sort by similarity score (highest first) and limit results
            similar_jobs.sort(key=lambda x: x['similarity_score'], reverse=True)
            result = similar_jobs[:limit]
            
            print(f"🔍 Found {len(result)} similar jobs with resumes above {threshold} threshold")
            return result
            
        except Exception as e:
            print(f"❌ Error finding similar jobs: {e}")
            if conn:
                conn.close()
            return self._fallback_similarity_search(company_name, position_title, job_description, limit)
    
    def find_similar_jobs_basic(self, company_name: str, position_title: str, 
                               job_description: str, limit: int = 10) -> List[Dict]:
        """Fallback: Find similar job applications using basic text matching."""
        return self._fallback_similarity_search(company_name, position_title, job_description, limit)
    
    def get_job_similarity_matrix(self, job_ids: List[int]) -> Dict[int, Dict[int, float]]:
        """Calculate similarity matrix between multiple jobs."""
        conn = self.db_connection.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Get embeddings for specified jobs
            placeholders = ','.join(['%s'] * len(job_ids))
            cursor.execute(f"""
                SELECT id, embedding
                FROM job_applications
                WHERE id IN ({placeholders}) AND embedding IS NOT NULL;
            """, job_ids)
            
            jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if len(jobs) < 2:
                print("⚠️ Need at least 2 jobs with embeddings for similarity matrix")
                return {}
            
            # Calculate similarity matrix
            similarity_matrix = {}
            for i, job1 in enumerate(jobs):
                similarity_matrix[job1['id']] = {}
                for j, job2 in enumerate(jobs):
                    if i == j:
                        similarity_matrix[job1['id']][job2['id']] = 1.0
                    else:
                        similarity = self.embedding_service.calculate_cosine_similarity(
                            job1['embedding'], job2['embedding']
                        )
                        similarity_matrix[job1['id']][job2['id']] = similarity
            
            return similarity_matrix
            
        except Exception as e:
            print(f"❌ Error calculating similarity matrix: {e}")
            if conn:
                conn.close()
            return {}
    
    def backfill_embeddings(self) -> bool:
        """Generate embeddings for existing job applications that don't have them."""
        conn = self.db_connection.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Get jobs without embeddings
            cursor.execute("""
                SELECT id, company_name, position_title, job_description
                FROM job_applications
                WHERE embedding IS NULL OR embedding_text IS NULL;
            """)
            
            jobs_without_embeddings = cursor.fetchall()
            
            if not jobs_without_embeddings:
                print("✅ All jobs already have embeddings")
                cursor.close()
                conn.close()
                return True
            
            print(f"🔄 Generating embeddings for {len(jobs_without_embeddings)} jobs...")
            
            success_count = 0
            for job in jobs_without_embeddings:
                try:
                    # Create embedding text and generate embedding
                    embedding_text = self.embedding_service.create_job_embedding_text(
                        job['company_name'], 
                        job['position_title'], 
                        job['job_description']
                    )
                    embedding = self.embedding_service.get_embedding(embedding_text)
                    
                    if embedding and self.embedding_service.validate_embedding(embedding):
                        # Update the job with embedding
                        cursor.execute("""
                            UPDATE job_applications 
                            SET embedding_text = %s, embedding = %s, updated_at = CURRENT_TIMESTAMP
                            WHERE id = %s;
                        """, (embedding_text, embedding, job['id']))
                        
                        success_count += 1
                        print(f"  ✅ Generated embedding for job {job['id']}")
                    else:
                        print(f"  ❌ Failed to generate valid embedding for job {job['id']}")
                        
                except Exception as e:
                    print(f"  ❌ Error processing job {job['id']}: {e}")
                    continue
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"✅ Embedding backfill completed: {success_count}/{len(jobs_without_embeddings)} successful")
            return success_count > 0
            
        except Exception as e:
            print(f"❌ Error during embedding backfill: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def _calculate_job_similarities(self, query_embedding: List[float], 
                                  existing_jobs: List[Dict], threshold: float) -> List[Dict]:
        """Calculate similarities between query embedding and existing jobs."""
        similar_jobs = []
        
        for job in existing_jobs:
            if not job['embedding']:
                continue
                
            # Calculate cosine similarity
            similarity = self.embedding_service.calculate_cosine_similarity(
                query_embedding, job['embedding']
            )
            
            if similarity >= threshold:
                # Construct API URL for resume access with URL encoding
                resume_api_path = f"{quote(job['company_name'])}/{quote(job['position_title'])}.pdf"
                resume_url = f"http://localhost:8080/api/resumes/generated/{resume_api_path}"
                
                job_dict = {
                    'id': job['id'],
                    'company_name': job['company_name'],
                    'position_title': job['position_title'],
                    'job_description': job['job_description'],
                    'resume_generated': job['resume_generated'],
                    'created_at': job['created_at'],
                    'similarity_score': round(similarity, 4),
                    'resume_path': resume_url
                }
                similar_jobs.append(job_dict)
        
        return similar_jobs
    
    def _fallback_similarity_search(self, company_name: str, position_title: str, 
                                   job_description: str, limit: int) -> List[Dict]:
        """Fallback similarity search using basic text matching."""
        conn = self.db_connection.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            # Simple similarity search using ILIKE (case-insensitive LIKE)
            cursor.execute("""
                SELECT 
                    id, 
                    company_name, 
                    position_title, 
                    job_description, 
                    resume_generated,
                    created_at,
                    CASE 
                        WHEN LOWER(company_name) = LOWER(%s) AND LOWER(position_title) = LOWER(%s) THEN 0.9
                        WHEN LOWER(company_name) = LOWER(%s) THEN 0.7
                        WHEN LOWER(position_title) ILIKE LOWER(%s) THEN 0.6
                        ELSE 0.3
                    END as similarity_score
                FROM job_applications
                WHERE 
                    resume_generated = TRUE AND (
                        LOWER(company_name) ILIKE LOWER(%s) OR
                        LOWER(position_title) ILIKE LOWER(%s) OR
                        LOWER(job_description) ILIKE LOWER(%s)
                    )
                ORDER BY similarity_score DESC, created_at DESC
                LIMIT %s;
            """, (
                company_name, position_title,  # For exact match scoring
                company_name,  # For company match scoring
                f'%{position_title}%',  # For position match scoring
                f'%{company_name}%',  # For ILIKE searches
                f'%{position_title}%',
                f'%{job_description[:100]}%',  # First 100 chars for basic description match
                limit
            ))
            
            similar_jobs = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Filter jobs with similarity > 0.5 (50%) and add resume URLs
            result = []
            for job in similar_jobs:
                if job['similarity_score'] > 0.5:
                    job_dict = dict(job)
                    
                    # Add resume URL if resume was generated
                    if job['resume_generated']:
                        resume_api_path = f"{quote(job['company_name'])}/{quote(job['position_title'])}.pdf"
                        job_dict['resume_path'] = f"http://localhost:8080/api/resumes/generated/{resume_api_path}"
                    
                    result.append(job_dict)
            
            print(f"🔍 Fallback search found {len(result)} similar jobs")
            return result
            
        except Exception as e:
            print(f"❌ Error in fallback similarity search: {e}")
            if conn:
                conn.close()
            return []