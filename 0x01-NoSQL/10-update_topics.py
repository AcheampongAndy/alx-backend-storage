#!/usr/bin/env python3
""" update all topics of doc """

from typing import List

from pymongo import MongoClient


def update_topics(mongo_collection, name: str, topics: List[str]):
    """ Updates all topics of school doc based on school name """

    new_collection = mongo_collection.update_one({"name": name},{"$set":{"topics": topics}})

    return new_collection
