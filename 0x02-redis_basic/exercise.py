#!/usr/bin/env python3
"""
Cache module for basic Redis operations.
"""

import redis
import uuid
from typing import Union, Optional, Callable

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

    def get(self, key: str, 
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves data from Redis and applies an optional conversion function.
        
        Args:
            key (str): The key to retrieve the data from Redis.
            fn (Optional[Callable]): A function to convert the data into the desired format.
        
        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted.
        """
        value = self._radis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis, decoding from bytes if necessary.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            The data converted to a string
        """
        value = self._radis.get(key)
        value = value.decode('utf-8')
        return value

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from Redis, converting from bytes if necessary.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            The data converted to an integer
        """
        value = self._radis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0

        return value

