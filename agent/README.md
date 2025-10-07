# Aria - AI-Powered Resume & Cover Letter Generator

Aria is an intelligent resume and cover letter generation system that leverages LangChain, LangGraph, and RAG (Retrieval Augmented Generation) to create personalized, job-specific documents. The system analyzes job postings and automatically tailors resumes and cover letters using your personal knowledge base of papers, projects, experiences, and previous applications.

## 🚀 Features

- **Intelligent Resume Generation**: Automatically selects and formats the most relevant experiences, skills, and projects for each job
- **Personalized Cover Letters**: Generates compelling cover letters using retrieved context from your knowledge base
- **RAG-Enhanced Content**: Uses vector search to find relevant content from your papers, projects, and experiences
- **LaTeX Output**: Produces professional, publication-ready PDFs
- **Modular Architecture**: Built with industry-standard LangChain patterns for maintainability and extensibility
- **LangGraph Workflows**: Orchestrates complex multi-step generation processes
- **Vector Store Integration**: ChromaDB for efficient similarity search

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [License](#license)

## 🔧 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- LaTeX distribution (for PDF generation)
- ChromaDB

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/amirrezaskh/Aria.git
   cd Aria
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Required Environment Variables**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   OPENAI_EMBEDDING_MODEL=text-embedding-3-large
   
   # Optional configurations
   CHUNK_SIZE=1000
   CHUNK_OVERLAP=200
   NUM_DOCS=8
   ```

5. **Setup Data Directory Structure**
   ```bash
   mkdir -p data/{papers,projects,transcripts}
   mkdir -p output/{resumes,cover_letters}
   ```

## 🚀 Quick Start

### 1. Setup Vector Store (One-time)

First, populate your knowledge base:

```python
from src.chains.context_retrieval_chain import ContextRetrievalChain

def setup_vector_store():
    context_chain = ContextRetrievalChain()
    
    # Add your papers (PDFs)
    context_chain.add_papers()
    
    # Add project documentation (Markdown)
    context_chain.add_projects()
    
    # Add transcripts (JSON)
    context_chain.add_transcripts()

setup_vector_store()
```

### 2. Generate Resume and Cover Letter

```python
from dotenv import load_dotenv
from src.workflows.workflows import Workflows
from src.workflows.states import ResumeState

load_dotenv()

# Create initial state
state = ResumeState(
    job_posting="Your job posting here...",
    company="Company Name",
    position="Position Title",
    experiences="",
    skills="", 
    project_names=[],
    project_summaries="",
    highlights="",
    resume_latex="",
    tex_file=None,
    pdf_file=None,
    context=[],
    generation_metadata={}
)

# Create and run workflow
workflow = Workflows.create_resume_cover_letter_workflow()
result = workflow.invoke(state)

print("✅ Resume and cover letter generated!")
```

### 3. Run the Main Application

```bash
python main.py
```

## 🏗️ Architecture

Aria follows a modular, enterprise-grade architecture built on LangChain and LangGraph:

### Core Components

```
src/
├── chains/           # LangChain components for specific tasks
├── config/          # Configuration and settings management
├── extractors/      # Content extraction utilities
├── format/          # LaTeX formatting and compilation
└── workflows/       # LangGraph workflow orchestration
```

### Key Design Patterns

- **Chain of Responsibility**: Each processing step is a separate chain
- **State Management**: LangGraph manages workflow state
- **Dependency Injection**: Modular, testable components
- **RAG Pattern**: Vector search enhanced generation

## ⚙️ Configuration

### Settings Management

Configuration is managed through `src/config/settings.py` using Pydantic:

```python
from src.config.settings import settings

# Access configuration
print(settings.openai_model)
print(settings.chunk_size)
```

### Customizable Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CHUNK_SIZE` | 1000 | Text chunk size for vector store |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `NUM_DOCS` | 8 | Number of documents to retrieve |
| `MAX_EXPERIENCES` | 4 | Maximum experiences in resume |
| `MAX_PROJECTS` | 5 | Maximum projects in resume |

## 📖 Usage

### Data Preparation

1. **Papers**: Place PDF research papers in `data/papers/`
2. **Projects**: Add Markdown project documentation in `data/projects/`
3. **Transcripts**: Store JSON course/interview transcripts in `data/transcripts/`
4. **Personal Data**: Update the following files:
   - `data/experiences.json`: Work experiences
   - `data/technical_skills.json`: Skills and expertise levels
   - `data/projects.json`: Project portfolio

### Workflow Types

#### Resume-Only Generation
```python
resume_workflow = Workflows.create_resume_workflow()
result = resume_workflow.invoke(state)
```

#### Combined Resume + Cover Letter
```python
combined_workflow = Workflows.create_resume_cover_letter_workflow()
result = combined_workflow.invoke(state)
```

### Output Files

Generated documents are saved to:
- **Resumes**: `output/resumes/{company}/{position}.pdf`
- **Cover Letters**: `output/cover_letters/{company}/{position}.pdf`

## 🔧 API Reference

### Core Classes

#### `ResumeState`
State object that flows through the workflow:

```python
@dataclass
class ResumeState(TypedDict):
    job_posting: str
    company: str
    position: str
    experiences: str
    skills: str
    project_names: List[str]
    project_summaries: str
    highlights: str
    context: List[Document]
    # ... additional fields
```

#### `ContextRetrievalChain`
Handles RAG functionality:

```python
class ContextRetrievalChain(BaseChain):
    def add_papers(self) -> None
    def add_projects(self) -> None
    def add_transcripts(self) -> None
    def retrieve_context(self, state: ResumeState) -> Dict[str, Any]
```

#### `Workflows`
LangGraph workflow orchestration:

```python
class Workflows:
    @staticmethod
    def create_resume_workflow() -> CompiledGraph
    
    @staticmethod
    def create_resume_cover_letter_workflow() -> CompiledGraph
```

### Processing Chains

| Chain | Purpose | Input | Output |
|-------|---------|-------|--------|
| `ExperienceChain` | Generate experience section | Job posting | LaTeX experiences |
| `SkillsChain` | Tailor skills section | Job posting, skills | LaTeX skills |
| `ProjectSelectionChain` | Select relevant projects | Job posting, projects | Project names |
| `ProjectSummariesChain` | Generate project summaries | Projects, job posting | LaTeX projects |
| `HighlightChain` | Create qualification highlights | All content | LaTeX highlights |
| `CoverLetterChain` | Generate cover letter | Resume + context | LaTeX cover letter |


## 🛠️ Project Structure

```
Aria/
├── src/
│   ├── chains/                 # Processing chains
│   │   ├── base.py            # Abstract base chain
│   │   ├── experience_chain.py
│   │   ├── skills_chain.py
│   │   ├── project_selection_chain.py
│   │   ├── project_summaries_chain.py
│   │   ├── highlight_chain.py
│   │   ├── context_retrieval_chain.py
│   │   └── cover_letter_chain.py
│   ├── config/                # Configuration management
│   │   ├── settings.py        # Pydantic settings
│   │   └── prompts.py         # Centralized prompts
│   ├── extractors/            # Content extraction
│   │   └── latex_extractor.py # LaTeX content parsing
│   ├── format/                # Document formatting
│   │   ├── latex_formatter.py # LaTeX template formatting
│   │   └── latex_compiler.py  # PDF compilation
│   └── workflows/             # LangGraph workflows
│       ├── states.py          # State definitions
│       ├── nodes.py           # Workflow nodes
│       └── workflows.py       # Workflow construction
├── data/                      # Input data
│   ├── papers/               # PDF research papers
│   ├── projects/             # Markdown project docs
│   ├── transcripts/          # JSON transcripts
│   ├── experiences.json      # Work experiences
│   ├── technical_skills.json # Skills database
│   └── projects.json         # Project portfolio
├── output/                   # Generated documents
│   ├── resumes/             # Generated resumes
│   └── cover_letters/       # Generated cover letters
├── main.py                  # Main application
├── requirements.txt         # Dependencies
└── README.md               # This file
```


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Aria** - Intelligent Resume & Cover Letter Generation with AI