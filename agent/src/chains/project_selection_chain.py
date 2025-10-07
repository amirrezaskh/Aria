import json
from ..workflows.states import ResumeState
from langchain.prompts import PromptTemplate
from typing import Dict, Any
from .base import BaseChain
from ..config.settings import settings
from ..config.prompts import PromptTemplates
from ..extractors.json_extractor import JSONExtractor


class ProjectSelectionChain(BaseChain):
    def get_prompt(self) -> PromptTemplate:
        return PromptTemplates.PROJECT_SELECTION_PROMPT

    def process_response(self, response: str) -> str:
        return JSONExtractor.extract_project_list(response)

    def load_projects_data(self) -> dict:
        with open(settings.projects_path, "r") as f:
            return json.load(f)

    def invoke(self, state: ResumeState) -> Dict[str, Any]:
        projects_data = self.load_projects_data()

        promptInputs = {
            "job": state["job_posting"],
            "projects": json.dumps(projects_data["projects"], indent=2)
        }

        result = super().invoke(promptInputs)

        return {
            "project_names": result["content"],
            "raw_response": result["raw_response"],
            "metadata": {
                "total_projects_available": len(projects_data["projects"])
            }
        }
