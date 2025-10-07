"""Base chain class for resume generation components"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from ..workflows.states import ResumeState
from ..config.settings import settings


class BaseChain(ABC):
    """Abstract base class for all resume generation chains"""
    
    def __init__(self):
        self.llm = init_chat_model(
            settings.openai_model, 
            model_provider="openai"
        )
    
    @abstractmethod
    def get_prompt(self) -> PromptTemplate:
        """Return the prompt template for this chain"""
        pass
    
    @abstractmethod
    def process_response(self, response: str) -> str:
        """Process the LLM response and extract relevant content"""
        pass
    
    def invoke(self, state: ResumeState) -> Dict[str, Any]:
        """Execute the chain with given inputs"""
        prompt = self.get_prompt()
        messages = prompt.invoke(state)
        response = self.llm.invoke(messages)
        processed_content = self.process_response(response.content)
        
        return {
            "content": processed_content,
            "raw_response": response.content,
            "inputs": state
        }