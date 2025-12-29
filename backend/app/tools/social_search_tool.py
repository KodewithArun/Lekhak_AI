import requests
from typing import Dict, Any
from app.core.setting import SERPAPI_API_KEY, SERPAPI_BASE_URL
from app.utils.loggers import get_logger

logger = get_logger("social_search_tool")


def serp_platform_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Executes a SERP API search and returns structured results with source metadata.
    The Research Agent MUST decide what information it needs.

    Args:
        query (str): The exact search query written by the Research Agent.
        num_results (int): Number of results to fetch (default: 5).

    Returns:
        dict: Structured response containing:
            - query: The original search query
            - results: List of search results with title, url, snippet, domain
            - total_results: Number of results returned
            - error: Error message if search failed (optional)
    """
    logger.info(f" Research Agent Search Query: '{query}'")

    try:
        url = SERPAPI_BASE_URL
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results,
            "hl": "en",
            "safe": "active",
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        # Extract and structure organic results
        organic_results = raw_data.get("organic_results", [])
        structured_results = []

        for idx, result in enumerate(organic_results[:num_results], 1):
            # Extract domain from URL
            result_url = result.get("link", "")
            domain = ""
            if result_url:
                try:
                    from urllib.parse import urlparse

                    parsed = urlparse(result_url)
                    domain = parsed.netloc.replace("www.", "")
                except Exception:
                    domain = "unknown"

            structured_result = {
                "position": idx,
                "title": result.get("title", "No title"),
                "url": result_url,
                "snippet": result.get("snippet", "No description available"),
                "domain": domain,
                "displayed_link": result.get("displayed_link", domain),
            }
            structured_results.append(structured_result)

        logger.info(f"Found {len(structured_results)} results for query: '{query}'")

        return {
            "query": query,
            "results": structured_results,
            "total_results": len(structured_results),
            "search_metadata": {
                "engine": "google",
                "language": "en",
            },
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"SERP API request failed: {str(e)}")
        return {
            "query": query,
            "results": [],
            "total_results": 0,
            "error": f"Search failed: {str(e)}",
        }
    except Exception as e:
        logger.error(f"Unexpected error in SERP search: {str(e)}")
        return {
            "query": query,
            "results": [],
            "total_results": 0,
            "error": f"Unexpected error: {str(e)}",
        }
