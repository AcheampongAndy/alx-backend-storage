#!/usr/bin/env python3
""" Return new _id """
from pymongo import MongoClient

list_all = __import__('8-all').list_all

def insert_school(mongo_collection, **kwargs):
    """ Insert new doc in collection based on kwargs """
    new_collection = mongo_collection.insert_one(kwargs)

    new_id = new_collection.inserted_id

    return new_id
