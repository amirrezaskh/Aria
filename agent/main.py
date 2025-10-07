"""
Refactored main.py using industry-standard LangChain project structure

This demonstrates how to use the modular architecture for cleaner,
more maintainable code.
"""

from dotenv import load_dotenv
from src.chains.context_retrieval_chain import ContextRetrievalChain
from src.workflows.workflows import Worlflows
from src.workflows.states import ResumeState
from src.config.settings import settings
import os

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

def main():
    """Main execution function demonstrating the new architecture"""
    load_dotenv()
    
    # Sample job posting
    job_posting = """
About the job
Job Title: Power BI Developer (Entry-Level to 3 Years Experience)

Location: Downtown Toronto (Hybrid/Flexible Work Environment)

Employment Type: Full-Time | Entry-Level to Junior

 Experience Required: Graduate to 1–3 Years



About the Role

We are on the lookout for a Power BI Developer who has a passion for building engaging, insightful dashboards and wants to grow their career as part of a collaborative, data-driven team. Whether you're a recent graduate or have up to 3 years of experience, this is a great opportunity to expand your skills in a supportive environment with real impact.
You’ll be working closely with data analysts, engineers, and business stakeholders to turn data into meaningful insights through visually compelling Power BI dashboards.


Key Responsibilities

Design, develop, and maintain Power BI dashboards and reports based on business requirements
Collaborate with data teams to understand data structures and ensure accurate reporting
Transform raw data into clean, organized models using Power BI’s data modeling tools
Translate business questions into metrics, KPIs, and visualizations that support decision-making
Perform data validation and ensure reporting accuracy
Continuously optimize dashboards for performance and usability
Stay current with Power BI updates and best practices


What We're Looking For

0–3 years of experience working with Power BI (internships or academic projects welcome!)
Strong skills in data visualization, dashboard creation, and report design
Basic knowledge of DAX and Power Query (M)
Familiarity with data modeling and working with relational databases (SQL knowledge a plus)
A passion for working with data and communicating insights
Strong problem-solving skills and a collaborative mindset
Excellent communication skills – ability to work with both technical and non-technical teams


Nice to Have (but not required)

Experience working in a business intelligence or analytics environment
Exposure to other BI tools (e.g., Tableau, Looker)
Understanding of data warehousing concepts
Experience working in an agile or team-based setting
"""

    company = "Dexian"
    position = "Junior BI developer"

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
    
    setup_vector_store()

    # resume_workflow = Worlflows.create_resume_workflow()
    resume_cover_letter_workflow = Worlflows.create_resume_cover_letter_workflow()

    print(f"🚀 Generating resume and cover letter for {position} at {company}")
    resume_cover_letter_workflow.invoke(state)
    print("🎁 Resume and cover letter created.")


if __name__ == "__main__":
    main()