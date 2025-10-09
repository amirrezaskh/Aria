"""
File handling utilities for API routes.
"""

import os
from urllib.parse import unquote

# Template mapping for resume files
RESUME_TEMPLATE_MAPPING = {
    'ml-engineering': 'data/resumes/Resume - ML - New.pdf',
    'data-science': 'data/resumes/Resume - DS.pdf',
    'software-engineering': 'data/resumes/Resume - SWE - New.pdf',
    'overall': 'data/resumes/Resume - OverAll.pdf'
}


def resolve_resume_path(resume_pdf_file):
    """
    Resolve resume file path from various input formats.
    
    Args:
        resume_pdf_file (str): Resume file path, URL, or template ID
        
    Returns:
        str: Resolved local file path
        
    Raises:
        ValueError: If template ID is unknown
    """
    resume_file_path = resume_pdf_file
    
    # Handle generated resume URLs
    if resume_pdf_file.startswith("http://localhost:8080/api/resumes/generated/"):
        # Extract the path part after the API endpoint
        path_part = resume_pdf_file.replace("http://localhost:8080/api/resumes/generated/", "")
        decoded_path = unquote(path_part)
        resume_file_path = os.path.join(os.getcwd(), 'output', 'resumes', decoded_path)
        
    # Handle template preview URLs
    elif resume_pdf_file.startswith("http://localhost:8080/api/resumes/preview/"):
        template_id = resume_pdf_file.replace("http://localhost:8080/api/resumes/preview/", "")
        if template_id in RESUME_TEMPLATE_MAPPING:
            resume_file_path = os.path.join(os.getcwd(), RESUME_TEMPLATE_MAPPING[template_id])
        else:
            raise ValueError(f"Unknown template: {template_id}")
    
    return resume_file_path


def validate_resume_file(file_path):
    """
    Validate that a resume file exists and is accessible.
    
    Args:
        file_path (str): Path to the resume file
        
    Returns:
        bool: True if file exists and is valid, False otherwise
    """
    if not file_path:
        return False
        
    if not os.path.exists(file_path):
        return False
        
    # Check if it's a PDF file
    if not file_path.lower().endswith('.pdf'):
        return False
        
    # Check if file is readable
    try:
        with open(file_path, 'rb') as f:
            # Try to read first few bytes to ensure it's accessible
            f.read(1024)
        return True
    except (IOError, OSError):
        return False


def sanitize_file_path(file_path):
    """
    Sanitize file path to prevent directory traversal attacks.
    
    Args:
        file_path (str): Input file path
        
    Returns:
        str: Sanitized file path
    """
    # URL decode if needed
    decoded_path = unquote(file_path)
    
    # Remove any directory traversal attempts
    safe_path = decoded_path.replace('..', '').strip('/')
    
    # Normalize path separators
    safe_path = os.path.normpath(safe_path)
    
    return safe_path


def get_file_info(file_path):
    """
    Get information about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: File information including size, modified time, etc.
    """
    if not os.path.exists(file_path):
        return None
        
    try:
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_file": os.path.isfile(file_path),
            "is_readable": os.access(file_path, os.R_OK),
            "extension": os.path.splitext(file_path)[1].lower()
        }
    except (IOError, OSError):
        return None


def ensure_output_directory(relative_path):
    """
    Ensure that an output directory exists.
    
    Args:
        relative_path (str): Relative path from current working directory
        
    Returns:
        str: Absolute path to the created directory
    """
    full_path = os.path.join(os.getcwd(), relative_path)
    os.makedirs(full_path, exist_ok=True)
    return full_path