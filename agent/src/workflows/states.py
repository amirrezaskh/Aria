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
    cover_letter: str
    
    # Final outputs
    resume_latex: str
    resume_latex_file: Optional[str]
    resume_pdf_file: Optional[str]
    cover_letter_latex: str
    cover_letter_latex_file: Optional[str]
    cover_letter_pdf_file: Optional[str]
    
    # RAG context (for cover letters)
    context: List[Document]
    
    # Metadata
    generation_metadata: dict


class CoverLetterState(TypedDict):
    # Input
    job_posting: str
    company: str
    position: str
    resume_pdf_file: str

    # Intermediate results
    resume: str
    cover_letter: str

    # Final outputs
    cover_letter_latex: str
    cover_letter_latex_file: Optional[str]
    cover_letter_pdf_file: Optional[str]

    # RAG context (for cover letters)
    context: List[Document]