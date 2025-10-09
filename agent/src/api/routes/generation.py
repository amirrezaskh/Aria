"""
Document generation API routes for resumes and cover letters.
"""

import os
from flask import Blueprint, request, jsonify
from src.workflows.workflows import Worlflows
from src.workflows.states import ResumeState, CoverLetterState
from src.database import db
from ..utils.file_helpers import validate_resume_file, resolve_resume_path

# Create blueprint for generation routes
generation_routes = Blueprint('generation', __name__, url_prefix='/api/generate')


@generation_routes.route('/', methods=['POST'])
def generate_resume_and_cover_letter():
    """Generate both resume and cover letter from job posting"""
    try:
        data = request.get_json()
        job_posting = data.get("jobDescription")
        company = data.get("companyName")
        position = data.get("positionTitle")

        # Validate required fields
        if not all([job_posting, company, position]):
            return jsonify({
                "status": "error",
                "message": "Missing required fields: jobDescription, companyName, positionTitle"
            }), 400

        # Save the job application to database with resume_generated = True
        try:
            job_id = db.save_job_application(company, position, job_posting, True)
            print(f"💾 Saved job application to database with ID: {job_id}")
        except Exception as e:
            print(f"⚠️ Failed to save job application: {e}")

        # Create ResumeState for workflow
        state = ResumeState(
            job_posting=job_posting,
            company=company,
            position=position,
            experiences="",
            skills="", 
            project_names=[],
            project_summaries="",
            highlights="",
            resume_latex="",
            tex_file=None,
            pdf_file=None,
            context=[],
            generation_metadata={}
        )

        # Execute workflow
        resume_cover_letter_workflow = Worlflows.create_resume_cover_letter_workflow()
        print(f"🚀 Generating resume and cover letter for {position} at {company}")
        result = resume_cover_letter_workflow.invoke(state)
        cwd = os.getcwd()
        print("🎁 Resume and cover letter created.")

        return jsonify({
            "status": "success",
            "resume_path": os.path.abspath(os.path.join(cwd, result["resume_pdf_file"])),
            "cover_letter_path": os.path.abspath(os.path.join(cwd, result["cover_letter_pdf_file"])),
            "job_id": job_id if 'job_id' in locals() else None
        })

    except Exception as e:
        print(f"❌ Error generating documents: {e}")
        return jsonify({
            "status": "error",
            "message": f"Failed to generate documents: {str(e)}"
        }), 500


@generation_routes.route('/cover-letter/', methods=['POST'])
def generate_cover_letter_only():
    """Generate only a cover letter using an existing resume"""
    try:
        data = request.get_json()
        job_posting = data.get("jobDescription")
        company = data.get("companyName")
        position = data.get("positionTitle")
        resume_pdf_file = data.get("resumePdfFile")

        # Validate required fields
        if not all([job_posting, company, position, resume_pdf_file]):
            return jsonify({
                "status": "error", 
                "message": "Missing required fields: jobDescription, companyName, positionTitle, resumePdfFile"
            }), 400

        # Resolve resume file path (handles URLs and local paths)
        resume_file_path = resolve_resume_path(resume_pdf_file)
        
        # Validate resume file exists
        if not validate_resume_file(resume_file_path):
            return jsonify({
                "status": "error",
                "message": f"Resume file not found: {resume_file_path}"
            }), 400

        # Save the job application to database with resume_generated = False (cover letter only)
        try:
            job_id = db.save_job_application(company, position, job_posting, False)
            print(f"💾 Saved cover letter job application to database with ID: {job_id}")
        except Exception as e:
            print(f"⚠️ Failed to save job application: {e}")

        # Create CoverLetterState
        state = CoverLetterState(
            job_posting=job_posting,
            company=company,
            position=position,
            resume_pdf_file=resume_file_path,  # Use the local file path
            resume="",
            cover_letter="",
            cover_letter_latex="",
            cover_letter_latex_file=None,
            cover_letter_pdf_file=None,
            context=[]
        )

        # Execute cover letter workflow
        cover_letter_workflow = Worlflows.create_cover_letter_worklflow()
        print(f"📝 Generating cover letter for {position} at {company}")
        result = cover_letter_workflow.invoke(state)
        cwd = os.getcwd()
        print("📄 Cover letter created.")

        return jsonify({
            "status": "success",
            "cover_letter_path": os.path.abspath(os.path.join(cwd, result["cover_letter_pdf_file"])),
            "resume_path": resume_pdf_file,  # Return the original URL for frontend use
            "job_id": job_id if 'job_id' in locals() else None
        })

    except Exception as e:
        print(f"❌ Error generating cover letter: {e}")
        return jsonify({
            "status": "error",
            "message": f"Failed to generate cover letter: {str(e)}"
        }), 500