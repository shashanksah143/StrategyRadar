import requests
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _get_metric_rating(metric_name, value):
    """
    Returns the standard Google Web Vitals rating (GOOD, NEEDS_IMPROVEMENT, POOR)
    based on the raw value. Returns None if value is None.
    
    All thresholds are strictly based on official Google documentation.
    """
    if value is None:
        return None

    # Ensure value is float for comparison
    try:
        val = float(value)
    except ValueError:
        return None

    if metric_name == "performance_score":
        # Source: https://web.dev/articles/performance-scoring
        # 90-100: Good (Green)
        # 50-89: Needs Improvement (Orange)
        # 0-49: Poor (Red)
        if val >= 90: return "GOOD"
        if val >= 50: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "LCP":
        # Largest Contentful Paint (ms)
        # Source: https://web.dev/articles/lcp
        # Good <= 2500ms
        # Needs Improvement <= 4000ms
        # Poor > 4000ms
        if val <= 2500: return "GOOD"
        if val <= 4000: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "CLS":
        # Cumulative Layout Shift (unitless)
        # Source: https://web.dev/articles/cls
        # Good <= 0.1
        # Needs Improvement <= 0.25
        # Poor > 0.25
        if val <= 0.1: return "GOOD"
        if val <= 0.25: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "INP":
        # Interaction to Next Paint (ms)
        # Source: https://web.dev/articles/inp
        # Good <= 200ms
        # Needs Improvement <= 500ms
        # Poor > 500ms
        if val <= 200: return "GOOD"
        if val <= 500: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "FCP":
        # First Contentful Paint (ms)
        # Source: https://web.dev/articles/fcp
        # Good <= 1800ms
        # Needs Improvement <= 3000ms
        # Poor > 3000ms
        if val <= 1800: return "GOOD"
        if val <= 3000: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "Speed_Index":
        # Speed Index (ms)
        # Source: https://web.dev/articles/speed-index
        # Good <= 3400ms
        # Needs Improvement <= 5800ms
        # Poor > 5800ms
        if val <= 3400: return "GOOD"
        if val <= 5800: return "NEEDS_IMPROVEMENT"
        return "POOR"

    elif metric_name == "Total_Blocking_Time":
        # Total Blocking Time (ms)
        # Source: https://web.dev/articles/tbt
        # Good <= 200ms
        # Needs Improvement <= 600ms
        # Poor > 600ms
        if val <= 200: return "GOOD"
        if val <= 600: return "NEEDS_IMPROVEMENT"
        return "POOR"

    return None

def _fetch_pagespeed_data(url, strategy, api_key):
    """
    Internal helper to fetch data for a single strategy (mobile/desktop).
    """
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    
    params = {
        "url": url,
        "strategy": strategy,
        "key": api_key,
        "category": "performance"
    }

    logger.info(f"Analyzing {strategy} performance for: {url}")

    try:
        response = requests.get(endpoint, params=params, timeout=60)
        
        if response.status_code != 200:
            logger.error(f"API Error {response.status_code} for {strategy}: {response.text}")
            return {"error": f"API Error {response.status_code}"}

        data = response.json()
        
        # 1. Loading Experience (Real User Data / CrUX)
        # This data comes from actual Chrome users. It may be missing for low-traffic sites.
        crux_metrics = {}
        loading_experience = data.get("loadingExperience", {})
        if loading_experience.get("metrics"):
            metrics = loading_experience["metrics"]
            
            # Helper to extract percentile and category
            def get_crux_val(key, name):
                metric_data = metrics.get(key, {})
                val = metric_data.get("percentile")
                return {
                    "value": val,
                    "rating": _get_metric_rating(name, val)
                }

            crux_metrics = {
                "INP_ms": get_crux_val("INTERACTION_TO_NEXT_PAINT", "INP"),
                "LCP_ms": get_crux_val("LARGEST_CONTENTFUL_PAINT", "LCP"),
                "CLS_score": get_crux_val("CUMULATIVE_LAYOUT_SHIFT", "CLS"),
                "overall_rating": loading_experience.get("overall_category")
            }

        # 2. Lighthouse Result (Lab Data - Simulated)
        lighthouse = data.get("lighthouseResult", {})
        audits = lighthouse.get("audits", {})
        categories = lighthouse.get("categories", {})
        
        # Performance Score (0-100)
        raw_score = categories.get("performance", {}).get("score")
        perf_score = int(raw_score * 100) if raw_score is not None else None

        # Helper to extract Lab Data
        def get_audit_val(key, name):
            audit = audits.get(key, {})
            # numericValue is the raw number (ms or score)
            raw_val = audit.get("numericValue")
            display_val = audit.get("displayValue")
            return {
                "displayValue": display_val,
                "numericValue": raw_val,
                "rating": _get_metric_rating(name, raw_val)
            }

        lab_metrics = {
            "performance_score": {
                "value": perf_score,
                "rating": _get_metric_rating("performance_score", perf_score)
            },
            "FCP": get_audit_val("first-contentful-paint", "FCP"),
            "LCP": get_audit_val("largest-contentful-paint", "LCP"),
            "CLS": get_audit_val("cumulative-layout-shift", "CLS"),
            "Speed_Index": get_audit_val("speed-index", "Speed_Index"),
            "Total_Blocking_Time": get_audit_val("total-blocking-time", "Total_Blocking_Time")
        }

        return {
            "lab_data": lab_metrics,
            "real_user_data": crux_metrics if crux_metrics else "Not enough traffic data"
        }

    except Exception as e:
        logger.error(f"Failed to analyze PageSpeed ({strategy}): {e}")
        return {"error": str(e)}

def analyze_web_vitals(url: str) -> dict:
    """
    Calls Google PageSpeed Insights API to fetch Core Web Vitals and Performance Score
    for BOTH Mobile and Desktop strategies.
    
    Args:
        url (str): The URL to analyze.
        
    Returns:
        dict: Combined results for mobile and desktop.
    """
    api_key = os.getenv("PAGESPEED_API_KEY")
    
    if not api_key:
        logger.error("PAGESPEED_API_KEY not found in environment variables.")
        return {"error": "Missing API Key"}

    # Fetch both strategies
    mobile_data = _fetch_pagespeed_data(url, "mobile", api_key)
    desktop_data = _fetch_pagespeed_data(url, "desktop", api_key)

    result = {
        "url": url,
        "analyzed_at": datetime.now().isoformat(),
        "mobile": mobile_data,
        "desktop": desktop_data
    }
    
    return result
