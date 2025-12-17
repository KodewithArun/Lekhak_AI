# app/tools/hashtag_tool.py

import requests
from typing import Dict, List
from google.adk.tools import FunctionTool
from app.core.setting import RITEKIT_API_URL, RITEKIT_CLIENT_ID
from app.utils.loggers import get_logger


logger = get_logger("Ritkit Initialized")


def get_trending_hashtags(query: str, limit: int = 10) -> Dict[str, List[str]]:
    """
    Fetch trending hashtags for a query using RiteKit API.
    """
    params = {
        "client_id": RITEKIT_CLIENT_ID,
        "query": query,
        "limit": limit,
    }
    try:
        response = requests.get(RITEKIT_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        hashtags = [tag.get("tag") for tag in data.get("tags", []) if tag.get("tag")]
        return {"trendinghashtags": hashtags}
    except Exception as e:
        logger.error(f"Error fetching hashtags from RiteKit: {e}")
        return {"trendinghashtags": [], "error": str(e)}


hashtag_tool = FunctionTool(func=get_trending_hashtags)

logger.info("up to here hastag tool initialized")
