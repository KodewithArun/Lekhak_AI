import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from src.agents.content_creator_agent import content_creator_agent
from src.services.agent_clients import get_agent_client_cached
from src.config import APP_NAME, DB_URL


# Initialize runner and session service once
_session_service = DatabaseSessionService(db_url=DB_URL)
_runner = Runner(
    agent=content_creator_agent, app_name=APP_NAME, session_service=_session_service
)
_client = get_agent_client_cached(_runner, _session_service, APP_NAME)

# In-memory session cache for Streamlit app
_user_sessions = {}


async def async_generate_content(prompt: str, user_id: str = "default_user") -> str:
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


# Sync wrapper for Streamlit
def generate_content(prompt: str, user_id: str = "default_user") -> str:
    return asyncio.run(async_generate_content(prompt, user_id))
