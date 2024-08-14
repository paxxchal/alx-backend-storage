#!/usr/bin/env python3
"""
Cache module for interacting with Redis.
"""

import redis
import uuid
import functools
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments
        the count and calls the original method.
        """
        # Generate the Redis key using the method's qualified name
        key = f"{method.__qualname__}"
        # Increment the count in Redis
        self._redis.incr(key)
        # Call the original method
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache instance with
        a Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis and return the key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and optionally convert it using a callable.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A function
            to apply to the data before returning it.

        Returns:
            Optional[Union[str, bytes, int, float]]:
            The retrieved data, optionally converted by `fn`.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data as a UTF-8 string.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[str]: The retrieved data as
            a UTF-8 string, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data as an integer.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[int]: The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, int)
