#!/usr/bin/env python

from pymongo import MongoClient
import time
from datetime import datetime

def main():
    # Write some data
    write_client = MongoClient(host = 'localhost:27000', username = 'root', password = 'mongo', replicaset = 'repl-1')
    db = write_client.get_database("read_test")
    coll = db.get_collection("analytics")
    i = 0
    while (True):
        doc = { "name" : "test %s" % i, "ts" : datetime.now() }
        coll.insert_one(doc)
        time.sleep(0.5)
        if i % 10 == 0:
            print("Written %d" %i )
        i += 1

####
# Main
####
if __name__ == '__main__':
    main()
