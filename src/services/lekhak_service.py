import asyncio
import os
import time
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.errors import ClientError
from src.agents.content_creator_agent import content_creator_agent
from src.services.agent_clients import get_agent_client_cached
from src.config import APP_NAME, DB_URL
from src.utils.loggers import get_logger

logger = get_logger("lekhak_service")


# Initialize runner and session service once
_session_service = DatabaseSessionService(db_url=DB_URL)
_runner = Runner(
    agent=content_creator_agent, app_name=APP_NAME, session_service=_session_service
)
_client = get_agent_client_cached(_runner, _session_service, APP_NAME)

# In-memory session cache for Streamlit app
_user_sessions = {}


async def async_generate_content(prompt: str, user_id: str = "default_user") -> str:
    """Generate content with automatic retry on rate limit errors."""
    max_retries = 3
    base_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            # Reuse session if exists
            if user_id in _user_sessions:
                session = _user_sessions[user_id]
            else:
                #  fetching existing session from DB or creating a new one
                try:
                    session = await _client.session_service.get_session(
                        app_name=APP_NAME, user_id=user_id
                    )
                except Exception:
                    session = None

                if not session:
                    session = await _client.get_or_create_session(user_id)
                _user_sessions[user_id] = session

            session_id = session.id
            resp = await _client.send_message(user_id, session_id, prompt)

            if resp.get("ok"):
                return resp["content"]
            return f"Error: {resp.get('error', 'Unknown')}"

        except Exception as e:
            # Check if it's a rate limit error (429)
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                if attempt < max_retries - 1:
                    delay = base_delay * (2**attempt)  # Exponential backoff: 2s, 4s, 8s
                    logger.warning(
                        f"Rate limit hit (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error("Rate limit error after all retries")
                    return "⚠️ API rate limit reached. Please wait a moment and try again. If this persists, consider:\n1. Waiting 1-2 minutes\n2. Using a different Google API key\n3. Switching to Vertex AI (set GOOGLE_GENAI_USE_VERTEXAI=1 in .env)"
            else:
                # Not a rate limit error, re-raise
                logger.error(f"Error during content generation: {e}")
                raise


# Sync wrapper for Streamlit
def generate_content(prompt: str, user_id: str = "default_user") -> str:
    return asyncio.run(async_generate_content(prompt, user_id))
