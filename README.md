# Lekhak AI

AI-powered content generation platform built with Google's Agent Development Kit (ADK), FastAPI, and PostgreSQL.

## Overview

Lekhak AI automates content creation through a multi-agent system that researches, writes, and optimizes blog posts and social media content. The platform uses intelligent routing to determine content type and applies proven persuasion frameworks (AIDA, PAS) for structured output.

### Key Features

- **Multi-Agent Architecture** - Specialized agents for planning, research, writing, and optimization
- **Dual Content Pipelines** - Separate workflows for blog posts and social media content
- **Brand Context Awareness** - Generates content aligned with company and product information
- **Framework Selection** - Supports AIDA, PAS, and other content frameworks
- **Async Architecture** - Built with async Python for high performance

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Google AI API key ([Get one here](https://aistudio.google.com/apikey))
- SerpAPI key ([Get one here](https://serpapi.com/))

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/Lekhak-AI.git
cd Lekhak-AI

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Start services
docker-compose up -d
```

### Access

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Docker Commands

```bash
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f        # View logs
docker-compose up -d --build  # Rebuild and start
docker-compose down -v        # Stop and remove volumes
```

### Development Mode

```bash
docker-compose -f docker-compose.dev.yml up -d
```

Includes hot reload and pgAdmin at http://localhost:5050.

## Local Development

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Setup

```bash
# Clone repository
git clone https://github.com/your-username/Lekhak-AI.git
cd Lekhak-AI

# Install dependencies with uv
uv sync

# Configure environment
cp .env.example .env
# Add your API keys to .env

# Start database
docker-compose up -d postgres

# Run backend
cd backend
uv run uvicorn app.main:app --reload

# Run frontend (separate terminal)
cd frontend
uv run streamlit run app.py
```

## Architecture

```
Frontend (Streamlit)
        |
        v
Backend (FastAPI)
        |
        +-- Routers (API endpoints)
        +-- Services (Business logic)
        +-- Agent System
                |
                +-- Content Creator Agent (Master)
                        |
                        +-- Planner Agent
                        +-- Router Agent
                                |
                                +-- Blog Pipeline
                                |       +-- Research Agent
                                |       +-- Writer Agent
                                |       +-- Optimizer Agent
                                |       +-- Presenter Agent
                                |
                                +-- Social Pipeline
                                        +-- Research Agent
                                        +-- Generator Agent
                                        +-- Optimizer Agent
        |
        v
External Services: PostgreSQL, Google AI (Gemini), SerpAPI
```

## Project Structure

```
Lekhak-AI/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI agent definitions
│   │   │   └── pipelines/    # Blog and social pipelines
│   │   ├── core/             # Configuration
│   │   ├── models/           # Database models
│   │   ├── routers/          # API endpoints
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── tools/            # Agent tools
│   │   └── prompts/          # Agent instructions
│   └── logs/
├── frontend/
│   └── app.py
├── docker-compose.yml
├── docker-compose.dev.yml
├── Dockerfile
├── Dockerfile.dev
├── Makefile
└── pyproject.toml
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/content/generate | Generate content |
| GET | /api/companies | List companies |
| POST | /api/companies | Create company |
| GET | /api/products | List products |
| POST | /api/products | Create product |
| GET | /api/conversations | Get conversation history |

Full documentation available at http://localhost:8000/docs.

## Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| GOOGLE_API_KEY | Google AI API key | Yes |
| SERPAPI_API_KEY | SerpAPI key | Yes |
| GEMINI_MODEL | Model name (default: gemini-2.5-flash) | No |
| DB_HOST | Database host (default: localhost) | No |
| DB_PORT | Database port (default: 5432) | No |
| DB_NAME | Database name (default: lekhak_ai) | No |
| DB_USER | Database user (default: postgres) | No |
| DB_PASSWORD | Database password | No |

## Makefile Commands

```bash
make up          # Start production
make down        # Stop services
make dev         # Start development
make logs        # View logs
make build       # Rebuild containers
make clean       # Remove containers and volumes
make db-shell    # Open database shell
```

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy (async), Pydantic
- **AI**: Google Agent Development Kit (ADK), Gemini
- **Database**: PostgreSQL 16
- **Frontend**: Streamlit
- **Infrastructure**: Docker, Docker Compose

## License

MIT License - see [LICENSE](LICENSE) for details.
