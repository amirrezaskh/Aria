"""Experience generation chain"""

import json
from typing import Dict, Any
from langchain.prompts import PromptTemplate

from .base import BaseChain
from ..config.prompts import PromptTemplates
from ..config.settings import settings
from ..extractors.latex_extractor import LaTeXExtractor


class ExperienceChain(BaseChain):
    """Chain for generating tailored professional experiences"""
    
    def get_prompt(self) -> PromptTemplate:
        """Return the experience generation prompt"""
        return PromptTemplates.EXPERIENCE_PROMPT
    
    def process_response(self, response: str) -> str:
        """Extract LaTeX experience content from response"""
        return LaTeXExtractor.extract_experiences(response)
    
    def load_experiences_data(self) -> dict:
        """Load experiences data from JSON file"""
        with open(settings.experiences_path, "r") as f:
            return json.load(f)
    
    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate experiences based on job posting"""
        # Load experiences data
        experiences_data = self.load_experiences_data()
        
        # Prepare inputs for the prompt
        prompt_inputs = {
            "job": inputs["job_posting"],
            "experiences": json.dumps(experiences_data["experiences"], indent=2)
        }
        
        # Execute the chain
        result = super().invoke(prompt_inputs)
        
        return {
            "experiences": result["content"],
            "raw_response": result["raw_response"],
            "metadata": {
                "total_experiences_available": len(experiences_data["experiences"]),
                "job_posting_length": len(inputs["job_posting"])
            }
        }