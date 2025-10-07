from langgraph.graph import StateGraph
from .states import ResumeState, CoverLetterState
from .nodes import Nodes


class Worlflows:
    def create_resume_workflow():
        workflow = StateGraph(ResumeState)

        workflow.add_node("generate_experiences", Nodes.generate_experiences_node)
        workflow.add_node("generate_skills", Nodes.generate_skills_node)
        workflow.add_node("select_projects", Nodes.select_projects_node)
        workflow.add_node("generate_project_summaries", Nodes.generate_project_summaries_node)
        workflow.add_node("generate_highlights", Nodes.generate_highlights_node)
        workflow.add_node("save_resume", Nodes.save_resume_node)

        workflow.set_entry_point("generate_experiences")
        workflow.add_edge("generate_experiences", "generate_skills")
        workflow.add_edge("generate_skills", "select_projects")
        workflow.add_edge("select_projects", "generate_project_summaries")
        workflow.add_edge("generate_project_summaries", "generate_highlights")
        workflow.add_edge("generate_highlights", "save_resume")
        workflow.set_finish_point("save_resume")

        return workflow.compile()
    
    def create_resume_cover_letter_workflow():
        workflow = StateGraph(ResumeState)

        workflow.add_node("generate_experiences", Nodes.generate_experiences_node)
        workflow.add_node("generate_skills", Nodes.generate_skills_node)
        workflow.add_node("select_projects", Nodes.select_projects_node)
        workflow.add_node("generate_project_summaries", Nodes.generate_project_summaries_node)
        workflow.add_node("generate_highlights", Nodes.generate_highlights_node)
        workflow.add_node("save_resume", Nodes.save_resume_node)
        workflow.add_node("retrieve_context", Nodes.retrieve_context_node)
        workflow.add_node("generate_cover_letter", Nodes.generate_cover_letter_node)
        workflow.add_node("save_cover_letter", Nodes.save_cover_letter_node)
        workflow.add_node("add_cover_letter_context", Nodes.add_cover_letter_context_node)

        workflow.set_entry_point("generate_experiences")
        workflow.add_edge("generate_experiences", "generate_skills")
        workflow.add_edge("generate_skills", "select_projects")
        workflow.add_edge("select_projects", "generate_project_summaries")
        workflow.add_edge("generate_project_summaries", "generate_highlights")
        workflow.add_edge("generate_highlights", "save_resume")
        workflow.add_edge("save_resume", "retrieve_context")
        workflow.add_edge("retrieve_context", "generate_cover_letter")
        workflow.add_edge("generate_cover_letter", "save_cover_letter")
        workflow.add_edge("save_cover_letter", "add_cover_letter_context")
        workflow.set_finish_point("add_cover_letter_context")

        return workflow.compile()
    
    def create_cover_letter_worklflow():
        workflow = StateGraph(CoverLetterState)

        workflow.add_node("load_resume", Nodes.load_resume_node)
        workflow.add_node("retrieve_context_only_cover_letter", Nodes.retrieve_context_only_cover_letter_node)
        workflow.add_node("generate_only_cover_letter", Nodes.generate_only_cover_letter_node)
        workflow.add_node("save_cover_letter", Nodes.save_cover_letter_node)
        workflow.add_node("add_cover_letter_context", Nodes.add_cover_letter_context_node)

        workflow.set_entry_point("load_resume")
        workflow.add_edge("load_resume", "retrieve_context_only_cover_letter")
        workflow.add_edge("retrieve_context_only_cover_letter", "generate_only_cover_letter")
        workflow.add_edge("generate_only_cover_letter", "save_cover_letter")
        workflow.add_edge("save_cover_letter", "add_cover_letter_context")
        workflow.set_finish_point("add_cover_letter_context")

        return workflow.compile()