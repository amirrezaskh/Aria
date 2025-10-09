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


@resumes_routes.route('/generated/<path:resume_path>', methods=['GET'])
def serve_generated_resume(resume_path):
    """Serve generated resume PDFs from the output directory"""
    try:
        # URL decode and sanitize the path to prevent directory traversal attacks
        decoded_path = unquote(resume_path)
        safe_path = decoded_path.replace('..', '').strip('/')
        
        # Construct full path to the resume file
        full_path = os.path.join(os.getcwd(), 'output', 'resumes', safe_path)
        
        if not os.path.exists(full_path):
            return jsonify({
                "status": "error", 
                "message": "Resume file not found"
            }), 404
        
        # Verify it's actually a PDF file
        if not full_path.endswith('.pdf'):
            return jsonify({
                "status": "error", 
                "message": "Invalid file type"
            }), 400
        
        return send_file(full_path, mimetype='application/pdf')
        
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