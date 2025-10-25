from typing import Dict, Any
from ..workflows.states import ResumeState
from ..config.prompts import PromptTemplates
from langchain.prompts import PromptTemplate
from ..extractors.latex_extractor import LaTeXExtractor
from .base import BaseChain


class SummaryChain(BaseChain):
    def get_prompt(self) -> PromptTemplate:
        return PromptTemplates.SUMMARY_PROMPT

    def process_response(self, response: str) -> str:
        return LaTeXExtractor.extract_summary(response)

    def invoke(self, state: ResumeState) -> Dict[str, Any]:
        promptInputs = {
            "job": state["job_posting"],
            "experiences": state["experiences"],
            "skills": state["skills"],
            "projects": state["project_summaries"]
        }

        result = super().invoke(promptInputs)

        return {
            "summary": result["content"],
            "metadata": {
                "summary_length": len(result["content"])
            }
        }
