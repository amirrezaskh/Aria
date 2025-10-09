"""
Embedding service module.
Handles OpenAI embeddings and vector operations.
"""

import os
import openai
import numpy as np
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


class EmbeddingService:
    """Handles OpenAI embeddings and vector similarity calculations."""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "text-embedding-3-small"
        self.embedding_dimension = 1536  # Dimension for text-embedding-3-small
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """Generate OpenAI embedding for given text."""
        if not text or not text.strip():
            print("⚠️ Empty text provided for embedding")
            return None
            
        try:
            response = self.openai_client.embeddings.create(
                model=self.model,
                input=text.strip()
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"❌ Error getting embedding: {e}")
            return None
    
    def get_batch_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts in batch."""
        if not texts:
            return []
        
        # Filter out empty texts
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        if not valid_texts:
            return [None] * len(texts)
        
        try:
            response = self.openai_client.embeddings.create(
                model=self.model,
                input=valid_texts
            )
            
            embeddings = []
            valid_index = 0
            
            for original_text in texts:
                if original_text and original_text.strip():
                    embeddings.append(response.data[valid_index].embedding)
                    valid_index += 1
                else:
                    embeddings.append(None)
            
            return embeddings
            
        except Exception as e:
            print(f"❌ Error getting batch embeddings: {e}")
            return [None] * len(texts)
    
    def calculate_cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        if not embedding1 or not embedding2:
            return 0.0
        
        if len(embedding1) != len(embedding2):
            print(f"⚠️ Embedding dimension mismatch: {len(embedding1)} vs {len(embedding2)}")
            return 0.0
        
        try:
            # Convert to numpy arrays
            emb1 = np.array(embedding1, dtype=np.float32)
            emb2 = np.array(embedding2, dtype=np.float32)
            
            # Calculate cosine similarity
            dot_product = np.dot(emb1, emb2)
            norm1 = np.linalg.norm(emb1)
            norm2 = np.linalg.norm(emb2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return float(dot_product / (norm1 * norm2))
            
        except Exception as e:
            print(f"❌ Error calculating cosine similarity: {e}")
            return 0.0
    
    def calculate_batch_similarities(self, query_embedding: List[float], embeddings: List[List[float]]) -> List[float]:
        """Calculate cosine similarities between a query embedding and multiple embeddings."""
        if not query_embedding or not embeddings:
            return []
        
        similarities = []
        for embedding in embeddings:
            similarity = self.calculate_cosine_similarity(query_embedding, embedding)
            similarities.append(similarity)
        
        return similarities
    
    def create_job_embedding_text(self, company_name: str, position_title: str, job_description: str) -> str:
        """Create standardized text for job embedding generation."""
        # Clean and format the inputs
        company = company_name.strip() if company_name else "Unknown Company"
        position = position_title.strip() if position_title else "Unknown Position"
        description = job_description.strip() if job_description else "No description provided"
        
        # Create structured text for embedding
        embedding_text = f"Company: {company}. Position: {position}. Description: {description}"
        
        # Truncate if too long (OpenAI has token limits)
        max_length = 8000  # Conservative limit for text-embedding-3-small
        if len(embedding_text) > max_length:
            # Keep company and position, truncate description
            base_text = f"Company: {company}. Position: {position}. Description: "
            remaining_length = max_length - len(base_text) - 3  # 3 for "..."
            truncated_description = description[:remaining_length] + "..."
            embedding_text = base_text + truncated_description
        
        return embedding_text
    
    def validate_embedding(self, embedding: List[float]) -> bool:
        """Validate that an embedding has the correct format and dimension."""
        if not embedding:
            return False
        
        if not isinstance(embedding, list):
            return False
        
        if len(embedding) != self.embedding_dimension:
            print(f"⚠️ Invalid embedding dimension: {len(embedding)}, expected {self.embedding_dimension}")
            return False
        
        # Check if all values are numbers
        try:
            np.array(embedding, dtype=np.float32)
            return True
        except (ValueError, TypeError):
            print("⚠️ Embedding contains non-numeric values")
            return False
    
    def get_model_info(self) -> dict:
        """Get information about the current embedding model."""
        return {
            "model": self.model,
            "dimension": self.embedding_dimension,
            "max_tokens": 8191,  # For text-embedding-3-small
            "description": "OpenAI text-embedding-3-small model"
        }