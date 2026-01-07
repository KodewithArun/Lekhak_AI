import asyncio
import json
import logging
import random
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

        # Retry configuration
        max_retries = 3
        base_delay = 1.0
        max_delay = 10.0

        last_error = None

        for attempt in range(max_retries + 1):
            start_time = time.time()
            try:
                if attempt > 0:
                    self.logger.info(
                        f"Retry attempt {attempt}/{max_retries} for session {session_id}"
                    )

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
                last_error = exc
                error_str = str(exc).lower()

                # Check for transient errors (503 Service Unavailable, 429 Too Many Requests, overloaded)
                is_transient = (
                    "503" in error_str
                    or "429" in error_str
                    or "overloaded" in error_str
                    or "unavailable" in error_str
                    or "resourceexhausted" in error_str
                )

                if is_transient and attempt < max_retries:
                    # Calculate exponential backoff with jitter
                    delay = min(
                        base_delay * (2**attempt) + (random.random() * 0.5), max_delay
                    )
                    self.logger.warning(
                        f"Model overloaded or unavailable (Attempt {attempt+1}/{max_retries+1}). "
                        f"Retrying in {delay:.2f}s. Error: {exc}"
                    )
                    await asyncio.sleep(delay)
                else:
                    # Not transient or out of retries
                    self.logger.error(
                        f"Agent error after {attempt+1} attempts. Final error: {exc}",
                        exc_info=True,
                    )
                    return {"ok": False, "error": str(exc)}

        # Should not be reached if logic is correct, but purely safe return
        return {"ok": False, "error": str(last_error)}

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
                    if author == "blog_optimizer":
                        self.logger.info("Captured final blog post.")
                        try:
                            # Ensure it's valid JSON with 'final_content'
                            json.loads(content_text)
                            final_blog_content = content_text
                        except json.JSONDecodeError:
                            final_blog_content = json.dumps(
                                {"final_content": content_text}
                            )

                    elif author in ["optimized_social_content", "social_optimizer"]:
                        self.logger.info("Captured final social post from optimizer.")
                        try:
                            json.loads(content_text)
                            final_social_content = content_text
                        except json.JSONDecodeError:
                            final_social_content = json.dumps({"content": content_text})

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

                    title = blog_data.get("final_title") or blog_data.get("title", "")
                    meta = blog_data.get("final_meta_description") or blog_data.get(
                        "meta_description", ""
                    )
                    body = blog_data.get("final_content") or blog_data.get(
                        "content", ""
                    )

                    # New verification fields
                    sources = blog_data.get("references_for_verification", [])

                    parts = []
                    if title:
                        parts.append(f"# {title}\n")
                    if meta:
                        parts.append(f"{meta}\n")

                    parts.append(body)

                    if sources:
                        parts.append("\n---\n### Sources & References")
                        for s in sources:
                            parts.append(f"- {s}")

                    blog_content = "\n".join(parts).strip()
                except json.JSONDecodeError:
                    blog_content = content["blog"]

            # Social content
            if content.get("social"):
                try:
                    social_data = json.loads(content["social"])

                    # Support both new and old field names for robustness
                    caption = (
                        social_data.get("caption")
                        or social_data.get("optimized_caption")
                        or ""
                    )
                    main_content = (
                        social_data.get("content")
                        or social_data.get("optimized_content")
                        or social_data.get("main_content", "")
                    )
                    hashtags = (
                        social_data.get("hashtags")
                        or social_data.get("final_hashtags")
                        or []
                    )
                    cta = (
                        social_data.get("cta")
                        or social_data.get("platform_cta")
                        or social_data.get("call_to_action", "")
                    )
                    trending = social_data.get("trending_now", [])
                    sources_list = (
                        social_data.get("sources")
                        or social_data.get("source_references")
                        or []
                    )

                    parts = []
                    if caption:
                        parts.append(f"**Caption:** {caption}\n")

                    if main_content:
                        parts.append(main_content)

                    if cta:
                        parts.append(f"\n**CTA:** {cta}")

                    if hashtags:
                        hashtags_str = " ".join([f"#{h.lstrip('#')}" for h in hashtags])
                        parts.append(f"\n{hashtags_str}")

                    if trending:
                        trending_str = ", ".join(trending)
                        parts.append(f"\n{trending_str}")

                    # Handle structured source references
                    if sources_list:
                        parts.append("\n**Sources & References:**")
                        for ref in sources_list:
                            # Handle both dict (from JSON) and object (if pydantic model)
                            if isinstance(ref, dict):
                                s_str = f"{ref.get('source', 'Source')}: {ref.get('url', '')}"
                                if ref.get("claim"):
                                    s_str = f"{ref['claim']} ({s_str})"
                            else:
                                s_str = str(ref)
                            parts.append(f"- {s_str}")

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
