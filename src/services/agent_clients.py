# src/services/agent_clients.py

import asyncio
from functools import lru_cache
from typing import Any, Dict, Optional, Tuple
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part
import logging
import json

logger = logging.getLogger("agent_client")


class AgentClient:
    def __init__(
        self,
        runner: Runner,
        session_service: DatabaseSessionService,
        app_name: str = "agents",
    ):
        self.runner = runner
        self.session_service = session_service
        self.app_name = app_name
        self.logger = logger

    # Create or get existing session
    async def get_or_create_session(
        self, user_id: str, initial_state: Optional[Dict[str, Any]] = None
    ):
        state = initial_state or {"user_name": user_id, "content_history": []}
        return await self.session_service.create_session(
            app_name=self.app_name, user_id=user_id, state=state
        )

    # Send message to agent and get response
    async def send_message(self, user_id: str, session_id: str, text: str):
        if not text.strip():
            return {"ok": False, "error": "empty input"}

        user_content = Content(role="user", parts=[Part(text=text)])
        try:
            response_iter = self.runner.run_async(
                user_id=user_id, session_id=session_id, new_message=user_content
            )

            response_iter = await _maybe_await(response_iter)

            #  Collect both blog and social content
            final_content = await self._collect_parallel_content(response_iter)

            if final_content:
                return {
                    "ok": True,
                    "content": self.extract_text_from_content(final_content),
                    "raw": final_content,
                }
            return {"ok": False, "error": "no content returned"}
        except Exception as exc:
            self.logger.error("Agent error", exc_info=True)
            return {"ok": False, "error": str(exc)}

    # Collect content from parallel pipelines
    async def _collect_parallel_content(
        self, response_iter: Any
    ) -> Optional[Dict[str, Any]]:
        final_blog_content = None
        final_social_content = None
        clarification_message = None

        if hasattr(response_iter, "__aiter__"):
            async for event in response_iter:
                # Check if the event is a final response from one of our presenter agents
                if event.is_final_response() and event.content and event.content.parts:
                    author = event.author
                    content_text = event.content.parts[0].text

                    # Store the content based on the author
                    if author == "blog_presenter":
                        self.logger.info("Captured final blog post.")
                        final_blog_content = content_text
                    elif author == "social_presenter":
                        self.logger.info("Captured final social post.")
                        final_social_content = content_text
                    elif author == "router_agent":
                        # Capture clarification or error messages from router
                        self.logger.info("Captured message from router agent.")
                        clarification_message = content_text

        # If only clarification is available, return it
        if (
            clarification_message
            and not final_blog_content
            and not final_social_content
        ):
            return {"clarification": clarification_message}

        # Return a dictionary containing both results
        return {"blog": final_blog_content, "social": final_social_content}

    # Handle the new dictionary structure
    def extract_text_from_content(self, content: Any) -> str:
        if content is None:
            return ""

        # Handle the new dictionary structure from _collect_parallel_content
        if isinstance(content, dict):
            # Check for clarification message first
            if content.get("clarification"):
                return content["clarification"]

            blog_content = ""
            social_content = ""

            if content.get("blog"):
                try:
                    # Parse the JSON string to get the clean text
                    blog_data = json.loads(content["blog"])
                    blog_content = blog_data.get("final_content", "")
                except json.JSONDecodeError:
                    blog_content = content["blog"]  # Fallback if not valid JSON

            if content.get("social"):
                try:
                    # Parse the JSON string to get the clean text
                    social_data = json.loads(content["social"])
                    social_content = social_data.get("final_content", "")
                except json.JSONDecodeError:
                    social_content = content["social"]  # Fallback if not valid JSON

            # Combine them into a single, well-formatted string for display
            output = ""
            if social_content:
                output += social_content
                output += "\n==============================\n\n"
            if blog_content:
                output += blog_content
                output += "\n============================\n"

            return output.strip()

        # Fallback for old content structure (if you ever run a single pipeline)
        if hasattr(content, "parts"):
            txts = []
            for p in content.parts:
                if hasattr(p, "text"):
                    txts.append(str(p.text))
            return "\n".join(txts)
        if isinstance(content, str):
            return content
        return str(content)


# Helper to await if object is coroutine or awaitable
async def _maybe_await(obj: Any):
    if asyncio.iscoroutine(obj) or hasattr(obj, "__await__"):
        return await obj
    return obj


# Cached agent client factory
@lru_cache(maxsize=8)
def get_agent_client_cached(
    runner: Runner, session_service: DatabaseSessionService, app_name: str = "agents"
):
    return AgentClient(runner, session_service, app_name)
