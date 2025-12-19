from serpapi import GoogleSearch
from app.core.setting import SERPAPI_API_KEY
from app.utils.loggers import get_logger
from typing import Optional, List, Dict, Any


logger = get_logger("blog_tool")


def serp_google_search(
    query: str, company_name: Optional[str] = None, product_name: Optional[str] = None
) -> dict:
    """
    Fetch Google search results using SerpAPI for SEO blog research.

    Creates a clean and SEO-friendly search query based on the given topic,
    product, and optional company name, then returns structured search data
    for keyword research and competitor analysis.

    Args:
        query (str): Main blog topic or primary search keyword.
        company_name (Optional[str]): Company or brand name to guide relevance.
        product_name (Optional[str]): Product or service name to refine results.

    Returns:
        dict: Search data including:
            - organic_results: Titles, snippets, and links from top results
            - people_also_ask: Common user questions (long-tail keywords)
            - related_searches: Related search suggestions (secondary keywords)
            - status/error_message: Included only if an error occurs
    """
    # Construct final query
    if company_name and product_name:
        final_query = f'"{product_name}" {company_name} {query}'
    elif product_name:
        final_query = f'"{product_name}" {query}'
    else:
        final_query = query

    if not SERPAPI_API_KEY:
        logger.error("SerpAPI key not configured")
        return {"status": "error", "error_message": "SerpAPI key is not configured"}
    try:
        # SERPAPI parameters
        params = {
            "q": final_query,
            "api_key": SERPAPI_API_KEY,
            "engine": "google",
            "hl": "en",
            "gl": "us",
            "num": 15,
        }

        search = GoogleSearch(params)
        data = search.get_dict()

        organic_results = data.get("organic_results", [])
        paa_questions = data.get("related_questions", [])
        related_searches = data.get("related_searches", [])

        return {
            "organic_results": [
                {
                    "title": r.get("title"),
                    "snippet": r.get("snippet"),
                    "link": r.get("link"),
                }
                for r in organic_results
            ],
            "people_also_ask": [p.get("question") for p in paa_questions],
            "related_searches": [s.get("query") for s in related_searches],
        }

    except Exception as e:
        logger.exception(f"SERP fetch failed for query: '{final_query}'")
        return {"status": "error", "error_message": str(e)}


def extract_seo_keywords(
    serp_data: Dict[str, Any],
    main_query: str,
    product_name: Optional[str] = None,
) -> Dict[str, List[str]]:
    """
    Extract and classify SEO keywords from SERP data.

    Uses SERP results to group keywords into primary, secondary,
    and long-tail categories based on search intent and relevance.

    Args:
        serp_data (dict): Structured SERP response from serp_google_search.
        main_query (str): Main topic or primary SEO keyword.
        product_name (Optional[str]): Product or service name used
            to filter relevant keyword phrases.

    Returns:
        dict: Keyword groups including:
            - primary_keywords: Main keyword representing core intent
            - secondary_keywords: Related and supporting keywords
            - long_tail_keywords: Question-based, detailed search queries
    """

    primary = [main_query]

    secondary = []
    long_tail = []

    # Long-tail from PAA
    for q in serp_data.get("people_also_ask", []):
        if q:
            long_tail.append(q)

    # Secondary from related searches
    for q in serp_data.get("related_searches", []):
        if q:
            secondary.append(q)

    # Enrich secondary from organic titles for safe filtering
    for r in serp_data.get("organic_results", [])[:5]:
        title = r.get("title", "")
        if title and product_name and product_name.lower() in title.lower():
            secondary.append(title)

    return {
        "primary_keywords": primary[:1],
        "secondary_keywords": list(set(secondary))[:5],
        "long_tail_keywords": list(set(long_tail))[:5],
    }


def analyze_pain_points(features: List[str], audience: str) -> Dict[str, List[str]]:
    """
    Identify user pain points based on product features and target audience.

    Translates key product features into common problems and challenges
    faced by the target audience, helping define strong content angles
    for SEO blogs and product-focused articles.

    Args:
        features (List[str]): Key product features or capabilities.
        audience (str): Target user group or customer segment.

    Returns:
        dict: Contains:
            - pain_points: List of user problems and challenges
              derived from missing or weak features
    """
    pain_points = []

    for feature in features:
        pain_points.extend(
            [
                f"{audience} face inefficiencies without {feature}",
                f"Manual workflows increase cost and time when {feature} is missing",
                f"Lack of {feature} leads to inconsistent results for {audience}",
            ]
        )

    return {"pain_points": list(set(pain_points))[:6]}


def competitor_gap_analysis(
    organic_results: List[Dict[str, Any]], product_features: List[str]
) -> Dict[str, Any]:
    """
    Analyze competitors and content gaps for blog research.

    Extract competitor products from SERP titles and identify
    which product features/topics are not covered by competitors.

    Args:
        organic_results (List[dict]): SERP results containing 'title' and 'link'.
        product_features (List[str]): Key features/topics of your product.

    Returns:
        dict: {
            'competitor_names': List of competitor products found in SERP,
            'competitor_gaps': List of product features not mentioned in competitor content
        }
    """
    competitor_names: List[str] = []
    covered_content: set = set()

    for result in organic_results:
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        if not title:
            continue

        # Extract competitor product/brand from title
        competitor_name = title.split(" review")[0].split("|")[0].strip()
        if competitor_name:
            competitor_names.append(competitor_name)

        # Track words/topics mentioned in competitor content
        for word in (title + " " + snippet).split():
            covered_content.add(word.lower())

    # Identify features not mentioned in any competitor content
    competitor_gaps = [
        feature
        for feature in product_features
        if feature.lower() not in covered_content
    ]

    return {
        "competitor_names": list(set(competitor_names)),
        "competitor_gaps": competitor_gaps,
    }
