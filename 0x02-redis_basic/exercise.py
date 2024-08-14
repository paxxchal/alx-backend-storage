#!/usr/bin/env python3
"""
Cache module for interacting with Redis.
"""

import redis
import uuid
from typing import Union


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
