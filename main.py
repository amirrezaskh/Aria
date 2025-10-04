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
Data Science (DS) 

Are you excited about taking your technical career to new heights with a full-time, W-2 role as a consultant in a dynamic and rapidly growing company? If you are, let's get in touch – your interest is the first step to starting the conversation. 



What This Role Requires: 

1-4 years of data analyst/ML/AI engineering work experience after your degree.
Must have experience with both Python programming & SQL language developer.
Should demonstrate experience developing end-to-end solutions.
Demonstrated SQL experience.
Additional experience with at least one: AWS, Azure or Databricks is preferred.
Additional experience with Pyspark, AWS S3, Lambda, EC2/AZ, Data bricks, Machine
learning (ML), GenAI/ Computer Vision, Theory of Probability, GitLab, R Programming, GCP & Airflow will be preferred.


To Qualify: 

You should be willing to relocate anywhere in the US on a client project-to-project basis, as this is an onsite, in-office position.
Strong English communication skills, both written and verbal.
Bachelor’s Degree in Computer Science, Information Systems, Electrical Engineering,
Mathematics, or a related quantitative field. Additional relevant Master’s degree is highly desirable for this role.


What’s In It For YOU? 

Gain valuable, career-enhancing experience working with our Fortune 1,000 clients.
Receive relocation support for training and project assignments, as required.
Enjoy comprehensive W2 employee benefits.
Access full coverage medical, dental, and vision insurance.
Qualify for 401K eligibility after one year of employment.
Benefit from basic life/AD&D and dependent disability (short/long term) coverage.


Who Are We? 

We are a premier IT consulting firm specializing in delivering top-tier Data Science solutions to companies across various sectors such as finance, energy, e-commerce, logistics, travel, retail, entertainment, automotive, and healthcare. Our clientele includes industry giants like Microsoft, Google, Johnson & Johnson, Fannie Mae, Walmart, PayPal, T-Mobile, McDonald's, CVS, Verizon, Charter, Nike, Dell, Wells Fargo, Capital One, and Charles Schwab, among many others. As a consultant, joining our team means you'll also have the opportunity to work with these renowned and leading companies and gain valuable, career-accelerating experience.


Company Highlights:

• Our Specialization: Providing IT consulting services.
• Experience: Over 25 years of combined domestic and international expertise in IT consulting serving hundreds of Fortune 1,000 and innovative startup clients.
    """

    company = "Tech Consulting"
    position = "Junior Data Scientist"

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