import json
from ..workflows.states import ResumeState
from typing import Dict, Any
from .base import BaseChain
from ..config.settings import settings
from langchain.prompts import PromptTemplate
from ..config.prompts import PromptTemplates
from ..extractors.latex_extractor import LaTeXExtractor

class SkillsChain(BaseChain):
    def get_prompt(self) -> PromptTemplate:
        return PromptTemplates.SKILLS_PROMPT

    def process_response(self, response: str) -> str:
        return LaTeXExtractor.extract_skills(response)
    
    def load_skills_data(self) -> dict:
        with open(settings.skills_path, "r") as f:
            return json.load(f)
        
    def invoke(self, state: ResumeState) -> Dict[str, Any]:
        skills_data = self.load_skills_data()
        promptInputs = {
            "job": state["job_posting"],
            "skills": json.dumps(skills_data, indent=2)
        }

        result = super().invoke(promptInputs)

        return {
            "skills": result["content"],
            "raw_response": result["raw_response"]
        }

