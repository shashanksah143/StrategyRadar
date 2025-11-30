from google.genai import types


def get_http_retry_config() -> types.HttpRetryOptions:
    """
    Returns the HTTP retry configuration for API calls.
    
    Returns:
        types.HttpRetryOptions: Configuration with:
            - 5 maximum retry attempts
            - Exponential backoff with base 7
            - 1 second initial delay
            - Retries on HTTP status codes 429, 500, 503, 504
    """
    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
    )
    return retry_config