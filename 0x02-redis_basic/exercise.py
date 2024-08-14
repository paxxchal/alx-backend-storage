#!/usr/bin/env python3
"""
Cache module for storing and
retrieving data in Redis with method call counting.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments
        the call count and calls the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """A class that provides caching functionality using Redis."""

    def __init__(self):
        """
        Initialize the Cache with a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using
        the given key and optionally apply a conversion function.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]:
            The retrieved data, optionally converted.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string from Redis using the given key.

        Args:
            key (str): The key of the string to retrieve.

        Returns:
            Union[str, None]: The retrieved string
            or None if the key doesn't exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis using the given key.

        Args:
            key (str): The key of the integer to retrieve.

        Returns:
            Union[int, None]: The retrieved integer
            or None if the key doesn't exist.
        """
        return self.get(key, fn=int)
