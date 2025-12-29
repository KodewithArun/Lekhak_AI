from serpapi import GoogleSearch
from app.core.setting import SERPAPI_API_KEY
from app.utils.loggers import get_logger
from typing import List, Dict, Any
from urllib.parse import urlparse

logger = get_logger("blog_tool")


def serp_google_search(
    query: str,
) -> dict:
    """
    Fetch Google search results using SerpAPI for SEO blog research.

    Returns structured data for keyword research, competitor analysis, and pain points.

    Args:
        query (str): Main search query.

    Returns:
        dict: Search data including:
            - organic_results
            - people_also_ask
            - related_searches
            - derived_insights (keywords, competitors, pain points)
            - status/error_message (only if an error occurs)
    """
    if not SERPAPI_API_KEY:
        logger.error("SerpAPI key not configured")
        return {"status": "error", "error_message": "SerpAPI key is not configured"}

    try:
        # SERPAPI parameters
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "hl": "en",
            "gl": "us",
            "num": 15,
        }

        logger.info(f"Performing SERPAPI search for query: '{query}'")

        search = GoogleSearch(params)
        data = search.get_dict()

        organic_results = data.get("organic_results", [])
        paa_questions = data.get("related_questions", [])
        related_searches = data.get("related_searches", [])

        #  extract questions
        questions = [p.get("question") for p in paa_questions]

        raw_data_for_extract = {
            "organic_results": organic_results,
            "people_also_ask": questions,
            "related_questions": questions,  # reuse same list
            "related_searches": [s.get("query") for s in related_searches],
        }

        # Perform extractions
        extracted_keywords = extract_seo_keywords(raw_data_for_extract, query)
        extracted_competitors = extract_competitors(raw_data_for_extract)
        extracted_pain_points = extract_pain_points(raw_data_for_extract)

        return {
            "organic_results": [
                {
                    "title": r.get("title"),
                    "snippet": r.get("snippet"),
                    "link": r.get("link"),
                }
                for r in organic_results
            ],
            "people_also_ask": raw_data_for_extract["people_also_ask"],
            "related_searches": raw_data_for_extract["related_searches"],
            "derived_insights": {
                "keywords": extracted_keywords
                or {
                    "primary_keywords": [query],
                    "secondary_keywords": [],
                    "long_tail_keywords": [],
                },
                "competitors": extracted_competitors or [],
                "pain_points": extracted_pain_points or [],
            },
        }

    except Exception as e:
        logger.exception(f"SERP fetch failed for query: '{query}'")
        return {
            "status": "error",
            "error_message": str(e),
            "organic_results": [],
            "people_also_ask": [],
            "related_searches": [],
            "derived_insights": {
                "keywords": {
                    "primary_keywords": [query],
                    "secondary_keywords": [],
                    "long_tail_keywords": [],
                },
                "competitors": [],
                "pain_points": [],
            },
        }


def extract_seo_keywords(
    serp_data: Dict[str, Any], main_query: str
) -> Dict[str, List[str]]:
    """Extract primary, secondary, and long-tail keywords from SERP data."""
    primary, secondary, long_tail = [], [], []

    related_searches = serp_data.get("related_searches", [])

    # Primary first 3 related searches
    for search in related_searches[:3]:
        if search and search.lower() != main_query.lower():
            primary.append(search)

    # Fallback to titles if no primary keywords
    if not primary:
        for r in serp_data.get("organic_results", [])[:3]:
            title = r.get("title")
            if title:
                primary.append(title)

    # Fallback to main query
    if not primary:
        primary = [main_query]

    # Long-tail from PAA
    long_tail = [q for q in serp_data.get("related_questions", []) if q]

    # Secondary from remaining related searches + titles
    secondary = related_searches[3:] or []
    for r in serp_data.get("organic_results", [])[:5]:
        title = r.get("title")
        if title and title not in primary:
            secondary.append(title)

    return {
        "primary_keywords": list(set(primary)),
        "secondary_keywords": list(set(secondary)),
        "long_tail_keywords": list(set(long_tail)),
    }


def extract_competitors(serp_data: Dict[str, Any]) -> List[str]:
    """Extract competitor names from SERP organic results."""
    competitors = []

    for r in serp_data.get("organic_results", []):
        link = r.get("link", "")
        if link:
            try:
                domain = urlparse(link).netloc
                brand = domain.replace("www.", "").split(".")[0]
                if brand and len(brand) > 3:
                    competitors.append(brand.capitalize())
            except Exception:
                pass

    return list(set(competitors))


def extract_pain_points(serp_data: Dict[str, Any]) -> List[str]:
    """Extract user pain points from PAA and related searches."""
    pain_points = []

    for q in serp_data.get("people_also_ask", []):
        q_lower = q.lower()
        if any(
            w in q_lower
            for w in [
                "fix",
                "issue",
                "problem",
                "slow",
                "error",
                "fail",
                "bad",
                "difficult",
            ]
        ):
            pain_points.append(q)

    for s in serp_data.get("related_searches", []):
        s_lower = s.lower()
        if any(w in s_lower for w in ["vs", "alternatives", "problems", "review"]):
            pain_points.append(s)

    return list(set(pain_points))
