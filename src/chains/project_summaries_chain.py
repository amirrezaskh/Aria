import json
from langchain.prompts import PromptTemplate
from typing import Dict, Any, List
from .base import BaseChain
from ..config.settings import settings
from ..config.prompts import PromptTemplates
from ..extractors.latex_extractor import LaTeXExtractor

class ProjectSummariesChain(BaseChain):
    def get_prompt(self) -> PromptTemplate:
        return PromptTemplates.PROJECT_SUMMARY_PROMPT
    
    def process_response(self, response : str) -> str:
        return LaTeXExtractor.extract_projects(response)
    
    def load_projects_data(self) -> dict:
        with open(settings.projects_path, "r") as f:
            return json.load(f)

    def load_project_context(self, project_name : str, projects_data : List[dict]) -> dict:
        project_info = None
        for project in projects_data:
            if project["title"] == project_name:
                project_info = project
                break

        project_docs = ""
        try:
            readme_path = project_info.get("readme", "")
            if readme_path:
                # Convert relative path to absolute path from data directory
                file_path = f"{settings.data_dir}/{readme_path}" if not readme_path.startswith(
                    "{settings.data_dir}/") else readme_path
                with open(file_path, "r") as f:
                    project_docs = f.read()

        except Exception:
            pass

        return {
            "title": project_info["title"],
            "description": project_info["description"],
            "stack": project_info["stack"],
            "documentation": project_docs,
            "github": project_info["github"]
        }

    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        project_data = self.load_projects_data()
        project_names = inputs["project_names"]
        project_summaries = []
        for project_name in project_names:
            project_context = self.load_project_context(project_name, project_data["projects"])

            promptInputs = {
                "job": inputs["job_posting"],
                "project_title": project_context["title"],
                "project_description": project_context["description"],
                "project_stack": ", ".join(project_context["stack"]),
                "project_docs": project_context["documentation"][:3000],
                "github": project_context["github"],
            }

            result = super().invoke(promptInputs)

            project_summaries.append(result["content"])
        
        combined_summaries = "\n\n".join(project_summaries)
        return {
            "project_summaries": combined_summaries,
            "metadata": {
                "total_projects_length": len(combined_summaries)
            }
        }