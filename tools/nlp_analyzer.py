import requests
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from typing import Dict, Any, List, Tuple

def clean_text(html_content: str) -> str:
    """
    Parses HTML, removes tags, scripts, styles, and special characters.
    Returns clean, lowercase plain text.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 1. Remove script and style elements and structural/meta elements
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
        # Simplified error handling without logger
        # print(f"Error cleaning HTML: {e}") 
        return ""

def fetch_content(url: str) -> str or None:
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
            
        # print(f"Crawling: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        # Simplified error handling without logger
        # print(f"Failed to fetch {url}: {e}")
        return None

def _get_tfidf_scores(corpus: List[str]) -> Dict[str, float]:
    """
    Internal helper to calculate TF-IDF scores for a single document.
    Returns a dictionary of term -> score (unsorted).
    """
    try:
        # ngram_range=(1, 3): Captures single words up to 3-word phrases
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 3), 
            stop_words='english', 
            max_df=1.0, 
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = np.array(vectorizer.get_feature_names_out())

        scores = tfidf_matrix[0].toarray()[0]
        # Get indices of top 50 scores
        top_n_indices = scores.argsort()[-50:][::-1]
        
        top_terms: Dict[str, float] = {}
        for idx in top_n_indices:
            term = feature_names[idx]
            score = round(float(scores[idx]), 4)
            if score > 0:
                top_terms[term] = score
        return top_terms

    except Exception as e:
        # Simplified error handling without logger
        # print(f"Error during TF-IDF calculation: {e}")
        return {}


def _get_ngram_density(corpus: List[str]) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Internal helper to calculate frequency and density for 1, 2, 3, 4-grams.
    Returns a dictionary structured as: { '1gram': {term: {'count': N, 'density': D}, ...} } (unsorted).
    """
    density_results: Dict[str, Dict[str, Dict[str, Any]]] = {}
    
    # Loop through 1-gram to 4-gram
    for n in [1, 2, 3, 4]:
        ngram_key = f"{n}gram"
        
        try:
            # CountVectorizer calculates raw frequency counts
            vectorizer = CountVectorizer(ngram_range=(n, n), stop_words='english')
            dtm = vectorizer.fit_transform(corpus)
            features = np.array(vectorizer.get_feature_names_out())
            
            row = dtm[0].toarray()[0]
            total_words_in_doc = row.sum() # Total n-grams in this specific document
            
            # Get top 50 indices by count
            top_indices = row.argsort()[-50:][::-1]
            
            site_ngram_data: Dict[str, Dict[str, Any]] = {}
            
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
            
            density_results[ngram_key] = site_ngram_data
                
        except ValueError:
            # Simplified error handling without logger
            # print(f"Could not generate {n}-grams (corpus might be too small).")
            density_results[ngram_key] = {}
                 
    return density_results

def sort_analysis_results(data_dict: Dict[str, float or Dict[str, Any]], sort_by_key: str = None) -> List[Tuple]:
    """
    Sorts a dictionary of terms in descending order by their value (score or count/density).

    :param data_dict: The dictionary of terms (str) to their values (float or dict).
    :param sort_by_key: If the values are dictionaries (e.g., in n-gram density), 
                        specify the key to sort by ('count' or 'density').
    :return: A list of tuples (term, value) or (term, count, density), sorted descendingly.
    """
    if not data_dict:
        return []

    if sort_by_key is None:
        # For TF-IDF, values are floats (the scores)
        # Sort by the float value itself
        sorted_list = sorted(data_dict.items(), key=lambda item: item[1], reverse=True)
        # item[0] is the term (n-gram), item[1] is the score
        return sorted_list
    else:
        # For N-Gram Density, values are dictionaries {"count": X, "density": Y}
        # Sort by the specified key ('count' or 'density')
        sorted_list = sorted(data_dict.items(), key=lambda item: item[1].get(sort_by_key, 0), reverse=True)
        
        # Format the output to be a flat tuple: (term, count, density)
        formatted_list = [
            (term, data['count'], data['density']) 
            for term, data in sorted_list
        ]
        return formatted_list


def analyze_content(base_url: str) -> Dict[str, Any]:
    """
    Main function: Fetches, cleans, analyzes, and returns sorted results for a URL.
    """
    
    # 1. Fetch & Clean Content
    raw_html = fetch_content(base_url)
    if not raw_html:
        return {"status": "error", "message": f"Could not fetch content for {base_url}"}

    cleaned_text = clean_text(raw_html)
    if not cleaned_text:
        return {"status": "error", "message": f"No extractable text found for {base_url}"}

    # The corpus for the single URL analysis
    corpus = [cleaned_text]

    # 2. Run Calculations
    # print(f"Running content analysis for: {base_url}")
    
    # These return the top N terms as UNORDERED dictionaries
    tfidf_data = _get_tfidf_scores(corpus)
    density_data = _get_ngram_density(corpus)

    # 3. Sort Results 🥇
    
    # Sort TF-IDF by the score (descending)
    # Result: List of tuples (term, tfidf_score)
    sorted_tfidf = sort_analysis_results(tfidf_data)
    
    # Sort N-Grams by 'count' (descending)
    # Result: Dict structured as { '1gram': [(term, count, density), ...], ...}
    sorted_density_data = {}
    for n_key, n_data in density_data.items():
        # Sort each n-gram level by the 'count' (most occurring first)
        sorted_density_data[n_key] = sort_analysis_results(n_data, sort_by_key='count')


    # 4. Merge and Return Results
    return {
        "url": base_url,
        "status": "success",
        # Results are now SORTED LISTS, ready for display
        "tf_idf_top_50_sorted": sorted_tfidf, 
        "keyword_density_sorted_by_count": sorted_density_data
    }