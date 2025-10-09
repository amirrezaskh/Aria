<h2 align="center" style="display: inline-block; border-bottom: 2px solid #ccc; padding-bottom: 6px;">
  <img src="frontend/public/agent.png" alt="Aria Logo" width="60" height="60" style="vertical-align: middle; margin-right: 10px;">
  Aria: AI-Powered Resume & Cover Letter Generation Platform
</h2>

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19.1.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![Chrome Extension](https://img.shields.io/badge/chrome-extension-green.svg)](https://developer.chrome.com/docs/extensions/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aria is an intelligent AI-powered platform that generates personalized resumes and cover letters using advanced language models, vector similarity matching, and seamless browser integration. The platform analyzes job descriptions and automatically creates tailored application materials optimized for specific positions.

## 🌟 Key Features

### 🤖 AI-Powered Document Generation
- **Smart Resume Creation**: Generates tailored resumes based on job descriptions and user profile using LangChain workflows
- **Dynamic Cover Letters**: Creates personalized cover letters matching specific job requirements
- **Template-Based Generation**: Choose from 4 professional templates (ML Engineering, Data Science, Software Engineering, Overall)
- **LaTeX Processing**: High-quality PDF generation with professional formatting

### 🔍 Intelligent Job Matching & Similarity
- **Vector Similarity Search**: Uses OpenAI embeddings (text-embedding-3-small) to find similar job applications
- **Semantic Understanding**: Analyzes job descriptions using pgvector for better content matching
- **Duplicate Prevention**: Prevents duplicate applications to the same company-position combinations
- **Smart Recommendations**: Suggests existing resumes for similar positions

### 🌐 Chrome Extension Integration
- **Automatic Job Detection**: Extracts job data from LinkedIn, Indeed, and Wellfound/AngelList
- **Side Panel Interface**: Embedded React app directly in Chrome browser
- **Real-time Data Transfer**: Seamless communication between web pages and application
- **One-Click Generation**: Generate documents without leaving the job posting page

### 🔄 Advanced Workflow Intelligence
- **Selective Generation**: Smart routing between full generation vs. cover letter-only workflows
- **Template Reuse**: Quickly generate cover letters using existing resume templates
- **Document Management**: Organized storage and retrieval of generated documents
- **Context Awareness**: Retrieves relevant experience and project information

### 📊 Database & Analytics
- **PostgreSQL + pgvector**: Advanced vector database for similarity search
- **Job Application Tracking**: Comprehensive storage of all job applications
- **System Health Monitoring**: Database connection monitoring and health checks
- **Embedding Management**: Automatic backfill and management of vector embeddings

## 🏗️ Architecture

```
Aria/
├── 🎨 frontend/                    # React + TypeScript Web Application
│   ├── src/
│   │   ├── components/            # Reusable UI components (Material-UI)
│   │   ├── features/generate/     # Document generation feature
│   │   │   ├── components/        # Generation-specific components
│   │   │   ├── hooks/             # Custom React hooks (useGenerateForm)
│   │   │   ├── types/             # TypeScript type definitions
│   │   │   └── constants/         # API endpoints and templates
│   │   └── types/                 # Global TypeScript types
│   ├── public/                    # Static assets and icons
│   └── package.json               # Dependencies (React 19, Material-UI)
│
├── 🤖 agent/                      # Python Backend & AI Engine
│   ├── src/
│   │   ├── api/                   # Flask REST API
│   │   │   ├── routes/            # API route handlers
│   │   │   │   ├── generation.py  # Document generation endpoints
│   │   │   │   ├── jobs.py        # Job management endpoints
│   │   │   │   ├── resumes.py     # Resume serving endpoints
│   │   │   │   ├── database.py    # Database management
│   │   │   │   └── context.py     # Vector store management
│   │   │   ├── middleware/        # Error handling and logging
│   │   │   └── utils/             # File helpers and utilities
│   │   ├── chains/                # LangChain conversation chains
│   │   │   ├── experience_chain.py      # Experience generation
│   │   │   ├── skills_chain.py          # Skills tailoring
│   │   │   ├── project_selection_chain.py # Project selection
│   │   │   ├── cover_letter_chain.py    # Cover letter generation
│   │   │   └── context_retrieval_chain.py # Context retrieval
│   │   ├── workflows/             # AI workflow orchestration
│   │   │   ├── workflows.py       # Main workflow definitions
│   │   │   ├── states.py          # Workflow state management
│   │   │   └── nodes.py           # Workflow node implementations
│   │   ├── database/              # Modular database architecture
│   │   │   ├── connection.py      # Database connection management
│   │   │   ├── schema.py          # Schema management & migrations
│   │   │   ├── embedding_service.py # Vector operations
│   │   │   ├── job_repository.py  # Job CRUD operations
│   │   │   ├── similarity_service.py # Similarity search
│   │   │   └── database.py        # Main database orchestrator
│   │   ├── extractors/            # Data extraction utilities
│   │   │   ├── latex_extractor.py # LaTeX content extraction
│   │   │   └── job_extractor.py   # Job posting analysis
│   │   ├── format/                # Document formatting
│   │   │   ├── latex_formatter.py # LaTeX document formatting
│   │   │   └── pdf_generator.py   # PDF generation utilities
│   │   └── config/                # Configuration management
│   │       └── settings.py        # Environment configuration
│   ├── data/                      # Templates & sample data
│   │   ├── resumes/               # Resume templates (PDF)
│   │   ├── projects/              # Project descriptions
│   │   ├── experiences/           # Experience templates
│   │   └── papers/                # Research papers
│   ├── output/                    # Generated documents
│   │   ├── resumes/               # Generated resume PDFs
│   │   └── cover_letters/         # Generated cover letter PDFs
│   ├── server.py                  # Flask application entry point
│   ├── setup_db.py               # Database initialization
│   └── requirements.txt           # Python dependencies
│
├── 🧩 chrome-extension/           # Chrome Browser Extension
│   ├── manifest.json             # Extension configuration (Manifest V3)
│   ├── background.js             # Service worker for extension
│   ├── content.js                # Content script for job sites
│   ├── sidepanel.html            # Side panel HTML interface
│   ├── sidepanel-react.js        # React app integration
│   ├── sidepanel.css             # Extension styling
│   └── icons/                    # Extension icons (agent.png)
│
└── 📚 Documentation/
    ├── PRODUCT_ROADMAP.md         # Product development roadmap
    ├── CHROME_EXTENSION_ARCHITECTURE.md # Extension architecture
    └── ENHANCEMENT_ROADMAP.md     # Technical enhancement plans
```

## 📐 System Architecture

### High-Level Architecture

```mermaid
graph TD
    subgraph "Client Layer"
        WEB[React Web App]
        EXT[Chrome Extension]
        SP[Side Panel]
    end
    
    subgraph "API Gateway"
        FLASK[Flask Server :8080]
        CORS[CORS Handler]
        AUTH[Request Validation]
    end
    
    subgraph "Business Logic"
        WF[AI Workflows]
        CHAIN[LangChain Orchestration]
        GEN[Document Generation]
        SIM[Similarity Engine]
    end
    
    subgraph "AI Services"
        OPENAI[OpenAI API]
        EMB[Embedding Service]
        LLM[Language Models]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL + pgvector)]
        FS[File System Storage]
        VEC[Vector Store]
    end
    
    subgraph "Document Processing"
        TEX[LaTeX Processing]
        PDF[PDF Generation]
        TMPL[Template Engine]
    end
    
    WEB --> FLASK
    EXT --> SP
    SP --> WEB
    FLASK --> CORS
    CORS --> AUTH
    AUTH --> WF
    WF --> CHAIN
    CHAIN --> GEN
    CHAIN --> SIM
    GEN --> OPENAI
    SIM --> EMB
    EMB --> OPENAI
    WF --> PG
    SIM --> VEC
    VEC --> PG
    GEN --> TEX
    TEX --> PDF
    PDF --> FS
    GEN --> TMPL
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **PostgreSQL 15+** with pgvector extension
- **OpenAI API Key** with GPT and embedding access
- **Chrome Browser** (for extension)

### 1. Clone & Environment Setup

```bash
# Clone the repository
git clone https://github.com/amirrezaskh/aria.git
cd aria

# Set up environment variables
cp agent/.env.example agent/.env
# Edit agent/.env with your configuration (see Configuration section)
```

### 2. Database Setup

```bash
# Start PostgreSQL and create database
createdb aria_db

# Install pgvector extension
psql -d aria_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Initialize database schema
cd agent
python setup_db.py
```

### 3. Backend Setup

```bash
cd agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python server.py
# Server will start on http://localhost:8080
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# Frontend will start on http://localhost:3000
```

### 5. Chrome Extension Setup

```bash
# Load extension in Chrome
1. Open Chrome and navigate to chrome://extensions/
2. Enable "Developer mode" (top-right toggle)
3. Click "Load unpacked"
4. Select the chrome-extension/ directory
5. Pin the Aria extension to your toolbar
```

### 6. Access & Test

- **Web Application**: http://localhost:3000
- **Backend API**: http://localhost:8080
- **Chrome Extension**: Click the Aria icon in Chrome toolbar
- **Test Job Sites**: Visit LinkedIn, Indeed, or Wellfound job postings

## 🔧 Configuration

### Environment Variables

Create `agent/.env` with the following configuration:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/aria_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aria_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Server Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=8080
HOST=localhost

# AI Configuration
SIMILARITY_THRESHOLD=0.8
MAX_SIMILAR_JOBS=5
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4

# File Paths
RESUMES_DIR=./output/resumes
COVER_LETTERS_DIR=./output/cover_letters
TEMPLATES_DIR=./data/resumes
PROJECTS_DIR=./data/projects
EXPERIENCES_DIR=./data/experiences

# Chrome Extension
FRONTEND_URL=http://localhost:3000
EXTENSION_ENABLED=true
```

### Database Schema

The application automatically creates the following tables:

```sql
-- Job applications with vector embeddings
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    position_title VARCHAR(255) NOT NULL,
    job_description TEXT NOT NULL,
    resume_generated BOOLEAN DEFAULT FALSE,
    embedding vector(1536),  -- OpenAI embedding dimension
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_name, position_title)
);

-- Vector similarity index for fast search
CREATE INDEX ON job_applications USING ivfflat (embedding vector_cosine_ops);
```

## 📖 Usage Guide

### Web Application Workflow

1. **Job Information Entry**
   - Enter job title, company name, and paste job description
   - Application automatically detects if Chrome extension provided data

2. **Generation Strategy Selection**
   - **Generate New**: Create both resume and cover letter from scratch
   - **Use Template**: Select from pre-built professional templates
   - **View Similar Jobs**: See previously generated resumes for similar positions

3. **Document Generation Process**
   - AI analyzes job requirements using OpenAI models
   - Generates tailored experiences, skills, and project highlights
   - Creates professional LaTeX-formatted documents
   - Converts to high-quality PDF files

4. **Preview & Download**
   - Preview documents in browser before downloading
   - Download individual PDF files
   - Access previously generated documents

### Chrome Extension Usage

1. **Installation & Setup**
   - Load extension in Chrome developer mode
   - Ensure Aria backend is running on localhost:8080
   - Frontend should be accessible on localhost:3000

2. **Job Site Integration**
   - Visit supported job sites: LinkedIn, Indeed, Wellfound
   - Extension automatically detects job postings
   - Click extension icon to open side panel with embedded Aria app

3. **Automatic Data Transfer**
   - Job information is automatically extracted and populated
   - Generate documents without manual data entry
   - Seamless workflow from job discovery to application materials

### Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | React 19 + TypeScript | Modern, type-safe web application |
| Backend | Flask + Python 3.11 | REST API and AI processing |
| Database | PostgreSQL + pgvector | Vector similarity search |
| AI | OpenAI + LangChain | Document generation and embeddings |
| Extension | Chrome Manifest V3 | Browser integration |
| Styling | Material-UI + CSS | Professional UI design |
| PDF | LaTeX + pdflatex | High-quality document generation |

## 🔮 Upcoming Features

### Phase 1: Enhanced AI Capabilities
- **� Advanced AI Models**: Integration with GPT-4 and Claude
- **📊 Application Success Prediction**: ML models to predict application success
- **🎯 ATS Optimization**: Resume optimization for Applicant Tracking Systems
- **📈 Performance Analytics**: Track application success rates and improvements

### Phase 2: Extended Platform Integration
- **🔗 Job Board APIs**: Direct integration with major job platforms
- **📱 Mobile App**: Native iOS and Android applications
- **🤖 Slack/Teams Integration**: Generate documents from team channels
- **📧 Email Integration**: Auto-generate applications from job emails

### Phase 3: Advanced Features
- **👥 Team Collaboration**: Multi-user accounts and shared templates
- **🔄 Version Control**: Track document versions and changes
- **📊 Interview Preparation**: AI-powered interview question generation
- **🎨 Custom Branding**: Personalized templates and styling

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
