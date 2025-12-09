"""Service for generating content using Lekhak AI with company and product context."""

from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from sqlalchemy import select
from app.agents.content_creator_agent import content_creator_agent
from app.services.agent_clients import get_agent_client_cached
from app.core.setting import APP_NAME, DATABASE_URL
from app.database import SessionLocal
from app.models.company import Company
from app.models.product import Product
from app.schemas.planner_schema import CompanyContext, ProductContext


async def _build_user_request(
    prompt: str, company_id: int, product_id: Optional[int] = None
) -> dict:
    """Build structured UserRequest with company and product context."""
    async with SessionLocal() as db:
        # Query company
        result = await db.execute(select(Company).where(Company.id == company_id))
        company = result.scalar_one_or_none()

        if not company:
            return {"instruction": prompt}

        company_context = CompanyContext(
            company_id=company.id,
            name=company.name,
            industry=company.industry,
            description=company.description,
        )

        product_context = None
        if product_id:
            # Query product
            result = await db.execute(select(Product).where(Product.id == product_id))
            product = result.scalar_one_or_none()
            if product:
                product_context = ProductContext(
                    product_id=product.id,
                    name=product.name,
                    description=product.description,
                )

        user_request = {
            "instruction": prompt,
            "company_context": (
                company_context.model_dump() if company_context else None
            ),
            "product_context": (
                product_context.model_dump() if product_context else None
            ),
        }

        return user_request


async def async_generate_content(
    prompt: str,
    user_id: str = "test_user",
    company_id: Optional[int] = None,
    product_id: Optional[int] = None,
) -> str:
    """Generate content with optional company and product context."""

    if company_id:
        user_request = await _build_user_request(prompt, company_id, product_id)
    else:
        user_request = {"instruction": prompt}

    print(f"Creating new isolated session service for user: {user_id}")
    session_service = DatabaseSessionService(db_url=DATABASE_URL)
    runner = Runner(
        agent=content_creator_agent, app_name=APP_NAME, session_service=session_service
    )
    client = get_agent_client_cached(runner, session_service, APP_NAME)

    session = await client.get_or_create_session(user_id)
    session_id = session.id

    resp = await client.send_message(user_id, session_id, user_request)

    if resp.get("ok"):
        return resp["content"]

    # Handle errors with user-friendly messages
    error = resp.get("error", "Unknown error")

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
