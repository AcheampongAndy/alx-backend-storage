#!/usr/bin/env python3
""" 12-log_stats """

from pymongo import MongoClient

if __name__ == "__main__":
    # call mongoclient
    the_client = MongoClient('mongodb://127.0.0.1:27017')
    # access collection nginx
    the_collection = the_client.logs.nginx
    # 
    methods = {
        'GET': 0,
        'POST': 0,
        'PUT': 0,
        'PATCH': 0,
        'DELETE': 0
    }

    count = 0

    for key in the_collection.find():
        if 'method' in key:
            if key['method'] in methods:
                methods[key['method']] += 1

            if key['method'] == 'GET' and 'path' in key and key['path'] == '/status':
                count += 1

print("{0} logs".format(the_collection.count_documents({})))
print("Methods:")
print("\tmethod GET: {0}".format(methods['GET']))
print("\tmethod POST: {0}".format(methods['POST']))
print("\tmethod PUT: {0}".format(methods['PUT']))
print("\tmethod PATCH: {0}".format(methods['PATCH']))
print("\tmethod DELETE: {0}".format(methods['DELETE']))
print("{0} status check".format(count))
