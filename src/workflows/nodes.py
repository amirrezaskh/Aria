from .states import ResumeState
from ..chains.experience_chain import ExperienceChain
from ..chains.skills_chain import SkillsChain
from ..chains.project_selection_chain import ProjectSelectionChain
from ..chains.project_summaries_chain import ProjectSummariesChain
from ..chains.highlight_chain import HighlightChain
from ..format.latex_formatter import LatexFormatter
from ..format.latex_compiler import LatexCompiler


class Nodes:
    @staticmethod
    def generate_experiences_node(state: ResumeState) -> ResumeState:
        print("📝 Generating experiences...")

        experience_chain = ExperienceChain()
        result = experience_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["experiences"] = result["experiences"]
        return state

    @staticmethod
    def generate_skills_node(state: ResumeState) -> ResumeState:
        print("📝 Generating experiences...")

        skills_chain = SkillsChain()
        result = skills_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["skills"] = result["skills"]
        return state

    @staticmethod
    def select_projects_node(state: ResumeState) -> ResumeState:
        print("📝 Selecting projects...")

        project_selection_chain = ProjectSelectionChain()
        result = project_selection_chain.invoke({
            "job_posting": state["job_posting"]
        })

        state["project_names"] = result["project_names"]
        return state

    @staticmethod
    def generate_project_summaries_node(state: ResumeState) -> ResumeState:
        print("📝 Summarizing projects...")

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
        resume_latex = LatexFormatter.format_resume(
            highlights=state["highlights"],
            experiences=state["experiences"],
            skills=state["skills"],
            projects=state["project_summaries"]
        )
        output_dir = f"./output/resumes/{state['company']}"
        latex_filename = f"{state['position']}.tex"
        result = LatexCompiler.compile_latex(resume_latex, output_dir, latex_filename)
        state["resume_latex"] = resume_latex
        state["latex_file"] = result["latex_file"]
        state["pdf_file"] = result["pdf_file"]

