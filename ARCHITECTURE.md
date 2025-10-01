# Industry LangChain Project Structure

Here's how professional LangChain projects are typically organized:

```
aria/
├── src/
│   ├── __init__.py
│   ├── main.py                    # Entry point & orchestration
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Environment & API keys
│   │   └── prompts.py             # All prompt templates
│   ├── chains/
│   │   ├── __init__.py
│   │   ├── base.py                # Base chain class
│   │   ├── experience_chain.py    # Experience generation
│   │   ├── skills_chain.py        # Skills generation
│   │   ├── project_chain.py       # Project selection & summary
│   │   └── highlights_chain.py    # Highlights generation
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── resume_agent.py        # Main resume generation agent
│   │   └── optimization_agent.py  # Length optimization agent
│   ├── workflows/
│   │   ├── __init__.py
│   │   ├── resume_workflow.py     # LangGraph workflow
│   │   └── states.py              # State definitions
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── latex_extractor.py     # LaTeX extraction logic
│   │   └── json_extractor.py      # JSON extraction logic
│   ├── formatters/
│   │   ├── __init__.py
│   │   ├── latex_formatter.py     # LaTeX formatting
│   │   └── pdf_generator.py       # PDF compilation
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loaders.py             # Data loading utilities
│   │   └── processors.py          # Data processing
│   └── utils/
│       ├── __init__.py
│       ├── validators.py          # Input validation
│       ├── helpers.py             # Common utilities
│       └── exceptions.py          # Custom exceptions
├── data/                          # Data files (existing)
├── output/                        # Generated files (existing)
├── tests/
│   ├── __init__.py
│   ├── test_chains/
│   ├── test_agents/
│   └── test_workflows/
├── requirements.txt
├── pyproject.toml                 # Modern Python packaging
├── .env.example
└── README.md
```

## Key Architecture Principles:

### 1. **Separation of Concerns**
- **Chains**: Single-responsibility components
- **Agents**: High-level orchestration
- **Workflows**: State management with LangGraph
- **Extractors**: Content parsing logic
- **Formatters**: Output generation

### 2. **Configuration Management**
- Environment variables in `.env`
- Centralized settings in `config/settings.py`
- All prompts in `config/prompts.py`

### 3. **Modular Design**
- Each chain is a separate class
- Reusable components
- Easy testing and mocking

### 4. **Error Handling**
- Custom exceptions
- Retry mechanisms
- Graceful degradation

### 5. **Scalability**
- Async support where needed
- Caching strategies
- Performance monitoring