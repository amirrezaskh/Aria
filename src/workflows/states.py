"""State definitions for LangGraph workflows"""

from typing import List, Optional
from typing_extensions import TypedDict
from langchain_core.documents import Document


class ResumeState(TypedDict):
    """State definition for resume generation workflow"""
    
    # Input
    job_posting: str
    company: str
    position: str
    
    # Intermediate results
    experiences: str
    skills: str
    project_names: List[str]
    project_summaries: str
    highlights: str
    
    # Final outputs
    resume_latex: str
    latex_file: Optional[str]
    pdf_file: Optional[str]
    
    # RAG context (for cover letters)
    context: List[Document]
    
    # Metadata
    generation_metadata: dict


class OptimizationState(TypedDict):
    """State definition for resume optimization workflow"""
    
    # Input
    original_state: ResumeState
    target_pages: int
    max_iterations: int
    
    # Current iteration
    current_iteration: int
    current_strategy: dict
    current_pages: Optional[int]
    
    # Results
    optimized_state: Optional[ResumeState]
    optimization_history: List[dict]