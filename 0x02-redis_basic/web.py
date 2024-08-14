#!/usr/bin/env python3
"""
Web module for fetching and caching web pages.
"""

import redis
import requests
from functools import wraps
from typing import Callable


def cache_and_track(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of
    a function and track how many times it's called.

    Args:
        expiration (int): Expiration time for the cache in seconds.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            redis_client = redis.Redis()
            count_key = f"count:{url}"
            content_key = f"content:{url}"

            # Increment the access count
            redis_client.incr(count_key)

            # Check if content is cached
            cached_content = redis_client.get(content_key)
            if cached_content:
                return cached_content.decode('utf-8')

            # If not cached, call the original function
            content = func(url)

            # Cache the content with expiration
            redis_client.setex(content_key, expiration, content)

            return content
        return wrapper
    return decorator


@cache_and_track()
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/http://www.example.com"
    
    print("First call (not cached):")
    print(get_page(url)[:100])  # Print first 100 characters
    
    print("\nSecond call (should be cached):")
    print(get_page(url)[:100])  # Print first 100 characters
    
    print("\nAccess count:")
    redis_client = redis.Redis()
    print(redis_client.get(f"count:{url}").decode('utf-8'))
    
    print("\nWait 11 seconds for cache to expire...")
    import time
    time.sleep(11)
    
    print("\nThird call (cache should have expired):")
    print(get_page(url)[:100])  # Print first 100 characters
    
    print("\nFinal access count:")
    print(redis_client.get(f"count:{url}").decode('utf-8'))
