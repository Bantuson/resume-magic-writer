# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Resume Magic Writer is an AI-powered resume optimization system built with CrewAI multi-agent framework. It uses three specialized agents in a sequential workflow to transform raw professional data into ATS-optimized, job-tailored resumes.

## Development Commands

### Server Development
```bash
# Start FastAPI development server
uvicorn src.resume_magic_writer.api.main:app --reload

# Access the web interface at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

### Testing
```bash
# Run CrewAI workflow directly (CLI mode)
python -m src.resume_magic_writer.main

# Run tests (when implemented)
pytest
```

### Code Quality
```bash
# Format code
black src/

# Type checking
mypy src/
```

### Dependencies
```bash
# Install with uv (preferred)
uv pip install -e .

# Install with pip
pip install -e .
```

## Architecture

### CrewAI Multi-Agent Workflow

This project implements a **sequential multi-agent workflow** using CrewAI. Understanding this architecture is critical:

1. **ResumeMagicWriterCrew** (`src/resume_magic_writer/crew.py`): Main crew orchestrator using CrewAI's `@CrewBase` decorator pattern
   - Loads agent and task configurations from YAML files
   - Instantiates custom tools (ResumeParserTool, JobAnalyzerTool, ATSOptimizerTool)
   - Defines three agents and three tasks with context dependencies

2. **Agent Pipeline** (Sequential Process):
   - **Resume Data Analyst** → Structures raw resume data using ResumeParserTool
   - **Job Match Strategist** → Analyzes job alignment using JobAnalyzerTool and ATSOptimizerTool (depends on analyst output)
   - **Resume Writer** → Generates final markdown resume using ATSOptimizerTool (depends on both previous outputs)

3. **Task Context Flow**:
   - `structure_candidate_data` → standalone
   - `analyze_job_requirements` → context: [structure_candidate_data]
   - `generate_tailored_resume` → context: [structure_candidate_data, analyze_job_requirements]

### Custom Tools (CrewAI BaseTool Pattern)

All tools inherit from `crewai.tools.BaseTool` and follow this structure:

```python
class CustomTool(BaseTool):
    name: str = "Tool Name"
    description: str = "What the tool does"
    args_schema: Type[BaseModel] = InputSchema  # Pydantic validation

    def _run(self, **kwargs) -> Any:
        # Tool implementation
```

**Tool Locations**:
- `tools/resume_parser.py`: Structures JSON resume data
- `tools/job_analyzer.py`: Analyzes job descriptions and candidate matching
- `tools/ats_optimizer.py`: Optimizes for ATS compatibility

### Configuration Files

**YAML-based configuration** using CrewAI's config pattern:

- `config/agents.yaml`: Defines three agents with role, goal, backstory, and model (gpt-3.5-turbo)
- `config/tasks.yaml`: Defines three tasks with description, expected_output, and agent assignment

**Modifying agents/tasks**: Edit the YAML files, not the Python code. CrewAI loads these at runtime via the `@agent` and `@task` decorators.

### API Layer

**FastAPI application** (`src/resume_magic_writer/api/`):

- `main.py`: App initialization, CORS, static file serving
- `routes.py`: Three main endpoints:
  - `POST /api/generate-resume`: Runs full CrewAI workflow
  - `POST /api/regenerate-resume`: Re-runs with variation instructions
  - `POST /api/download-pdf`: Converts markdown to PDF using WeasyPrint
- `schemas.py`: Pydantic request/response models

**Key API pattern**: Routes instantiate `ResumeMagicWriterCrew()`, convert inputs to JSON strings, call `crew.crew().kickoff(inputs=inputs)`, and return the result.

### Data Models

**Pydantic models** in `src/resume_magic_writer/models/`:

- `resume_models.py`: ResumeData, ContactInfo, WorkExperience, Education, etc.
- `job_models.py`: JobDescription, Requirements, etc.
- `output_models.py`: GeneratedResume output schema

**Important**: The API expects these exact Pydantic schemas in requests. CrewAI tools receive JSON-serialized versions.

### Frontend Architecture

**Vanilla JavaScript** with no framework (`static/`):

- `index.html`: Single-page form interface
- `js/app.js`: Main app orchestration and localStorage auto-save
- `js/form-handler.js`: Form validation and serialization
- `js/api-client.js`: Fetch API calls to backend
- `css/`: Gradient animations, graffiti-style branding, executive resume templates

**Data flow**: Form inputs → JSON serialization → POST /api/generate-resume → Markdown response → Rendered with marked.js

## Environment Configuration

Required environment variables (`.env`):

```env
OPENAI_API_KEY=sk-...          # Required for CrewAI agents
SERPER_API_KEY=...             # Optional: for web search tools
ENVIRONMENT=development
DEBUG=True
```

**Never commit `.env`**. Use `.env.example` as template.

## CrewAI Development Patterns

### Adding a New Agent

1. Define in `config/agents.yaml`:
```yaml
new_agent_name:
  role: >
    Agent role
  goal: >
    What the agent achieves
  backstory: >
    Agent's expertise context
  model: gpt-3.5-turbo
```

2. Create agent method in `crew.py`:
```python
@agent
def new_agent_name(self) -> Agent:
    return Agent(
        config=self.agents_config["new_agent_name"],
        tools=[relevant_tools],
        verbose=True,
        allow_delegation=False,
    )
```

### Adding a New Task

1. Define in `config/tasks.yaml`:
```yaml
new_task_name:
  description: >
    Detailed task instructions
  expected_output: >
    What the task should produce
  agent: agent_name
```

2. Create task method in `crew.py`:
```python
@task
def new_task_name(self) -> Task:
    return Task(
        config=self.tasks_config["new_task_name"],
        agent=self.agent_name(),
        context=[dependent_tasks()],  # Optional
    )
```

### Adding a New Tool

1. Create file in `tools/` following BaseTool pattern:
```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class ToolInput(BaseModel):
    param: str = Field(..., description="Parameter description")

class NewTool(BaseTool):
    name: str = "Tool Name"
    description: str = "What it does (agents read this)"
    args_schema: Type[BaseModel] = ToolInput

    def _run(self, param: str) -> str:
        # Implementation
        return result
```

2. Import in `tools/__init__.py`
3. Instantiate in `ResumeMagicWriterCrew.__init__()`
4. Add to relevant agent's tools list

## Working with Resume Data

**Resume data structure** follows the schema in `resume_models.py`:

```python
{
  "contact_info": {...},
  "professional_summary": "...",
  "work_experience": [...],
  "education": [...],
  "skills": {...},
  "certifications": [...],
  # Optional: projects, volunteer_experience, awards, etc.
}
```

**ResumeParserTool** transforms this into a structured format with header, summary, skills, experience, education, achievements, and certifications.

## PDF Generation

Uses **WeasyPrint** for markdown → PDF conversion in `routes.py`:

- Converts markdown to HTML with `markdown.markdown()`
- Applies executive-style CSS (Georgia font, professional spacing)
- Generates PDF with letter size, 0.75in margins
- Returns as streaming response

**CSS customization**: Modify inline styles in `download_pdf()` function for different templates.

## Output Locations

- **CLI mode**: Saves to `output/generated_resume.md`
- **Web mode**: Returns markdown via API, PDF generated on-demand
- **Frontend**: Auto-saves form data to browser localStorage

## Important Notes

### CrewAI Process Flow
- The workflow is **Process.sequential** - tasks run in order, each receiving context from previous tasks
- Agents do NOT delegate to each other (`allow_delegation=False`)
- All agent reasoning is logged (`verbose=True`)

### API Input Format
Routes expect:
```json
{
  "resume_data": {/* ResumeData Pydantic model */},
  "job_description": {/* JobDescription Pydantic model */}
}
```

But CrewAI receives:
```python
{
  "resume_data": json.dumps(request.resume_data),  # JSON string
  "job_description": job_desc_text  # Plain text
}
```

### Model Configuration
- All agents use `gpt-3.5-turbo` by default (defined in `agents.yaml`)
- Change model globally in YAML or per-agent as needed
- Ensure OPENAI_API_KEY has access to specified models

### Frontend State Management
- Form data auto-saves to localStorage on changes
- Keyboard shortcuts: Ctrl/Cmd+S (save), Ctrl/Cmd+G (generate)
- No database - all state is client-side or ephemeral

## Common Development Tasks

### Modify Agent Behavior
Edit the `description` field in `config/tasks.yaml` to change agent instructions. CrewAI uses these descriptions as LLM prompts.

### Change Resume Format
Modify the `generate_tailored_resume` task description in `tasks.yaml` to specify different formatting requirements (e.g., "use bullet points", "limit to one page").

### Add New API Endpoint
1. Define Pydantic schemas in `api/schemas.py`
2. Add route handler in `api/routes.py`
3. Follow existing pattern: instantiate crew → prepare inputs → kickoff → return response

### Debug CrewAI Workflow
- Run CLI mode: `python -m src.resume_magic_writer.main`
- Check console output - CrewAI logs all agent reasoning and tool calls
- Inspect `output/generated_resume.md` for final result

### Update Dependencies
Edit `pyproject.toml` dependencies array, then:
```bash
uv pip install -e .  # or pip install -e .
```

## Testing Strategy

When implementing tests:
- Test individual tools in isolation (mock LLM calls)
- Test API endpoints with sample data
- Test CrewAI workflow with fixed inputs
- Verify PDF generation with various markdown inputs
- Test frontend form validation and API integration
