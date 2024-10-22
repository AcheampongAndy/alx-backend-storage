#!/usr/bin/env python3
""" Py function returns school with specific topic """


def schools_by_topic(mongo_collection, topic: str):
    """ same thing I mentioned above"""
    entire_data = mongo_collection.find()
    the_school = []
    for key in entire_data:
        if 'topics' in key:
            if topic in key['topics']:
                the_school.append(key)

    return the_school
