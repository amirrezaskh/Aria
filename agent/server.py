import os
import signal
import concurrent.futures
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from src.chains.context_retrieval_chain import ContextRetrievalChain
from src.workflows.workflows import Worlflows
from src.workflows.states import ResumeState, CoverLetterState
from src.config.settings import settings
from flask_cors import CORS
from src.database import db

port = 8080
load_dotenv()
executer = concurrent.futures.ThreadPoolExecutor(3)
app = Flask(__name__)
CORS(app)


@app.route("/api/db/test", methods=['GET'])
def test_database():
    """Test database connection"""
    try:
        if db.test_connection():
            return jsonify({"status": "success", "message": "Database connected successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to connect to database"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/db/init", methods=['POST'])
def initialize_database():
    """Initialize database schema"""
    try:
        if db.initialize_schema():
            return jsonify({"status": "success", "message": "Database schema initialized successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to initialize database schema"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/jobs/save", methods=['POST'])
def save_job_application():
    """Save a new job application"""
    try:
        data = request.get_json()
        company_name = data.get('companyName')
        position_title = data.get('positionTitle')
        job_description = data.get('jobDescription')
        resume_generated = data.get('resumeGenerated', False)
        
        if not all([company_name, position_title, job_description]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        job_id = db.save_job_application(company_name, position_title, job_description, resume_generated)
        
        if job_id:
            return jsonify({
                "status": "success", 
                "message": "Job application saved successfully",
                "job_id": job_id
            })
        else:
            return jsonify({"status": "error", "message": "Failed to save job application"}), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/jobs/similar", methods=['POST'])
def find_similar_jobs():
    """Find similar job applications using vector embeddings"""
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        position_title = data.get('position_title') 
        job_description = data.get('job_description')
        threshold = data.get('threshold', 0.75)  # Default 75% similarity
        
        if not all([company_name, position_title, job_description]):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        similar_jobs = db.find_similar_jobs(company_name, position_title, job_description, threshold)
        
        return jsonify({
            "status": "success",
            "similar_jobs": similar_jobs,
            "count": len(similar_jobs),
            "threshold": threshold,
            "method": "vector_embeddings"
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/jobs/backfill", methods=['POST'])
def backfill_embeddings():
    """Generate embeddings for existing jobs that don't have them"""
    try:
        if db.backfill_embeddings():
            return jsonify({"status": "success", "message": "Embeddings backfilled successfully"})
        else:
            return jsonify({"status": "error", "message": "Failed to backfill embeddings"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/jobs/all", methods=['GET'])
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
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/context/", methods=['POST'])
def setup_vector_store():
    print("🚀 Setting up vector store...")
    context_chain = ContextRetrievalChain()
    
    # Add papers
    if os.path.exists(settings.papers_dir):
        print("📄 Adding papers...")
        context_chain.add_papers()
    
    # Add projects
    if os.path.exists(settings.projects_dir):
        print("🔧 Adding projects...")
        context_chain.add_projects()
    
    # Add transcripts
    if os.path.exists(settings.transcripts_dir):
        print("📝 Adding transcripts...")
        context_chain.add_transcripts()

@app.route("/api/generate/", methods=["POST"])
def generate():
    job_posting = request.get_json()["jobDescription"]
    company = request.get_json()["companyName"]
    position = request.get_json()["positionTitle"]

    # Save the job application to database with resume_generated = True
    try:
        job_id = db.save_job_application(company, position, job_posting, True)
        print(f"💾 Saved job application to database with ID: {job_id}")
    except Exception as e:
        print(f"⚠️ Failed to save job application: {e}")

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

    resume_cover_letter_workflow = Worlflows.create_resume_cover_letter_workflow()
    print(f"🚀 Generating resume and cover letter for {position} at {company}")
    result = resume_cover_letter_workflow.invoke(state)
    cwd = os.getcwd()
    print("🎁 Resume and cover letter created.")

    return {
        "resume_path": os.path.abspath(os.path.join(cwd, result["resume_pdf_file"])),
        "cover_letter_path": os.path.abspath(os.path.join(cwd, result["cover_letter_pdf_file"]))
    }

@app.route("/api/generate/cover-letter/", methods=["POST"])
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

        # Check if resume file exists
        resume_file_path = resume_pdf_file
        
        # If it's an API URL, convert to local path
        if resume_pdf_file.startswith("http://localhost:8080/api/resumes/generated/"):
            from urllib.parse import unquote
            # Extract the path part after the API endpoint
            path_part = resume_pdf_file.replace("http://localhost:8080/api/resumes/generated/", "")
            decoded_path = unquote(path_part)
            resume_file_path = os.path.join(os.getcwd(), 'output', 'resumes', decoded_path)
        elif resume_pdf_file.startswith("http://localhost:8080/api/resumes/preview/"):
            # Handle template preview URLs
            template_id = resume_pdf_file.replace("http://localhost:8080/api/resumes/preview/", "")
            template_files = {
                'ml-engineering': 'data/resumes/Resume - ML - New.pdf',
                'data-science': 'data/resumes/Resume - DS.pdf',
                'software-engineering': 'data/resumes/Resume - SWE - New.pdf',
                'overall': 'data/resumes/Resume - OverAll.pdf'
            }
            if template_id in template_files:
                resume_file_path = os.path.join(os.getcwd(), template_files[template_id])
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Unknown template: {template_id}"
                }), 400
        
        if not os.path.exists(resume_file_path):
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

@app.route("/api/resumes/preview/<template_id>", methods=['GET'])
def preview_resume_template(template_id):
    """Serve resume template PDFs for preview"""
    try:
        # Mapping of template IDs to file paths
        resume_files = {
            'ml-engineering': 'data/resumes/Resume - ML - New.pdf',
            'data-science': 'data/resumes/Resume - DS.pdf',
            'software-engineering': 'data/resumes/Resume - SWE - New.pdf',
            'overall': 'data/resumes/Resume - OverAll.pdf'
        }
        
        if template_id not in resume_files:
            return jsonify({"status": "error", "message": "Template not found"}), 404
        
        resume_path = resume_files[template_id]
        full_path = os.path.join(os.getcwd(), resume_path)
        
        if not os.path.exists(full_path):
            return jsonify({"status": "error", "message": "Resume file not found"}), 404
        
        from flask import send_file
        return send_file(full_path, mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/resumes/generated/<path:resume_path>", methods=['GET'])
def serve_generated_resume(resume_path):
    """Serve generated resume PDFs from the output directory"""
    try:
        from urllib.parse import unquote
        
        # URL decode and sanitize the path to prevent directory traversal attacks
        decoded_path = unquote(resume_path)
        safe_path = decoded_path.replace('..', '').strip('/')
        
        # Construct full path to the resume file
        full_path = os.path.join(os.getcwd(), 'output', 'resumes', safe_path)
        
        if not os.path.exists(full_path):
            return jsonify({"status": "error", "message": "Resume file not found"}), 404
        
        # Verify it's actually a PDF file
        if not full_path.endswith('.pdf'):
            return jsonify({"status": "error", "message": "Invalid file type"}), 400
        
        from flask import send_file
        return send_file(full_path, mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/exit/")
def exit_miner():
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)