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
    We are on the hunt for passionate developers ready to design and implement efficient APIs and subsystems that enhance every aspect of our system. While your main focus will be tackling data-driven challenges, your versatility will shine as you collaborate on dev-ops and front-end tasks whenever needed.


Alert Labs HVAC team is a small and innovative division within the company. Reporting to the VP, your contributions will cover a wide range of ideas and technology. Join us if you thrive in a dynamic environment and are eager to contribute to a team dedicated to delivering industry-leading products. If you’re enthusiastic, engaged, and ready to make an impact, we want to hear from you!


Responsibilities:

Take ownership for successfully executing software tasks and projects given higher-level requirements or scope
Design small modules following SOLID and other design principles
Select, adapt, and apply appropriate algorithms
Collaborate with other team members and stakeholders to clarify requirements
Get the project done, hands-on and with other team members
Analyze problems and synthesize solutions applying both technical skill and consideration of the business case


Must Haves:
At least 3 years of professional software development experience
Undergraduate degree in Software Engineering, Computer Science, or equivalent experience
Experience developing software in Python or Typescript
Experience with dev-ops: Jenkins, AWS, Bitbucket, Kafka
Excellent computer science fundamentals including data structures and algorithms, databases, and/or distributed systems
A track record of success delivering complex software projects
Ability to communicate effectively with people in different roles. You are open to learning and mentoring.


Nice to Haves:
Data Science experience
Experience with Node.js, React, Dart/Flutter or a lower-level language such as C++
Experience or introductory course in Machine Learning or Data Science
    """

    company = "Alert Labs Inc."
    position = "Software Developer"

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
    
    # setup_vector_store()

    # resume_workflow = Worlflows.create_resume_workflow()
    resume_cover_letter_workflow = Worlflows.create_resume_cover_letter_workflow()

    print(f"🚀 Generating resume and cover letter for {position} at {company}")
    resume_cover_letter_workflow.invoke(state)
    print("🎁 Resume and cover letter created.")


if __name__ == "__main__":
    main()