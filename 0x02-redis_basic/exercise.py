#!/usr/bin/env python3
"""
Cache module for basic Redis operations.
"""

import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of calls to a method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper for decorated function."""
        self._redis.incr(key)
        return method(self, *args, **kwds)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper for the decorated function."""
        input_data = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input_data)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper

def replay(fn: Callable):
    """display the history of calls of a particular function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} times:".format(function_name, value))
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """
    A Cache class to interact with a Redis server for storing and retrieving data.
    """

    def __init__(self) -> None:
        """
        Initializes a new Cache instance, connecting to a Redis server.
        The Redis database is flushed upon initialization.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key for retrieving the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
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
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string from Redis, decoding from bytes if necessary.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            str: The data converted to a string.
        """
        value = self._redis.get(key)
        if value is None:
            return ""
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer from Redis, converting from bytes if necessary.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            int: The data converted to an integer.
        """
        value = self._redis.get(key)
        if value is None:
            return 0
        try:
            return int(value.decode('utf-8'))
        except ValueError:
            return 0
