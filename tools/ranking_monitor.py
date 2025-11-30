import os
import json
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_indian_organic_results(keyword):
    """
    Fetches Top 10 Google Search results for India (English).
    Reads API key from environment variable 'SERPAPI_KEY'.
    Returns a JSON string.
    """
    
    # 1. Get Key from Env
    api_key = os.getenv("SERPAPI_KEY")
    
    if not api_key:
        return json.dumps({
            "error": "Missing API Key. Please set SERPAPI_KEY in your .env file or environment variables."
        })

    # 2. Configure for India (gl=in) and English (hl=en)
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": api_key,
        "num": 10,       # Request top 10
        "gl": "in",      # Geo-location: India
        "hl": "en",      # Language: English
        "google_domain": "google.co.in" # Force Google India domain
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # 3. specific extraction based on your provided structure
        organic_results = results.get("organic_results", [])
        
        cleaned_data = []
        
        # We slice [:10] to ensure we only process the top 10
        for item in organic_results[:10]:
            entry = {
                "position": item.get("position"),
                "title": item.get("title"),
                "url": item.get("link"), # Mapped from 'link' in your raw structure
                "snippet": item.get("snippet", "No description available")
            }
            cleaned_data.append(entry)

        # Return formatted JSON
        return json.dumps(cleaned_data, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})