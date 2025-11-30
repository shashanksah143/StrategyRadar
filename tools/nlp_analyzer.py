import requests
from bs4 import BeautifulSoup
import re
import logging
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_text(html_content):
    """
    Parses HTML, removes tags, scripts, styles, and special characters.
    Returns clean, lowercase plain text.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Remove script and style elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav', 'meta', 'noscript']):
            script_or_style.decompose()

        # 2. Get text with separator to avoid merging words
        text = soup.get_text(separator=' ')

        # 3. Regex cleaning: Keep only letters and spaces (remove numbers/punctuation)
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # 4. Collapse multiple spaces and convert to lower case
        text = re.sub(r'\s+', ' ', text).strip().lower()

        return text
    except Exception as e:
        logger.error(f"Error cleaning HTML: {e}")
        return ""

def fetch_content(url):
    """
    Fetches the homepage content with a timeout and user-agent.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # Ensure URL schema
        if not url.startswith('http'):
            url = 'https://' + url
            
        logger.info(f"Crawling: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

def _get_tfidf_scores(corpus, valid_urls):
    """Internal helper to calculate TF-IDF scores."""
    try:
        # ngram_range=(1, 3): Captures "biodata" (1), "wedding biodata" (2)
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 3), 
            stop_words='english', 
            max_df=0.85, 
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = np.array(vectorizer.get_feature_names_out())

        results = {}

        # Extract Top 100 Terms per Site
        for i, url in enumerate(valid_urls):
            row = tfidf_matrix[i]
            scores = row.toarray()[0]
            # Get indices of top 100 scores
            top_n_indices = scores.argsort()[-100:][::-1]
            
            top_terms = {}
            for idx in top_n_indices:
                term = feature_names[idx]
                score = round(float(scores[idx]), 3)
                if score > 0:
                    top_terms[term] = score
            
            results[url] = top_terms
        return results

    except Exception as e:
        logger.error(f"Error during TF-IDF calculation: {e}")
        return {url: {} for url in valid_urls}

def _get_ngram_density(corpus, valid_urls):
    """Internal helper to calculate frequency and density for 1, 2, 3, 4-grams."""
    density_results = {url: {} for url in valid_urls}
    
    # Loop through 1-gram to 4-gram
    for n in [1, 2, 3, 4]:
        ngram_key = f"{n}gram"
        
        try:
            # CountVectorizer calculates raw frequency counts
            vectorizer = CountVectorizer(ngram_range=(n, n), stop_words='english')
            dtm = vectorizer.fit_transform(corpus)
            features = np.array(vectorizer.get_feature_names_out())
            
            for i, url in enumerate(valid_urls):
                row = dtm[i].toarray()[0]
                total_words_in_doc = row.sum() # Total n-grams in this specific document
                
                # Get top 50 indices by count
                top_indices = row.argsort()[-50:][::-1]
                
                site_ngram_data = {}
                
                for idx in top_indices:
                    count = int(row[idx])
                    if count > 0:
                        term = features[idx]
                        # Density = (Count of this phrase / Total phrases in doc)
                        density = round(count / total_words_in_doc, 5) if total_words_in_doc > 0 else 0
                        
                        site_ngram_data[term] = {
                            "count": count,
                            "density": density
                        }
                
                if ngram_key not in density_results[url]:
                    density_results[url][ngram_key] = {}
                
                density_results[url][ngram_key] = site_ngram_data
                
        except ValueError:
            # Handles cases where a document is too short for 4-grams
            logger.warning(f"Could not generate {n}-grams (corpus might be too small).")
            for url in valid_urls:
                 density_results[url][ngram_key] = {}
                 
    return density_results

def analyze_competitors_content(file_path="data/competitors.txt"):
    """
    Main function:
    1. Reads URLs.
    2. Fetches & Cleans content (Corpus creation).
    3. Runs TF-IDF Analysis (Top 100).
    4. Runs N-Gram Density Analysis (Top 50 for 1,2,3,4-grams).
    5. Returns a merged dictionary.
    """
    
    # 1. Read URLs
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {}

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        logger.warning("No URLs found in file.")
        return {}

    # 2. Build Corpus (Fetch once, use multiple times)
    corpus = []
    valid_urls = []

    for url in urls:
        raw_html = fetch_content(url)
        if raw_html:
            cleaned_text = clean_text(raw_html)
            if cleaned_text:
                corpus.append(cleaned_text)
                valid_urls.append(url)
            else:
                logger.warning(f"No text extracted from {url}")

    if not corpus:
        return {}

    # 3. Run Calculations
    logger.info("Running TF-IDF Analysis...")
    tfidf_data = _get_tfidf_scores(corpus, valid_urls)
    
    logger.info("Running N-Gram Density Analysis...")
    density_data = _get_ngram_density(corpus, valid_urls)

    # 4. Merge Results
    final_results = {}
    for url in valid_urls:
        final_results[url] = {
            "tf_idf_top_100": tfidf_data.get(url, {}),
            "keyword_density": density_data.get(url, {})
        }

    return final_results