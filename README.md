# Lekhak AI (लेखक AI) - Professional Content Creation Platform

> **Lekhak** means "Writer" in Hindi - an AI platform that replicates professional human content writers for B2B organizations.

[![Google ADK](https://img.shields.io/badge/Google-ADK%201.19+-4285F4?logo=google)](https://github.com/google/genai-agent-starter-kit)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791?logo=postgresql)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?logo=streamlit)](https://streamlit.io/)

## 🎯 Overview

**Lekhak AI** is a professional B2B content creation platform built with **Google ADK (Agent Development Kit)** that automatically generates publication-ready social media posts and blog articles that match professional human writer quality.

### **Key Differentiator**
Unlike generic AI content generators, Lekhak AI requires comprehensive business context (company name, products, services, unique value, target audience) to create branded, strategic content that organizations can publish immediately.

## 🏗️ Architecture

### **Multi-Agent System (Google ADK)**

```
User Query → Planner Agent → Router Agent → Content Pipeline → Final Output
                                              ↓
                                    ┌─────────┴─────────┐
                             Social Pipeline      Blog Pipeline
                                    ↓                   ↓
                            Researcher              Researcher
                                ↓                       ↓
                            Writer                  Writer
                                ↓                       ↓
                            Presenter              Presenter
```

### **Technology Stack**
- **Google ADK 1.19+**: Multi-agent orchestration, session management
- **Gemini 2.0 Flash**: LLM for content generation
- **PostgreSQL**: Session persistence (Google ADK DatabaseSessionService)
- **Streamlit**: Web interface
- **Pydantic**: Schema validation
- **asyncpg**: Async database operations

## ✨ Features

### **Content Generation**
- ✅ **Social Media Posts**: Platform-optimized (LinkedIn, Instagram, Facebook, Twitter)
  - 1-line attention-grabbing hook
  - 2-3 lines branded content
  - Trending hashtags
  - Clean, copy-paste ready format

- ✅ **Blog Articles**: SEO-optimized long-form content
  - 1500-2500 words
  - Professional structure (intro, sections, conclusion)
  - Company integration throughout
  - Markdown formatted

### **Information Flow**
- ✅ **Zero Information Loss**: Company name, products, services flow through all agents
- ✅ **Context Preservation**: Google ADK session state maintains all data
- ✅ **Professional Quality**: Output matches human content writer standards

### **Platform Integration**
- ✅ **Database Persistence**: PostgreSQL-backed sessions
- ✅ **Web Interface**: Streamlit UI for easy access
- ✅ **Async Processing**: Fast, efficient content generation

## 🚀 Quick Start

**🎯 New to Lekhak AI? Start here: [QUICKSTART.md](QUICKSTART.md)**

### **Prerequisites**
```bash
- Python 3.12+
- PostgreSQL 16+ (optional - uses in-memory if not configured)
- Google API Key (Gemini)
```

### **Installation**

1. **Clone the repository**
```bash
git clone <repository-url>
cd Lekhak-AI
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -e .
```

4. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your configuration:
GOOGLE_API_KEY=your_gemini_api_key
DB_URL=postgresql://user:password@localhost:5432/lekhak_db
APP_NAME=lekhak_ai
```

5. **Initialize database**
```bash
# Create PostgreSQL database
createdb lekhak_db

# Google ADK will auto-create session tables
```

6. **Run the application**
```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## 📖 Usage

### **Creating Content**

1. **Open Lekhak AI** in your browser
2. **Enter your request** with business context:
   ```
   Create a LinkedIn post announcing our new AI-powered task management feature.
   Company: TechFlow AI
   Product: TaskMaster Pro
   Target Audience: Busy professionals and project managers
   ```

3. **Receive professional content**:
   ```
   Drowning in endless tasks with no time to breathe?

   Introducing TaskMaster Pro by TechFlow AI - the intelligent task management platform that cuts your workload time by 50%. Built for busy professionals who need to focus on what truly matters, not wrestle with complex tools.

   #productivity #ai #taskmanagement #saas #innovation
   ```

### **Input Requirements**

For best results, provide:
- ✅ Company/brand name
- ✅ Products or services  
- ✅ What makes you unique
- ✅ Target audience
- ✅ Content topic
- ✅ Platform (social media or blog)
- ✅ Desired tone

## 🏛️ Project Structure

```
Lekhak-AI/
├── app.py                          # Streamlit web interface
├── pyproject.toml                  # Project dependencies
├── .env                            # Environment configuration
├── src/
│   ├── agents/
│   │   ├── content_creator_agent.py    # Main orchestrator
│   │   ├── planner_agent.py           # Extracts company info
│   │   ├── router_agent.py            # Routes to pipelines
│   │   └── pipelines/
│   │       ├── social_pipeline.py     # Social media generation
│   │       └── blog_pipeline.py       # Blog article generation
│   ├── schema/
│   │   ├── planner_schema.py         # Planner input/output
│   │   └── pipeline_schemas.py       # Pipeline schemas
│   ├── prompts/
│   │   └── planner_instruction.py    # Planner instructions
│   ├── services/
│   │   ├── lekhak_service.py        # Main service layer
│   │   └── agent_clients.py         # ADK client wrapper
│   ├── config/
│   │   └── settings.py              # Configuration
│   └── utils/
│       └── loggers.py               # Logging utilities
└── docs/
    └── INFORMATION_FLOW.md          # Detailed architecture docs
```

## 🔧 Configuration

### **Environment Variables**

```env
# Google Gemini API
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=0

# Database
DB_URL=postgresql://username:password@localhost:5432/lekhak_db

# Application
APP_NAME=lekhak_ai
USER_ID=default_user
```

### **Model Configuration** (`src/config/settings.py`)
```python
GEMINI_MODEL = "gemini-2.0-flash"  # Fast, efficient
# or
GEMINI_MODEL = "gemini-2.0-pro"    # Higher quality
```

## 🧠 How It Works

### **Agent Flow (Google ADK)**

**1. Planner Agent** (`planner_agent.py`)
- Extracts: company_name, products_services, company_description, unique_value, target_audience, topic, platform, tone
- Decides: social, blog, or both
- Saves to session state: `planner_output`

**2. Router Agent** (`router_agent.py`)
- Reads: `planner_output` from session state
- Routes to appropriate pipeline
- Handles parallel execution if "both"

**3. Content Pipeline** (Sequential)

**Social Media:**
```
Researcher → Analyzes company context, audience, trends, hashtags
     ↓
Writer → Creates 1-line hook + 2-3 line content + hashtags
     ↓
Presenter → Formats clean, copy-paste ready output
```

**Blog:**
```
Researcher → Deep topic analysis, company positioning
     ↓
Writer → Creates 1500-2500 word article with sections
     ↓
Presenter → Formats markdown, publication-ready
```

**4. Output Delivery**
- Returns final formatted content to user
- Session persisted in PostgreSQL (Google ADK)

### **Information Flow Guarantee**

✅ **No Information Loss**
- All company data flows through every agent
- Google ADK session state maintains context
- Agents explicitly reference previous outputs
- Pydantic schemas enforce data integrity

See [docs/INFORMATION_FLOW.md](docs/INFORMATION_FLOW.md) for detailed architecture.

## 🛠️ Development

### **Adding New Features**

**1. Add new agent:**
```python
from google.adk.agents import LlmAgent

new_agent = LlmAgent(
    name="agent_name",
    model=GEMINI_MODEL,
    description="Agent purpose",
    output_schema=YourSchema,
    output_key="agent_output",
    instruction="Detailed instructions..."
)
```

**2. Update schema:**
```python
class YourSchema(BaseModel):
    field: str = Field(description="Field purpose")
```

**3. Add to pipeline:**
```python
pipeline = SequentialAgent(
    name="pipeline_name",
    sub_agents=[agent1, agent2, new_agent]
)
```

### **Testing**

```bash
# Test planner extraction
python -m pytest tests/test_planner.py

# Test content generation
python -m pytest tests/test_pipelines.py
```

## 📊 Database Schema

Google ADK automatically manages session tables. Optional custom tables for company/product management can be added in `database/schema.sql`.

## 🤝 Contributing

This is a professional B2B platform. Contributions should:
- Follow Google ADK patterns
- Maintain information flow integrity
- Include proper Pydantic schemas
- Add tests for new features
- Update documentation

## 📄 License

[Your License]

## 🔗 Resources

- [Google ADK Documentation](https://github.com/google/genai-agent-starter-kit)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📞 Support

For issues or questions:
1. Check [docs/INFORMATION_FLOW.md](docs/INFORMATION_FLOW.md)
2. Review agent instructions in `src/prompts/`
3. Verify schemas in `src/schema/`
4. Open an issue

---

**Built with Google ADK** | **Powered by Gemini 2.0** | **Professional B2B Content Creation**
