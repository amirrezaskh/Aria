"""Settings and configuration management for Aria"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o", env="OPENAI_MODEL") 
    openai_embedding_model: str = Field("text-embedding-3-large", env="OPENAI_EMBEDDING_MODEL")
    
    # TODO: We can probably delete this.
    # LangChain Configuration
    langchain_tracing_v2: bool = Field(False, env="LANGCHAIN_TRACING_V2")
    langchain_api_key: Optional[str] = Field(None, env="LANGCHAIN_API_KEY")
    
    # Application Configuration
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    max_retries: int = Field(3, env="MAX_RETRIES")
    num_docs: int = Field(8, env="NUM_DOCS")
    
    # File Paths
    data_dir: str = Field("./data", env="DATA_DIR")
    output_dir: str = Field("./output", env="OUTPUT_DIR")
    papers_dir: str = Field("./data/papers", env="PAPERS_DIR")
    projects_dir: str = Field("./data/projects", env="PROJECTS_DIR")
    transcripts_dir: str = Field("./data/transcripts", env="TRANSCRIPTS_DIR")
    resumes_dir: str = Field("./output/resumes", env="RESUMES_DIR")
    cover_letters_dir: str = Field("./output/cover_letters", env="COVER_LETTERS_DIR")

    experiences_file: str = Field("experiences.json", env="EXPERIENCES_FILE")
    skills_file: str = Field("technical_skills.json", env="SKILLS_FILE")
    projects_file: str = Field("projects.json", env="PROJECTS_FILE")
    
    # Resume Configuration
    default_target_pages: int = Field(2, env="DEFAULT_TARGET_PAGES")
    max_experiences: int = Field(4, env="MAX_EXPERIENCES")
    max_projects: int = Field(5, env="MAX_PROJECTS")
    max_highlights: int = Field(7, env="MAX_HIGHLIGHTS")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def experiences_path(self) -> str:
        return os.path.join(self.data_dir, self.experiences_file)
    
    @property 
    def skills_path(self) -> str:
        return os.path.join(self.data_dir, self.skills_file)
    
    @property
    def projects_path(self) -> str:
        return os.path.join(self.data_dir, self.projects_file)


# Global settings instance
settings = Settings()