import asyncio
import os
from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from src.agents.content_creator_agent import content_creator_agent
from src.services.agent_clients import get_agent_client_cached
from src.config import APP_NAME, DATABASE_URL
from src.database import SessionLocal, get_company_by_id, get_product_by_id
from src.schema.planner_schema import CompanyContext, ProductContext


def _build_user_request(
    prompt: str, company_id: int, product_id: Optional[int] = None
) -> dict:
    """Build structured UserRequest with company and product context."""
    with SessionLocal() as db:
        company = get_company_by_id(db, company_id)

        if not company:
            return {"instruction": prompt}

        company_context = CompanyContext(
            company_id=company.id,
            name=company.name,
            industry=company.industry,
            description=company.description,
            target_audience="General",
            brand_voice="Professional",
        )

        product_context = None
        if product_id:
            product = get_product_by_id(db, product_id)
            if product:
                product_context = ProductContext(
                    product_id=product.id,
                    name=product.name,
                    description=product.description,
                    key_features=product.key_features,
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
        user_request = _build_user_request(prompt, company_id, product_id)
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
    return f"Error: {resp.get('error', 'Unknown')}"
