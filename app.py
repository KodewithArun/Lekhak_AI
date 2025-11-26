# streamlit_app.py
"""Simple Streamlit UI for Lekhak AI"""

import asyncio
import streamlit as st
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# ADK imports
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part
from src.agents.content_creator_agent import content_creator_agent
from src.utils.loggers import get_logger

logger = get_logger("streamlit_app")

APP_NAME = os.getenv("APP_NAME", "agents")
USER_ID = os.getenv("USER_ID", "streamlit_user")
DB_URL = os.getenv("DB_URL")


@st.cache_resource
def get_runner():
    """Create or retrieve a Runner instance."""
    session_service = DatabaseSessionService(db_url=DB_URL)
    runner = Runner(
        agent=content_creator_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    return runner, session_service


async def _collect_content(iter_obj):
    """Collect the final content from the async generator."""
    final = None
    async for part in iter_obj:
        if hasattr(part, "content"):
            final = part.content
    return final


async def get_or_create_session(session_service):
    """Create a session once and store in session_state."""
    if "session_id" in st.session_state:
        return st.session_state["session_id"]

    new = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={"user_name": "Streamlit User", "content_history": []},
    )

    st.session_state["session_id"] = new.id
    return new.id


# UI
st.title("Lekhak AI")
user_input = st.text_area("Your request", height=150)

if st.button("Generate"):
    if not user_input.strip():
        st.warning("Please enter a request.")
    else:
        runner, session_service = get_runner()

        with st.spinner("Thinking..."):
            try:
                # Get a persistent session ID
                SESSION_ID = asyncio.run(get_or_create_session(session_service))

                # Run the agent only once
                response_iter = runner.run_async(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=Content(role="user", parts=[Part(text=user_input)]),
                )

                final_content = asyncio.run(_collect_content(response_iter))

                if final_content and hasattr(final_content, "parts"):
                    texts = [p.text for p in final_content.parts if hasattr(p, "text")]
                    st.success("\n".join(texts))
                else:
                    st.info("No response returned.")

            except Exception as e:
                logger.error(f"Streamlit error: {e}", exc_info=True)
                st.error(f"Error: {e}")
