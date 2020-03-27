#!/usr/bin/env python

from pymongo import MongoClient
import time

def main():
    # Read docs		
    read_client = MongoClient(host = 'localhost:27000', 
                                      replicaset = 'repl-1',
                                      username = 'root', 
                                      password = 'mongo', 
                                      readPreference='secondary')
    db = read_client.get_database("bankdata")
    coll = db.get_collection("customers")

    while (True):
        cur = coll.find().sort("cust_id", -1).limit(10)
        for doc in cur:
            pass
        time.sleep(0.2)


####
# Main
####
if __name__ == '__main__':
    main()
