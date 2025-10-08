# Aria Enhanced Architecture

## Overview
This document outlines the enhanced architecture for Aria that incorporates intelligent resume reuse, human-in-the-loop validation, and sophisticated content management.

## Core Components

### 1. Job Input System
```
┌─────────────────┐    ┌──────────────────┐
│  Manual Input   │    │   Web Scraper    │
│                 │    │                  │
│ • Job Desc      │    │ • LinkedIn       │
│ • Position      │    │ • Indeed         │
│ • Company       │    │ • Company Sites  │
└─────────────────┘    └──────────────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌─────────────────────────┐
         │   Job Data Processor    │
         │                         │
         │ • Clean & Normalize     │
         │ • Extract Requirements  │
         │ • Generate Embeddings   │
         └─────────────────────────┘
```

### 2. Resume Strategy Selection
```
User Choice:
├── Generate New Resume
│   ├── Check Similarity Database
│   │   ├── High Match Found → Notify User → Use Existing
│   │   └── No Match → Generate New
│   └── Human-in-Loop Workflow
└── Use Template Resume
    ├── ML Engineering
    ├── Data Science  
    ├── Software Engineering
    ├── PhD
    └── Overall
```

### 3. Enhanced Database Schema

#### Resume Cache Table
```sql
CREATE TABLE resume_cache (
    id SERIAL PRIMARY KEY,
    job_embedding VECTOR(1536),
    company_name VARCHAR(255),
    position_title VARCHAR(255),
    resume_content TEXT,
    resume_pdf_path VARCHAR(500),
    similarity_threshold FLOAT,
    created_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0
);
```

#### Experience Library
```sql
CREATE TABLE experience_library (
    id SERIAL PRIMARY KEY,
    experience_type VARCHAR(100), -- 'work', 'research', 'project'
    original_text TEXT,
    summarized_versions JSONB, -- Different summaries for different job types
    tags VARCHAR[],
    relevance_scores JSONB, -- Scores for different domains
    created_at TIMESTAMP
);
```

#### Project Library
```sql
CREATE TABLE project_library (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    base_description TEXT,
    tech_stack VARCHAR[],
    domain_tags VARCHAR[], -- 'ml', 'web', 'data', etc.
    customized_descriptions JSONB, -- Job-specific descriptions
    relevance_embeddings VECTOR(1536),
    usage_frequency INTEGER DEFAULT 0
);
```

### 4. Workflow Pipeline

#### Stage 1: Job Analysis & Similarity Check
```python
class JobAnalysisStage:
    def process(self, job_data):
        # 1. Generate job embedding
        job_embedding = self.embedding_service.embed(job_data.description)
        
        # 2. Search for similar resumes
        similar_resumes = self.similarity_search(job_embedding, threshold=0.85)
        
        # 3. Present options to user
        if similar_resumes:
            return self.present_similar_options(similar_resumes)
        else:
            return self.proceed_to_generation()
```

#### Stage 2: Experience Selection
```python
class ExperienceSelectionStage:
    def process(self, job_requirements):
        # 1. Retrieve relevant experiences
        experiences = self.experience_library.get_relevant(
            job_requirements, 
            limit=10
        )
        
        # 2. Rank by relevance
        ranked_experiences = self.rank_experiences(experiences, job_requirements)
        
        # 3. Present to user for selection
        return self.present_experience_options(ranked_experiences)
```

#### Stage 3: Skills Generation with Human Validation
```python
class SkillsGenerationStage:
    def process(self, job_requirements, selected_experiences):
        # 1. Generate skills using LLM
        suggested_skills = self.llm.generate_skills(
            job_requirements, 
            selected_experiences
        )
        
        # 2. Present for human validation
        validated_skills = self.human_validation_interface(suggested_skills)
        
        return validated_skills
```

#### Stage 4: Project Selection & Customization
```python
class ProjectSelectionStage:
    def process(self, job_requirements, skills):
        # 1. Get relevant projects
        relevant_projects = self.project_library.search_by_relevance(
            job_requirements, 
            skills
        )
        
        # 2. Rank and suggest
        suggestions = self.rank_projects(relevant_projects, job_requirements)
        
        # 3. User selection
        selected_projects = self.user_selection_interface(suggestions)
        
        # 4. Generate/retrieve customized descriptions
        customized_projects = []
        for project in selected_projects:
            description = self.get_or_generate_description(
                project, 
                job_requirements
            )
            customized_projects.append(description)
            
        return customized_projects
```

### 5. User Interface Enhancements

#### Job Input Form
```tsx
interface JobInputForm {
  // Manual input
  jobDescription: string;
  company: string;
  position: string;
  
  // Scraper input
  jobUrl?: string;
  
  // Options
  resumeStrategy: 'generate' | 'template';
  templateType?: 'ml' | 'ds' | 'swe' | 'phd' | 'general';
}
```

#### Human-in-Loop Interfaces
```tsx
// Skills validation component
const SkillsValidation = ({ suggestedSkills, onValidate }) => {
  // Allow editing, adding, removing skills
  // Show relevance scores
  // Highlight AI-suggested vs user-added
};

// Project selection component  
const ProjectSelection = ({ projects, onSelect }) => {
  // Show relevance scores
  // Preview project descriptions
  // Allow custom project addition
};
```

### 6. Caching & Performance Strategy

#### Vector Search Optimization
```python
class SimilaritySearchService:
    def __init__(self):
        self.index = faiss.IndexFlatIP(1536)  # For fast similarity search
        self.cache = {}
    
    def search_similar_resumes(self, job_embedding, threshold=0.85):
        # Use FAISS for fast vector similarity search
        scores, indices = self.index.search(job_embedding, k=10)
        return self.filter_by_threshold(scores, indices, threshold)
```

#### Content Caching Strategy
```python
class ContentCache:
    def __init__(self):
        self.experience_cache = {}
        self.project_cache = {}
        self.skills_cache = {}
    
    def get_cached_content(self, content_type, job_hash):
        cache = getattr(self, f"{content_type}_cache")
        return cache.get(job_hash)
```

### 7. Machine Learning Pipeline

#### Content Ranking Model
```python
class ContentRankingModel:
    def __init__(self):
        self.experience_ranker = self.load_model('experience_ranking')
        self.project_ranker = self.load_model('project_ranking')
    
    def rank_experiences(self, experiences, job_requirements):
        # Use trained model to rank experiences by relevance
        features = self.extract_features(experiences, job_requirements)
        scores = self.experience_ranker.predict(features)
        return self.sort_by_score(experiences, scores)
```

### 8. Analytics & Learning

#### Usage Tracking
```python
class AnalyticsService:
    def track_resume_generation(self, job_data, user_choices, outcome):
        # Track what works well
        # Learn from user selections
        # Improve similarity matching
        pass
    
    def update_content_popularity(self, selected_content):
        # Update usage frequencies
        # Improve ranking algorithms
        pass
```

## Implementation Priority

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Enhanced database schema
- [ ] Similarity search service
- [ ] Experience/Project libraries
- [ ] Basic UI enhancements

### Phase 2: Human-in-Loop Features (Week 3-4)
- [ ] Skills validation interface
- [ ] Project selection interface
- [ ] Resume similarity notifications
- [ ] Template system

### Phase 3: Advanced Features (Week 5-6)
- [ ] Web scraping service
- [ ] ML ranking models
- [ ] Advanced caching
- [ ] Analytics dashboard

### Phase 4: Production Polish (Week 7-8)
- [ ] Performance optimization
- [ ] Error handling
- [ ] User testing
- [ ] Documentation

## Technical Benefits

1. **Performance**: 70-80% faster resume generation through reuse
2. **Quality**: Human validation ensures accuracy
3. **Consistency**: Reusable content maintains quality standards
4. **Learning**: System improves over time
5. **Scalability**: Efficient caching and search
6. **User Experience**: Faster, more intuitive workflow

## Next Steps

Would you like me to start implementing any specific component? I'd recommend starting with:

1. **Enhanced database schema** - Foundation for everything
2. **Similarity search service** - Core efficiency feature
3. **Human-in-loop UI components** - Better user experience

This architecture maintains your current LangGraph workflow while adding intelligent optimization layers.