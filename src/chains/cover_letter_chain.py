from .base import BaseChain
from ..config.prompts import PromptTemplates
from langchain.prompts import PromptTemplate
from ..extractors.latex_extractor import LaTeXExtractor
from ..workflows.states import ResumeState
from typing import Dict, Any

class CoverLetterChain(BaseChain):
    def get_prompt(self) -> PromptTemplate:
        return PromptTemplates.COVER_LETTER_PROMPT
    
    def process_response(self, response: str) -> str:
        return LaTeXExtractor.extract_cover_letter(response)
    
    def invoke(self, state: ResumeState) -> Dict[str, Any]:
        promptInputs = {
            "position": state["position"],
            "company": state["company"],
            "job_posting": state["job_posting"],
            "resume_highlights": state["highlights"],
            "resume_experiences": state["experiences"],
            "resume_skills": state["skills"],
            "resume_projects": state["project_summaries"],
            "retrieved_context": state["context"]
        }

        result = super().invoke(promptInputs)
        return {
            "cover_letter_tex": result['content'],
            "metadata": {
                "cover_letter_length": len(result['content'])
            } 
        }