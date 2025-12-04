from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from google.adk.tools import FunctionTool
from serpapi import GoogleSearch
from src.utils.loggers import get_logger
from src.config.settings import SERPAPI_API_KEY

logger = get_logger("serpapi_tool")


class GoogleSearchInput(BaseModel):
    query: str = Field(
        ..., description="Google search query, e.g. 'Latest trends in AI technology'"
    )
    num: int = Field(10, ge=1, le=100, description="Number of results to return")
    allowed_domains: Optional[List[str]] = Field(
        default=None,
        description="Only return results from these domains (e.g., ['example.com']).",
    )
    required_keywords: Optional[List[str]] = Field(
        default=None,
        description="Words/phrases that must appear in title or snippet (case-insensitive).",
    )
    exclude_keywords: Optional[List[str]] = Field(
        default=None,
        description="Words/phrases that, if present, will exclude a result (case-insensitive).",
    )


def google_search(
    query: str,
    num: int = 3,
    allowed_domains: Optional[List[str]] = None,
    required_keywords: Optional[List[str]] = None,
    exclude_keywords: Optional[List[str]] = None,
) -> Dict:
    """
    Google Search using SerpAPI - returns top search results with key information.
    """
    logger.info(f"🔍 SerpAPI Query: '{query}' | num={num}")

    if not SERPAPI_API_KEY:
        logger.error("❌ SERPAPI_API_KEY is missing!")
        return {"error": "SERPAPI_API_KEY missing"}

    try:
        search_params = {
            "engine": "google",
            "q": query,
            "num": num,
            "api_key": SERPAPI_API_KEY,
        }

        search = GoogleSearch(search_params)
        results = search.get_dict()

        # Debug: Log the actual SerpAPI response status
        if "error" in results:
            logger.error(f" SerpAPI returned error: {results.get('error')}")
            return {"error": f"SerpAPI error: {results.get('error')}"}

        logger.debug(f" SerpAPI response keys: {list(results.keys())}")

        organic = results.get("organic_results", [])
        logger.debug(f"Raw organic_results count: {len(organic)}")
        # Detect explicit site: filter from query, prefer domain constraints
        site_domain: Optional[str] = None
        if " site:" in query:
            try:
                # naive parse: take text after 'site:' until space
                site_domain = query.split(" site:", 1)[1].split()[0].strip()
            except Exception:
                site_domain = None

        def domain_from_link(link: Optional[str]) -> Optional[str]:
            if not link:
                return None
            try:
                # simple extraction without urlparse to avoid extra deps
                no_scheme = link.split("//", 1)[-1]
                host = no_scheme.split("/", 1)[0]
                # strip port if any
                host = host.split(":", 1)[0]
                return host.lower()
            except Exception:
                return None

        def contains_any(text: str, keywords: List[str]) -> bool:
            t = text.lower()
            for k in keywords:
                if k and k.lower() in t:
                    return True
            return False

        def contains_all(text: str, keywords: List[str]) -> bool:
            t = text.lower()
            for k in keywords:
                if k and k.lower() not in t:
                    return False
            return True

        # Apply intent-focused filtering
        filtered: List[Dict] = []
        for r in organic:
            title = r.get("title", "") or ""
            snippet = r.get("snippet", "") or ""
            link = r.get("link")
            dom = domain_from_link(link)

            # Enforce explicit site:domain if present
            if site_domain and dom and site_domain.lower() not in dom:
                continue

            # Enforce allowed_domains if provided
            if allowed_domains:
                if not dom or not any(ad.lower() in dom for ad in allowed_domains):
                    continue

            # Exclude off-topic by keywords
            if exclude_keywords and contains_any(
                title + " " + snippet, exclude_keywords
            ):
                continue

            # Require at least one required keyword if provided
            if required_keywords and not contains_any(
                title + " " + snippet, required_keywords
            ):
                continue

            filtered.append(r)

        # If filtering removed all, fall back to original but cap to num
        final_results = (filtered if filtered else organic)[:num]
        knowledge_graph = results.get("knowledge_graph")
        answer_box = results.get("answer_box")

        logger.info(f"Returning {len(final_results)} results:")
        for i, r in enumerate(final_results, 1):
            logger.info(f"   [{i}] {r.get('title', 'No title')}")
            logger.info(f"       URL: {r.get('link', 'No link')}")
            logger.info(f"       Snippet: {r.get('snippet', 'No snippet')[:150]}...")

        response_data = {
            "organic_results": [
                {
                    "title": r.get("title"),
                    "link": r.get("link"),
                    "snippet": r.get("snippet"),
                }
                for r in final_results
            ],
            "knowledge_graph": knowledge_graph,
            "answer_box": answer_box,
            "error": None,
        }

        return response_data

    except Exception as e:
        logger.error(f"SerpAPI error: {str(e)}")
        return {"error": str(e)}


serp_tool = FunctionTool(google_search)
