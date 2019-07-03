#!/usr/bin/env python3

import pymongo
from bson.json_util import dumps
import time
import random
import demo_settings

def read_data(collection, doc_id):
    # dictionary to be added in the database
    item = collection.find({"emp_no" : doc_id})
    return item


if __name__ == "__main__":
    try:
        conn=pymongo.MongoClient(demo_settings.URI_STRING)
        
        print("Microservice One - connected to MongoDB\n")
        
        collection = conn.test.employees
        
        ids = collection.distinct("emp_no")
        
        while True:
            print("Running employees report (microservice one)")
            for i in range(5):                
                item = collection.find({"emp_no" : random.choice(ids)}, {"_id": 0, "first_name": 1, "last_name": 1, "gender": 1})
                print(dumps(item))
          
            print("\n...")
            time.sleep(5)

        print("Operation completed successfully!!!")
          
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
    conn.close()    
