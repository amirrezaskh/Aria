"""
Job application management API routes.
"""

from flask import Blueprint, request, jsonify
from src.database import db

# Create blueprint for job routes
jobs_routes = Blueprint('jobs', __name__, url_prefix='/api/jobs')


@jobs_routes.route('/save', methods=['POST'])
def save_job_application():
    """Save a new job application"""
    try:
        data = request.get_json()
        company_name = data.get('companyName')
        position_title = data.get('positionTitle')
        job_description = data.get('jobDescription')
        resume_generated = data.get('resumeGenerated', False)
        
        if not all([company_name, position_title, job_description]):
            return jsonify({
                "status": "error", 
                "message": "Missing required fields"
            }), 400
        
        job_id = db.save_job_application(
            company_name, 
            position_title, 
            job_description, 
            resume_generated
        )
        
        if job_id:
            return jsonify({
                "status": "success", 
                "message": "Job application saved successfully",
                "job_id": job_id
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Failed to save job application"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@jobs_routes.route('/similar', methods=['POST'])
def find_similar_jobs():
    """Find similar job applications using vector embeddings"""
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        position_title = data.get('position_title') 
        job_description = data.get('job_description')
        threshold = data.get('threshold', 0.75)  # Default 75% similarity
        
        if not all([company_name, position_title, job_description]):
            return jsonify({
                "status": "error", 
                "message": "Missing required fields"
            }), 400
        
        similar_jobs = db.find_similar_jobs(
            company_name, 
            position_title, 
            job_description, 
            threshold
        )
        
        return jsonify({
            "status": "success",
            "similar_jobs": similar_jobs,
            "count": len(similar_jobs),
            "threshold": threshold,
            "method": "vector_embeddings"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500


@jobs_routes.route('/all', methods=['GET'])
def get_all_jobs():
    """Get all job applications"""
    try:
        jobs = db.get_all_job_applications()
        return jsonify({
            "status": "success",
            "jobs": jobs,
            "count": len(jobs)
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e)
        }), 500