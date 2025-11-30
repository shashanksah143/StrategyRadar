import requests
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_competitor_sitemap(base_url: str) -> str:
    """
    Fetches the sitemap XML content for a given competitor URL.
    
    Args:
        base_url (str): The home URL of the competitor.

    Returns:
        str: The raw XML content of the sitemap, or an error message.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Ensure base_url ends with /
    if not base_url.endswith('/'):
        base_url += '/'
        
    sitemap_url = urljoin(base_url, 'sitemap.xml')
    logger.info(f"Fetching raw sitemap from: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Check if the content is actually XML (basic check)
        if "<" not in response.text:
             return f"Error: The content at {sitemap_url} does not look like XML."

        # Return the raw XML string for the LLM to parse
        return response.text

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch sitemap for {base_url}: {e}")
        return f"Error: Could not fetch sitemap. {str(e)}"