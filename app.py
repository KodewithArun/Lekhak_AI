# streamlit_app.py
"""Simple Streamlit UI for Lekhak AI"""

import asyncio
import os
import streamlit as st

# ADK imports
from google.adk.runners import Runner
from google.genai.types import Content, Part
from src.agents.content_creator_agent import content_creator_agent
from src.utils.agent_runner import call_agent_async as async_call
from src.utils.loggers import get_logger

# Configuration
APP_NAME = os.getenv("APP_NAME")
DB_URL = os.getenv("DB_URL")
USER_ID = os.getenv("USER_ID")
logger = get_logger("streamlit_app")


# Persistent Runner (cached resource)
@st.cache_resource
def get_runner():
    """Create or retrieve a Runner instance for the session."""
    try:
        from google.adk.sessions import DatabaseSessionService

        session_service = DatabaseSessionService(db_url=DB_URL)
        runner = Runner(
            agent=content_creator_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        logger.info("Streamlit Runner initialized")
        return runner, session_service
    except Exception as e:
        logger.error(f"Failed to init Runner: {e}", exc_info=True)
        st.error(" Unable to start the AI backend.")
        st.stop()


# Helper to collect final content from async iterator
async def _collect_content(iter_obj):
    final = None
    if hasattr(iter_obj, "__aiter__"):
        async for part in iter_obj:
            if hasattr(part, "content"):
                final = part.content
    else:
        if hasattr(iter_obj, "content"):
            final = iter_obj.content
    return final


# UI
st.title("Lekhak AI")
user_input = st.text_area(
    "Your request", placeholder="eg. Write a LinkedIn post about AI", height=150
)
if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        runner, session_service = get_runner()

        async def get_or_create_session():
            existing = await session_service.list_sessions(
                app_name=APP_NAME, user_id=USER_ID
            )
            if existing and len(existing.sessions) > 0:
                return existing.sessions[0].id
            new = await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                state={"user_name": "Streamlit User", "content_history": []},
            )
            return new.id

        with st.spinner("Thinking..."):
            try:
                SESSION_ID = asyncio.run(get_or_create_session())
                # Run agent via utility (handles async generators)
                asyncio.run(async_call(runner, USER_ID, SESSION_ID, user_input))
                # Fetch final response for display
                response_iter = runner.run_async(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=Content(role="user", parts=[Part(text=user_input)]),
                )
                final_content = asyncio.run(_collect_content(response_iter))
                if final_content:
                    # Extract and display only the text parts
                    if hasattr(final_content, "parts"):
                        texts = [
                            part.text
                            for part in final_content.parts
                            if hasattr(part, "text")
                        ]
                        st.success("\n".join(texts))
                    else:
                        st.success(str(final_content))
                else:
                    st.info("No response returned.")
            except Exception as e:
                logger.error(f"Streamlit error: {e}", exc_info=True)
                st.error(f"Error: {e}")
