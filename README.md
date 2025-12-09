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

### In Progress

Implementing frontend interface using Streamlit for user interaction with Lekhak AI.

### Upcoming Features

-Implemting social pipelines and blog pipelines for content generation by changing the test implementations pipelines for the router agent.

### Recent Updates (December 2025)
