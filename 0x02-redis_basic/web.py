#!/usr/bin/env python3
"""
Module for retrieving web pages and caching results in Redis.
"""

import requests
import redis
import time
from functools import wraps


redis_client = redis.Redis()

def cache_page(method):
    """Decorator to cache page content and track access count."""
    @wraps(method)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cached_content = redis_client.get(url)

        if cached_content:
            redis_client.incr(count_key)
            return cached_content.decode('utf-8')

        content = method(url)
        
        redis_client.setex(url, 10, content)

        redis_client.incr(count_key)

        return content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status() 
    return response.text
