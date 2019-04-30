#!/usr/bin/env python

from pymongo import MongoClient
import time

def main():
    # Read docs		
    read_client = MongoClient(host = 'localhost:27000', 
                                      replicaset = 'repl-1',
                                      username = 'root', 
                                      password = 'mongo', 
                                      readPreference='secondary', 
                                      readPreferenceTags = ["use:analytics"])
    db = read_client.get_database("read_test")
    coll = db.get_collection("analytics")

    while (True):
        cur = coll.find().sort("ts", -1).limit(10)
        for doc in cur:
            pass
        time.sleep(0.2)


####
# Main
####
if __name__ == '__main__':
    main()
