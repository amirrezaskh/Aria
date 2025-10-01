from langgraph.graph import StateGraph
from .states import ResumeState
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