"""Service for generating content using Lekhak AI with company and product context."""

import time
from datetime import datetime
from typing import Optional

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from sqlalchemy import select

from app.agents.content_creator_agent import content_creator_agent
from app.core.setting import APP_NAME, DATABASE_URL
from app.database import SessionLocal
from app.models.company import Company
from app.models.framework import Framework
from app.models.product import Product
from app.schemas.planner_schema import CompanyContext, ProductContext
from app.services.agent_clients import AgentClient
from app.utils.loggers import get_logger

logger = get_logger("lekhak_service")

# Global singleton instances - created once and reused across all requests
_session_service = None
_runner = None
_agent_client = None


def _get_agent_client() -> AgentClient:
    """Get or create singleton agent client instance."""
    global _session_service, _runner, _agent_client

    if _agent_client is None:
        _session_service = DatabaseSessionService(db_url=DATABASE_URL)
        _runner = Runner(
            agent=content_creator_agent,
            app_name=APP_NAME,
            session_service=_session_service,
        )
        _agent_client = AgentClient(_runner, _session_service, APP_NAME)

    return _agent_client


async def _get_context_data(
    company_id: Optional[int] = None,
    product_id: Optional[int] = None,
    framework_id: Optional[int] = None,
) -> dict:
    """Get company, product, and framework context from database.

    Returns a dict with keys: company_context, product_context, framework_context
    All values are dicts ready for session state injection.
    """
    context = {}

    async with SessionLocal() as db:
        # Query company
        if company_id:
            result = await db.execute(select(Company).where(Company.id == company_id))
            company = result.scalar_one_or_none()

            if company:
                context["company_context"] = CompanyContext(
                    company_id=company.id,
                    name=company.name,
                    industry=company.industry,
                    description=company.description,
                    url=company.url,
                ).model_dump()
                context["company_name"] = company.name
                context["company_description"] = company.description
                context["company_url"] = company.url
                context["industry"] = company.industry

        # Query product
        if product_id:
            result = await db.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()

            if product:
                context["product_context"] = ProductContext(
                    product_id=product.id,
                    name=product.name,
                    description=product.description,
                    url=product.url,
                ).model_dump()
                context["product_name"] = product.name
                context["product_description"] = product.description
                context["product_url"] = product.url

        # Query framework (default to AIDA if not specified)
        if framework_id:
            result = await db.execute(
                select(Framework).where(Framework.id == framework_id)
            )
            framework = result.scalar_one_or_none()
        else:
            # Default to AIDA framework
            result = await db.execute(select(Framework).where(Framework.name == "AIDA"))
            framework = result.scalar_one_or_none()

        if framework:
            context["framework_context"] = {
                "name": framework.name,
                "description": framework.description,
                "instruction": framework.instruction,
            }
            context["framework_name"] = framework.name 
            context["framework_description"] = framework.description
            context["framework_instruction"] = framework.instruction
            logger.info(f"Framework selected: {framework.name}")
        else:
            logger.warning("No framework found - AIDA default should be applied")

    context["current_year"] = str(datetime.now().year)

    return context


async def async_generate_content(
    prompt: str,
    user_id: str = "test_user",
    session_id: Optional[str] = None,
    company_id: Optional[int] = None,
    product_id: Optional[int] = None,
    framework_id: Optional[int] = None,
) -> str:
    start_time = time.time()
    logger.info(f" START GENERATION (Task: {session_id})")

    default_state = {"user_name": user_id}
    user_request = {"instruction": prompt}

    # Fetch all context data in one call (company, product, framework)
    context_data = await _get_context_data(company_id, product_id, framework_id)
    default_state.update(context_data)

    # Set framework name in user request for planner routing
    if "framework_context" in context_data:
        user_request["framework_name"] = context_data["framework_context"]["name"]

    # Initialize agent client and create session
    client = _get_agent_client()
    effective_session_id = session_id or user_id
    session = await client.get_or_create_session(
        user_id, session_id=effective_session_id, initial_state=default_state
    )
    session_id = session.id

    # Update session state to ensure current request's context/framework is used.
    for key, value in default_state.items():
        session.state[key] = value

    # Verify framework in session state
    if "framework_context" in session.state:
        logger.info(
            f"Framework context verified in session {session_id}: {session.state['framework_context']['name']}"
        )
    else:
        logger.warning(f"Framework context missing from session {session_id}")

    # Process agent call
    agent_start = time.time()
    response = await client.send_message(user_id, session_id, user_request)
    logger.info(f"Agent processing took {time.time() - agent_start:.2f}s")

    logger.info(f" TOTAL GENERATION TIME: {time.time() - start_time:.2f}s ")

    if response.get("ok"):
        return response["content"]

    # Handle errors with user-friendly messages
    error = response.get("error", "Unknown error")

    # Check for specific error types
    if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
        raise Exception(
            "Rate limit exceeded. Please try again in a few moments. Our AI service has reached its request limit."
        )
    elif "quota" in str(error).lower():
        raise Exception(
            "Service quota exceeded. Please try again later or contact support."
        )
    elif "invalid" in str(error).lower() or "authentication" in str(error).lower():
        raise Exception("Service configuration error. Please contact support.")
    else:
        raise Exception(
            f"Unable to generate content at this time. Please try again later."
        )
