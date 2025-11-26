import asyncio
from functools import lru_cache
from typing import Any, Dict, Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part
import logging

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

            final_content = await self._collect_final_content(response_iter)
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

    # Helper to collect final content from async iterator
    async def _collect_final_content(self, response_iter: Any):
        final = None

        if hasattr(response_iter, "__aiter__"):
            async for part in response_iter:

                if hasattr(part, "content"):

                    final = part.content
                elif hasattr(part, "parts") or hasattr(part, "text"):
                    final = part
        else:
            if hasattr(response_iter, "content"):
                final = response_iter.content
            else:
                final = response_iter
        return final

    # Extract text from Content or Part objects
    def extract_text_from_content(self, content: Any) -> str:
        if content is None:
            return ""
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
