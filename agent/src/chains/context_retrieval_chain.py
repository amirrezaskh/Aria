import os
from glob import glob
from .base import BaseChain
from typing import List
from uuid import uuid4
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from ..workflows.states import ResumeState
from ..config.settings import settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader, JSONLoader
from typing import Dict, Any


class ContextRetrievalChain(BaseChain):
    def __init__(self):
        super().__init__()

        self.embeddings = OpenAIEmbeddings(
            model=settings.openai_embedding_model)
        self.vector_store = Chroma(
            collection_name="aria-vs",
            embedding_function=self.embeddings,
            host="localhost",
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            add_start_index=True,
        )

    def add_context(self, documents: List[Document]) -> None:
        splits = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(documents=splits)

    def add_papers(self) -> None:
        paths = glob(os.path.join(settings.papers_dir, "*.pdf"))
        for path in paths:
            loader = PyPDFLoader(path)
            documents = loader.load()
            self.add_context(documents)

    def add_projects(self) -> None:
        paths = glob(os.path.join(settings.papers_dir, "*.md"))
        for path in paths:
            loader = UnstructuredMarkdownLoader(path)
            documents = loader.load()
            self.add_context(documents)

    def add_transcripts(self) -> None:
        paths = glob(os.path.join(settings.transcripts_dir, "*.json"))
        for path in paths:
            loader = JSONLoader(
                file_path=path,
                jq_schema=".courses[]",
                text_content=False
            )
            documents = loader.load()
            self.add_context(documents)

    def retrieve_context(self, state: ResumeState) -> Dict[str, Any]:
        query_parts = []
    
        if state.get("job_posting"):
            job_excerpt = state["job_posting"][:500]
            query_parts.append(job_excerpt)

        if state.get("company"):
            query_parts.append(f"company: {state['company']}")

        if state.get("position"):
            query_parts.append(f"position: {state['position']}")

        try:
            if state.get("skills"):
                skills_text = state["skills"]
                query_parts.append(f"technical skills: {skills_text}")

            if state.get("experiences"):
                exp_text = state["experiences"][:300]
                query_parts.append(f"experience: {exp_text}")
        except:
            if state.get("resume"):
                resume_text = state["resume"]
                query_parts.append(f"resume: {resume_text}")

        query = " ".join(query_parts)

        retrieved_docs = self.vector_store.similarity_search(query, settings.num_docs)

        return {
            "context": retrieved_docs,
            "query_used": query
        }

    def get_prompt(self):
        return ""
    
    def process_response(self, response):
        return ""