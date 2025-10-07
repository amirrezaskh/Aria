import os
import signal
import concurrent.futures
from flask import Flask, request
from dotenv import load_dotenv
from src.chains.context_retrieval_chain import ContextRetrievalChain
from src.workflows.workflows import Worlflows
from src.workflows.states import ResumeState
from src.config.settings import settings
from flask_cors import CORS

port = 8080
load_dotenv()
executer = concurrent.futures.ThreadPoolExecutor(3)
app = Flask(__name__)
CORS(app)


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

@app.route("/exit/")
def exit_miner():
    os.kill(os.getpid(), signal.SIGTERM)


if __name__ == '__main__':
    app.run(host="localhost", port=port, debug=True)