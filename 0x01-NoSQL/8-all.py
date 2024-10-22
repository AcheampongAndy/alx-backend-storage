#!/usr/bin/env python3
""" list all docs """
from pymongo import MongoClient


def list_all(mongo_collection) -> list:
    """ Py function listing all documents in collection """
    listing = []

    for x in mongo_collection.find():
        listing.append(x)

    return listing
