import requests
from typing import Dict, List
from pydantic import BaseModel, Field
from google.adk.tools import FunctionTool
from src.utils.loggers import get_logger
from src.config.settings import RITEKIT_API_KEY

logger = get_logger("ritekit_tool")


class HashtagInput(BaseModel):
    text: str = Field(..., description="Post text to analyze (max ~1000 chars)")
    max_hashtags: int = Field(
        6, ge=1, le=15, description="Number of hashtags to return"
    )
    platform: str = Field(
        "twitter", description="Social platform: twitter, instagram, linkedin, etc."
    )


def suggest_hashtags(
    text: str, max_hashtags: int = 8, platform: str = "twitter"
) -> Dict:
    """
    Generate trending and relevant hashtags using RiteKit API.

    Args:
        text (str): Rich context text (~50-200 chars recommended)
        max_hashtags (int): Number of hashtags to return (1-15)
        platform (str): Social media platform (twitter, instagram, linkedin, etc.)

    Returns:
        Dict: {
            original_text: str,
            suggested_hashtags: List[Dict[hashtag, exposure, color]],
            optimized_text: str,
            error: str | None
        }
    """
    logger.info(f"#️⃣ RiteKit: Generating {max_hashtags} hashtags for {platform}")

    if not RITEKIT_API_KEY:
        logger.error("❌ RITEKIT_API_KEY is missing!")
        return {"error": "RITEKIT_API_KEY missing", "suggested_hashtags": []}

    try:
        response = requests.get(
            "https://api.ritekit.com/v1/stats/hashtag-suggestions",
            params={
                "text": text,
                "maxHashtags": max_hashtags,
                "client_id": RITEKIT_API_KEY,
                "platform": platform,
            },
            timeout=12,
        )
        response.raise_for_status()
        data = response.json()

        raw = [
            {
                "hashtag": t.get("hashtag", "").strip(),
                "exposure": int(t.get("exposure", 0) or 0),
                "color": t.get("color", "#000000"),
            }
            for t in data.get("data", [])
        ]

        # Basic quality filters: remove empty, duplicates, generic or very low exposure
        stop_words = {
            "lab",
            "updates",
            "solutions",
            "solution",
            "savingtime",
            "savetime",
            "realtime",
        }

        seen = set()
        filtered = []
        for t in raw:
            tag = t["hashtag"].lstrip("#").lower()
            if not tag or tag in seen:
                continue
            if tag in stop_words:
                continue
            if t["exposure"] < 100:  # drop very low exposure tags
                continue
            seen.add(tag)
            filtered.append(t)

        # Sort by exposure desc and cap to requested count
        filtered.sort(key=lambda x: x["exposure"], reverse=True)
        hashtags = [
            {
                "hashtag": (
                    f"#{t['hashtag']}"
                    if not t["hashtag"].startswith("#")
                    else t["hashtag"]
                ),
                "exposure": t["exposure"],
                "color": t["color"],
            }
            for t in filtered[:max_hashtags]
        ]

        optimized_text = f"{text} " + " ".join(h["hashtag"] for h in hashtags)

        logger.info(f"✅ Generated {len(hashtags)} hashtags")
        for h in hashtags[:8]:
            logger.info(f"   {h['hashtag']} (exposure: {h['exposure']:,})")

        return {
            "original_text": text,
            "suggested_hashtags": hashtags,
            "optimized_text": optimized_text,
            "error": None,
        }

    except requests.exceptions.HTTPError as e:
        logger.error(
            f"❌ HTTP error: {e.response.status_code if e.response else 'N/A'}"
        )
        return {"error": str(e), "suggested_hashtags": []}
    except requests.exceptions.Timeout:
        logger.error("❌ Timeout: RiteKit API took longer than 12 seconds")
        return {"error": "API timeout", "suggested_hashtags": []}
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"error": str(e), "suggested_hashtags": []}


# ✅ Simple FunctionTool usage for your ADK version
ritekit_tool = FunctionTool(suggest_hashtags)
