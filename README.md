# 🎯 Aria - AI-Powered Resume & Cover Letter Generation Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/react-19.1.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Aria is an intelligent AI-powered platform that generates personalized resumes and cover letters using advanced language models and vector similarity matching. The platform analyzes job descriptions and automatically creates tailored application materials optimized for specific positions.

## 🌟 Features

### 🤖 AI-Powered Generation
- **Smart Resume Creation**: Generates tailored resumes based on job descriptions and user profile
- **Dynamic Cover Letters**: Creates personalized cover letters matching specific job requirements
- **Template-Based Generation**: Choose from pre-built professional templates for quick applications

### 🔍 Intelligent Job Matching
- **Vector Similarity Search**: Uses OpenAI embeddings to find similar job applications
- **Semantic Understanding**: Analyzes job descriptions for better content matching
- **Duplicate Prevention**: Prevents duplicate applications to the same company-position combinations

### 🔄 Workflow Intelligence
- **Selective Generation**: Smart routing between full generation vs. cover letter-only workflows
- **Template Reuse**: Quickly generate cover letters using existing resume templates
- **Document Management**: Organized storage and retrieval of generated documents

## 🏗️ Architecture

```
Aria/
├── 🎨 frontend/          # React + TypeScript frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── features/     # Feature-specific components
│   │   ├── hooks/        # Custom React hooks
│   │   └── types/        # TypeScript type definitions
│   └── public/           # Static assets
│
├── 🤖 agent/            # Python backend & AI engine
│   ├── src/
│   │   ├── chains/       # LangChain conversation chains
│   │   ├── config/       # Configuration management
│   │   ├── database/     # Modular database architecture
│   │   ├── extractors/   # Data extraction utilities
│   │   ├── format/       # Document formatting
│   │   └── workflows/    # AI workflow orchestration
│   ├── data/            # Resume templates & sample data
│   ├── output/          # Generated documents
│   └── server.py        # Flask API server
│
└── 📚 papers/           # Research papers & documentation
```



## 📐 System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        UI[React Frontend]
        API[REST API Calls]
    end
    
    subgraph "Application Layer"
        Server[Flask Server]
        Auth[Authentication]
        Valid[Input Validation]
    end
    
    subgraph "Business Logic Layer"
        Workflow[AI Workflows]
        Chain[LangChain Orchestration]
        Embed[Embedding Service]
        Similar[Similarity Engine]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL + pgvector)]
        Files[File Storage]
        Cache[Vector Cache]
    end
    
    subgraph "External Services"
        OpenAI[OpenAI API]
        PDF[PDF Generation]
    end
    
    UI --> API
    API --> Server
    Server --> Auth
    Server --> Valid
    Server --> Workflow
    Workflow --> Chain
    Chain --> Embed
    Chain --> Similar
    Embed --> OpenAI
    Similar --> DB
    Workflow --> Files
    Files --> PDF
    DB --> Cache
```



## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** 
- **PostgreSQL 15+** with pgvector extension
- **OpenAI API Key**

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/aria.git
cd aria

# Set up environment variables
cp agent/.env.example agent/.env
# Edit agent/.env with your configuration
```

### 2. Backend Setup

```bash
cd agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python setup_db.py

# Start the backend server
python server.py
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **Database**: PostgreSQL on port 5432

## 🔧 Configuration

### Environment Variables

Create `agent/.env` with the following variables:

```env
# OpenAI Configuration
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

# Optional: Advanced Configuration
SIMILARITY_THRESHOLD=0.8
MAX_SIMILAR_JOBS=5
EMBEDDING_MODEL=text-embedding-3-small
```

### Database Setup

Ensure PostgreSQL is running with the pgvector extension:

```sql
-- Connect to PostgreSQL
CREATE DATABASE aria_db;
\c aria_db;

-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- The application will automatically create tables
```

## 📖 Usage Guide

### Basic Workflow

1. **Job Information**: Enter job title, company, and job description
2. **Generation Options**:
   - **New Resume**: Generate both resume and cover letter from scratch
   - **Use Template**: Select from pre-built templates for quick generation
   - **Similar Jobs**: View and reuse resumes from similar applications

3. **Document Generation**: AI processes the information and generates tailored documents
4. **Preview & Download**: Review generated documents and download PDFs

### API Endpoints

#### Resume Generation
```http
POST /api/generate/
Content-Type: application/json

{
  "job_title": "Senior Data Scientist",
  "company_name": "TechCorp",
  "job_description": "We are looking for...",
  "additional_instructions": "Emphasize machine learning experience"
}
```

#### Cover Letter Only
```http
POST /api/generate/cover-letter/
Content-Type: application/json

{
  "job_title": "ML Engineer",
  "company_name": "AI Startup",
  "job_description": "...",
  "resume_pdf_file": "/path/to/resume.pdf"
}
```

#### Similarity Search
```http
GET /api/jobs/similar?description=Machine%20learning%20engineer%20role
```

#### Document Preview
```http
GET /api/resumes/preview/ml-engineering
GET /api/resumes/generated/{filename}
```

### Upcoming Features

- **🔌 Chrome Extension**: Browser integration for job applications
- **📊 Analytics Dashboard**: Application tracking and success metrics
- **🤖 Advanced AI Models**: Integration with latest language models
- **📱 Mobile App**: Native mobile application
- **🔗 ATS Integration**: Direct integration with applicant tracking systems

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

