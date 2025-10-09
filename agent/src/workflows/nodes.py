from .states import ResumeState, CoverLetterState
from ..format.latex_formatter import LatexFormatter
from ..format.latex_compiler import LatexCompiler
from ..config.settings import settings
from langchain.docstore.document import Document
from pypdf import PdfReader
from ..database import db

class Nodes:
    @staticmethod
    def generate_experiences_node(state: ResumeState) -> ResumeState:
        print("📝 Generating experiences...")

        from ..chains.experience_chain import ExperienceChain
        experience_chain = ExperienceChain()
        result = experience_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["experiences"] = result["experiences"]
        return state

    @staticmethod
    def generate_skills_node(state: ResumeState) -> ResumeState:
        print("📝 Generating skills...")

        from ..chains.skills_chain import SkillsChain
        skills_chain = SkillsChain()
        result = skills_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["skills"] = result["skills"]
        return state

    @staticmethod
    def select_projects_node(state: ResumeState) -> ResumeState:
        print("📝 Selecting projects...")

        from ..chains.project_selection_chain import ProjectSelectionChain
        project_selection_chain = ProjectSelectionChain()
        result = project_selection_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["project_names"] = result["project_names"]
        return state

    @staticmethod
    def generate_project_summaries_node(state: ResumeState) -> ResumeState:
        print("📝 Summarizing projects...")

        from ..chains.project_summaries_chain import ProjectSummariesChain
        project_summaries_chain = ProjectSummariesChain()
        result = project_summaries_chain.invoke({
            "job_posting": state["job_posting"],
            "project_names": state["project_names"]
        })

        state["project_summaries"] = result["project_summaries"]
        return state

    @staticmethod
    def generate_highlights_node(state: ResumeState) -> ResumeState:
        print("📝 Generating highlights...")

        from ..chains.highlight_chain import HighlightChain
        highlight_chain = HighlightChain()
        result = highlight_chain.invoke({
            "job_posting": state["job_posting"],
            "experiences": state["experiences"],
            "skills": state["skills"],
            "project_summaries": state["project_summaries"]
        })
        state["highlights"] = result["highlights"]
        return state

    @staticmethod
    def save_resume_node(state: ResumeState) -> ResumeState:
        print("✅ Saving resume...")
        resume_latex = LatexFormatter.format_resume(
            highlights=state["highlights"],
            experiences=state["experiences"],
            skills=state["skills"],
            projects=state["project_summaries"]
        )
        output_dir = f"{settings.resumes_dir}/{state['company']}"
        latex_filename = f"{state['position']}.tex"
        result = LatexCompiler.compile_latex(
            resume_latex, output_dir, latex_filename)
        state["resume_latex"] = resume_latex
        state["resume_latex_file"] = result["latex_file"]
        state["resume_pdf_file"] = result["pdf_file"]
        return state

    @staticmethod
    def retrieve_context_node(state: ResumeState) -> ResumeState:
        print("🔎 Retrieving context...")
        from ..chains.context_retrieval_chain import ContextRetrievalChain
        context_retrieval_chain = ContextRetrievalChain()
        result = context_retrieval_chain.retrieve_context({
            "job_posting": state["job_posting"],
            "company": state["company"],
            "position": state["position"],
            "skills": state["skills"],
            "experiences": state["experiences"]
        })
        state["context"] = result["context"]
        return state

    @staticmethod
    def generate_cover_letter_node(state: ResumeState) -> ResumeState:
        print("📝 Generating cover letter...")
        from ..chains.cover_letter_chain import CoverLetterChain
        cover_letter_chain = CoverLetterChain()
        result = cover_letter_chain.invoke({
            "position": state["position"],
            "company": state["company"],
            "job_posting": state["job_posting"],
            "highlights": state["highlights"],
            "experiences": state["experiences"],
            "skills": state["skills"],
            "project_summaries": state["project_summaries"],
            "context": state["context"]
        })
        state["cover_letter"] = result["cover_letter_tex"]
        return state

    @staticmethod
    def save_cover_letter_node(state: ResumeState) -> ResumeState:
        cover_letter_latex = LatexFormatter.format_cover_letter(
            position=state["position"],
            company=state["company"],
            cover_letter=state["cover_letter"]
        )
        output_dir = f"{settings.cover_letters_dir}/{state['company']}"
        latex_filename = f"{state['position']}.tex"
        result = LatexCompiler.compile_latex(
            cover_letter_latex, output_dir, latex_filename)
        state["cover_letter_latex"] = cover_letter_latex
        state["cover_letter_latex_file"] = result["latex_file"]
        state["cover_letter_pdf_file"] = result["pdf_file"]
        return state

    @staticmethod
    def add_cover_letter_context_node(state: ResumeState) -> ResumeState:
        from ..chains.context_retrieval_chain import ContextRetrievalChain
        context_retrieval_chain = ContextRetrievalChain()
        document = Document(
            page_content=state["cover_letter"],
            metadata={
                "source": "cover letter",
                "position": state["position"],
                "company": state["company"]
            })
        context_retrieval_chain.add_context([document])
        return state
    

    @staticmethod
    def load_resume_node(state: CoverLetterState):
        reader = PdfReader(state["resume_pdf_file"])
        resume = ""
        for page in reader.pages:
            resume += page.extract_text()
        state["resume"] = resume
        
        return state
    
    @staticmethod
    def retrieve_context_only_cover_letter_node(state: CoverLetterState) -> CoverLetterState:
        print("🔎 Retrieving context...")
        from ..chains.context_retrieval_chain import ContextRetrievalChain
        context_retrieval_chain = ContextRetrievalChain()
        result = context_retrieval_chain.retrieve_context({
            "job_posting": state["job_posting"],
            "company": state["company"],
            "position": state["position"],
            "resume": state["resume"],
        })
        state["context"] = result["context"]
        return state

    @staticmethod
    def generate_only_cover_letter_node(state: CoverLetterState):
        print("📝 Generating cover letter...")
        from ..chains.cover_letter_chain import CoverLetterChain
        cover_letter_chain = CoverLetterChain(withResume=False)
        result = cover_letter_chain.invoke({
            "position": state["position"],
            "company": state["company"],
            "job_posting": state["job_posting"],
            "resume": state["resume"],
            "context": state["context"]
        })
        state["cover_letter"] = result["cover_letter_tex"]
        return state
    
    @staticmethod
    def save_job_application_node(state: CoverLetterState | ResumeState):
        """Save job application to database with vector embeddings"""
        print("💾 Saving job application to database...")
        
        company_name = state.get("company", "")
        position_title = state.get("position", "")
        job_posting = state.get("job_posting", "")
        
        # Check if this is a ResumeState by looking for keys unique to ResumeState
        resume_generated = "resume_latex" in state or "experiences" in state
        
        db.save_job_application(
            company_name=company_name,
            position_title=position_title,
            job_description=job_posting,
            resume_generated=resume_generated
        )
        return state