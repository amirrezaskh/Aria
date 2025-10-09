"""
Context and vector store management API routes.
"""

import os
from flask import Blueprint, jsonify
from src.chains.context_retrieval_chain import ContextRetrievalChain
from src.config.settings import settings

# Create blueprint for context routes
context_routes = Blueprint('context', __name__, url_prefix='/api/context')


@context_routes.route('/', methods=['POST'])
def setup_vector_store():
    """Setup and populate the vector store with documents"""
    try:
        print("🚀 Setting up vector store...")
        context_chain = ContextRetrievalChain()
        
        setup_results = {
            "papers": False,
            "projects": False,
            "transcripts": False,
            "errors": []
        }
        
        # Add papers
        if os.path.exists(settings.papers_dir):
            try:
                print("📄 Adding papers...")
                context_chain.add_papers()
                setup_results["papers"] = True
            except Exception as e:
                setup_results["errors"].append(f"Papers: {str(e)}")
        
        # Add projects
        if os.path.exists(settings.projects_dir):
            try:
                print("🔧 Adding projects...")
                context_chain.add_projects()
                setup_results["projects"] = True
            except Exception as e:
                setup_results["errors"].append(f"Projects: {str(e)}")
        
        # Add transcripts
        if os.path.exists(settings.transcripts_dir):
            try:
                print("📝 Adding transcripts...")
                context_chain.add_transcripts()
                setup_results["transcripts"] = True
            except Exception as e:
                setup_results["errors"].append(f"Transcripts: {str(e)}")

        # Determine overall status
        if any([setup_results["papers"], setup_results["projects"], setup_results["transcripts"]]):
            status = "success" if not setup_results["errors"] else "partial_success"
            message = "Vector store setup completed successfully"
            if setup_results["errors"]:
                message += f" with {len(setup_results['errors'])} errors"
        else:
            status = "error"
            message = "Failed to setup vector store - no documents processed"

        return jsonify({
            "status": status,
            "message": message,
            "results": setup_results
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Vector store setup failed: {str(e)}"
        }), 500


@context_routes.route('/status', methods=['GET'])
def get_vector_store_status():
    """Get the current status of the vector store"""
    try:
        status_info = {
            "papers_dir_exists": os.path.exists(settings.papers_dir),
            "projects_dir_exists": os.path.exists(settings.projects_dir),
            "transcripts_dir_exists": os.path.exists(settings.transcripts_dir),
            "papers_count": 0,
            "projects_count": 0,
            "transcripts_count": 0
        }
        
        # Count files in each directory
        if status_info["papers_dir_exists"]:
            status_info["papers_count"] = len([f for f in os.listdir(settings.papers_dir) 
                                               if f.endswith('.pdf')])
        
        if status_info["projects_dir_exists"]:
            status_info["projects_count"] = len([f for f in os.listdir(settings.projects_dir) 
                                                if os.path.isdir(os.path.join(settings.projects_dir, f))])
        
        if status_info["transcripts_dir_exists"]:
            status_info["transcripts_count"] = len([f for f in os.listdir(settings.transcripts_dir)
                                                   if f.endswith(('.txt', '.md'))])
        
        return jsonify({
            "status": "success",
            "vector_store_status": status_info
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500