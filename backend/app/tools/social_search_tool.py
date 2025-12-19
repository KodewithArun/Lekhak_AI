"""Social Media Search Tool using SERP API Performs searches for social media trends and content using SERP API"""

import requests
from app.core.setting import SERPAPI_API_KEY, SERPAPI_BASE_URL


def serp_platform_search(query: str, platform: str, num_results: int = 5) -> dict:
    """
    Performs a SERP API search for a specific platform.
    Returns structured JSON results with title, snippet, URL.
    """
    url = SERPAPI_BASE_URL
    params = {
        "q": f"{query} site:{platform}",  # platform-specific search
        "api_key": SERPAPI_API_KEY,
        "num": num_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
