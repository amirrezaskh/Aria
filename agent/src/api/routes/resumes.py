"""
Resume and document serving API routes.
"""

import os
from flask import Blueprint, jsonify, send_file
from urllib.parse import unquote

# Create blueprint for resume routes
resumes_routes = Blueprint('resumes', __name__, url_prefix='/api/resumes')

# Template mapping
RESUME_TEMPLATES = {
    'ml-engineering': 'data/resumes/Resume - ML - New.pdf',
    'data-science': 'data/resumes/Resume - DS.pdf',
    'software-engineering': 'data/resumes/Resume - SWE - New.pdf',
    'overall': 'data/resumes/Resume - OverAll.pdf'
}


@resumes_routes.route('/preview/<template_id>', methods=['GET'])
def preview_resume_template(template_id):
    """Serve resume template PDFs for preview"""
    try:
        # Reject paths that start with 'generated' to avoid conflicts
        if template_id.startswith('generated'):
            return jsonify({
                "status": "error", 
                "message": "Invalid template ID"
            }), 400
            
        if template_id not in RESUME_TEMPLATES:
            return jsonify({
                "status": "error", 
                "message": "Template not found"
            }), 404
        
        resume_path = RESUME_TEMPLATES[template_id]
        full_path = os.path.join(os.getcwd(), resume_path)
        
        if not os.path.exists(full_path):
            return jsonify({
                "status": "error", 
                "message": "Resume file not found"
            }), 404
        
        return send_file(full_path, mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@resumes_routes.route('/generated/<path:file_path>', methods=['GET'])
def serve_generated_file(file_path):
    """Serve generated resume and cover letter PDFs from the output directory"""
    try:
        # URL decode and sanitize the path to prevent directory traversal attacks
        decoded_path = unquote(file_path)
        safe_path = decoded_path.replace('..', '').strip('/')
        
        # Check if the path already includes the directory (resumes/ or cover_letters/)
        if safe_path.startswith('resumes/') or safe_path.startswith('cover_letters/'):
            # Path already includes directory, use it directly
            full_path = os.path.join(os.getcwd(), 'output', safe_path)
            
            if os.path.exists(full_path) and full_path.endswith('.pdf'):
                return send_file(full_path, mimetype='application/pdf')
        else:
            # Legacy format - try both resumes and cover_letters directories
            possible_paths = [
                os.path.join(os.getcwd(), 'output', 'resumes', safe_path),
                os.path.join(os.getcwd(), 'output', 'cover_letters', safe_path)
            ]
            
            for path in possible_paths:
                if os.path.exists(path) and path.endswith('.pdf'):
                    return send_file(path, mimetype='application/pdf')
        
        # File not found in any location
        return jsonify({
            "status": "error", 
            "message": f"File not found: {safe_path}"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@resumes_routes.route('/templates', methods=['GET'])
def list_available_templates():
    """List all available resume templates"""
    try:
        templates = []
        for template_id, file_path in RESUME_TEMPLATES.items():
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.exists(full_path):
                templates.append({
                    "id": template_id,
                    "name": template_id.replace('-', ' ').title(),
                    "preview_url": f"/api/resumes/preview/{template_id}",
                    "file_path": file_path
                })
        
        return jsonify({
            "status": "success",
            "templates": templates,
            "count": len(templates)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500