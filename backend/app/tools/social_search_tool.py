import os
from serpapi import GoogleSearch
from google.adk.tools import FunctionTool
from app.core.setting import SERPAPI_API_KEY
from app.utils.loggers import get_logger


logger = get_logger("SerpApi Tool")


def serp_api_search(query: str) -> dict:
    """
    Performs a web search using the SerpApi and returns the full result dictionary.
    The 'query' parameter is the search term.
    """
    if SERPAPI_API_KEY is None:
        logger.error(
            "SerpApi API key is not configured. Please set the SERPAPI_API_KEY environment variable."
        )
        return {"error": "SerpApi API key is not configured."}

    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": SERPAPI_API_KEY,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        logger.info(f"Successfully performed SerpApi search for query: '{query}'")
        return results
    except Exception as e:
        logger.error(f"Error during SerpApi search: {e}")

        return {"error": str(e)}


serp_search_tool = FunctionTool(func=serp_api_search)

logger.info("SerpApi search tool initialized.")
