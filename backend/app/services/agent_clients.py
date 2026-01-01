import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai.types import Content, Part

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
        self,
        user_id: str,
        session_id: Optional[str] = None,
        initial_state: Optional[Dict[str, Any]] = None,
    ):
        state = initial_state if initial_state is not None else {"user_name": user_id}
        # Pass session_id to session service if provided
        return await self.session_service.create_session(
            app_name=self.app_name, user_id=user_id, session_id=session_id, state=state
        )

    # Send message to agent and get response
    async def send_message(self, user_id: str, session_id: str, message):
        # Handle both string and dict (structured) messages
        if isinstance(message, str):
            if not message.strip():
                return {"ok": False, "error": "empty input"}
            user_content = Content(role="user", parts=[Part(text=message)])
        elif isinstance(message, dict):
            message_text = json.dumps(message)
            user_content = Content(role="user", parts=[Part(text=message_text)])
        else:
            return {"ok": False, "error": "invalid message type"}

        self.logger.info(
            f"Sending message to runner '{self.app_name}' (Session: {session_id})"
        )
        start_time = time.time()

        try:
            response_iter = self.runner.run_async(
                user_id=user_id, session_id=session_id, new_message=user_content
            )

            response_iter = await _maybe_await(response_iter)

            # Collect both blog and social content
            final_content = await self._collect_parallel_content(response_iter)

            elapsed_time = time.time() - start_time
            self.logger.info(f"Agent response received in {elapsed_time:.2f}s")

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
                if event.is_final_response() and event.content and event.content.parts:
                    author = event.author
                    content_text = event.content.parts[0].text

                    # Wrap blog content in JSON for consistency
                    if author == "blog_final_output":
                        self.logger.info("Captured final blog post.")
                        try:
                            # Ensure it's valid JSON with 'final_content'
                            json.loads(content_text)
                            final_blog_content = content_text
                        except json.JSONDecodeError:
                            final_blog_content = json.dumps(
                                {"final_content": content_text}
                            )

                    elif author == "optimized_social_content":
                        self.logger.info("Captured final social post from optimizer.")
                        try:
                            json.loads(content_text)
                            final_social_content = content_text
                        except json.JSONDecodeError:
                            final_social_content = json.dumps({"caption": content_text})

                    elif author == "router_agent":
                        self.logger.info("Captured message from router agent.")
                        clarification_message = content_text

        # If only clarification is available, return it
        if (
            clarification_message
            and not final_blog_content
            and not final_social_content
        ):
            return {"clarification": clarification_message}

        return {"blog": final_blog_content, "social": final_social_content}

    # Extract text from blog/social content
    def extract_text_from_content(self, content: Any) -> str:
        if content is None:
            return ""

        if isinstance(content, dict):
            # Return clarification if exists
            if content.get("clarification"):
                return content["clarification"]

            blog_content = ""
            social_content = ""

            # Blog content
            if content.get("blog"):
                try:
                    blog_data = json.loads(content["blog"])
                    blog_content = blog_data.get("final_content", "")
                except json.JSONDecodeError:
                    blog_content = content["blog"]

            # Social content
            if content.get("social"):
                try:
                    social_data = json.loads(content["social"])
                    caption = social_data.get("optimized_caption") or social_data.get(
                        "caption", ""
                    )
                    main_content = social_data.get(
                        "optimized_content"
                    ) or social_data.get("main_content", "")
                    hashtags = social_data.get("final_hashtags") or social_data.get(
                        "hashtags", []
                    )
                    cta = social_data.get("platform_cta") or social_data.get(
                        "call_to_action", ""
                    )

                    hashtags_str = (
                        " ".join([f"#{h}" for h in hashtags]) if hashtags else ""
                    )

                    parts = []
                    if caption:
                        parts.append(f"**Caption:** {caption}")
                    if main_content:
                        parts.append(f"\n{main_content}")

                    social_content = "\n".join(parts).strip()
                except json.JSONDecodeError:
                    social_content = content["social"]

            # Combine blog and social content
            output = ""
            if social_content:
                output += social_content
            if blog_content:
                output += ("\n" if output else "") + blog_content

            return output.strip()

        # Fallback: if content is string or parts
        if hasattr(content, "parts"):
            txts = [p.text for p in content.parts if hasattr(p, "text")]
            return "\n".join(txts)
        if isinstance(content, str):
            return content
        return str(content)


# Helper to await if object is coroutine or awaitable
async def _maybe_await(obj: Any):
    if asyncio.iscoroutine(obj) or hasattr(obj, "__await__"):
        return await obj
    return obj
