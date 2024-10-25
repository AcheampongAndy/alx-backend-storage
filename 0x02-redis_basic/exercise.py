#!/usr/bin/env python3
"""
Cache module for basic Redis operations.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    A Cache class to interact with a Redis server for storing and retrieving data.
    """

    def __init__(self) -> None:
        """
        Initializes a new Cache instance, connecting to a Redis server.
        The Redis database is flushed upon initialization.
        """
        self._redis = radis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key for retrieving the stored data.
        """
        key = str(uuid.uuid4())
        self._radis.set(key, data)
        return key
