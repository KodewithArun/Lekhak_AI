## Lekhak AI

Lekhak AI is an AI-powered content creation platform designed to streamline and automate the process of generating high-quality written material. Leveraging Google's Agent Development Kit (ADK) for advanced agent orchestration and Streamlit for an intuitive web interface, Lekhak AI enables users to plan, route, and produce content efficiently. The platform integrates with PostgreSQL for robust data management and uses modular agents to handle tasks such as request analysis, content generation, and formatting. Whether you're creating blog posts, social media updates, or other written content, Lekhak AI provides a scalable and extensible solution for modern content workflows.

## Project Status

### Completed Features

#### Backend Infrastructure

- **Async SQLAlchemy Integration**: Migrated from synchronous to async database operations
- **Database Models**: Company, Product, and Conversation models with proper relationships
- **Startup Event**: Automatic database table creation on FastAPI application startup
- **PostgreSQL Integration**: Full async support driver

#### AI Agent System

- **Content Creator Agent**: Master orchestration agent coordinating planner and router
- **Planner Agent**: Intelligent request analysis and pipeline routing with company/product context awareness
- **Router Agent**: Dynamic pipeline selection (social, blog, both, or none) based on planner output

#### API Endpoints (Async)

- **Companies API**: Create, list, and retrieve companies with async operations
- **Products API**: Manage products with company relationships
- **Conversations API**: Track generated content history
- **Content Generation API**: Main endpoint for AI-powered content creation with context

#### Services & Business Logic

- **Lekhak Service**: Content generation orchestration with company/product context integration
- **Agent Client**: Session management, message handling, and parallel content collection
- **Context Building**: Automatic company and product context injection from database
- **Error Handling**: User-friendly error messages for rate limits, quota exceeded, and API failures

## Updated Features

- Social Media Content Generation Pipeline

  1. Social Research Agent along with social_search tool using SerpAPI
  2. Social Content Generator Agent
  3. Social Content Optimizer Agent

- Blog Content Generation Pipeline
  1. Blog Research Agent along with blog_search tool using SerpAPI for google search results.
  2. Blog Content Writer Agent that creates blog content based on research output.
  3. Blog Content Optimizer Agent that refines and polishes the draft blog content.
  4. Blog Content Presenter Agent who present the final output in user friendly way.

### Recent Updates (December 2025)
