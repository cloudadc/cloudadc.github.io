#!/usr/bin/env python3

import pymongo
import datetime
import random
import demo_settings

def alter_model(collection):
    pipeline = [{'$sample': {'size': demo_settings.NUM_SAMPLING}}]
    docs = collection.aggregate(pipeline)
    for doc in docs:
            new_doc = add_newfields(doc["emp_no"])
            update_data(collection, new_doc)

def add_newfields(emp_no):
    # add new fields to employee document
    departments = ["Marketing", "Sales","Engineering", "Human Resources", "Finance", "Services", "Other"]
    titles = ["Director", "Manager","Senior Staff", "Staff", "Other"]
    hobbies = ["movies", "cycling", "singing", "running", "hiking", "photography", "reading", "sleeping"]
    base_birth_year = 1975
    employee={
            "emp_no": emp_no,
            "birth_date": datetime.datetime(int(base_birth_year + random.choice(range(15))),int(1 + random.choice(range(11))), int(1 + random.choice(range(28)))),
            "department" : random.choice(departments),
            "title" : random.choice(titles),
            "hobbies": []
            }

    for i in range(1 + int(1000 * random.random()) % 3) :
        employee["hobbies"].append(random.choice(hobbies))

    return employee

def update_data(collection, doc):
    #print("updating employee: ", doc["emp_no"])
    result = collection.update_one({"emp_no": doc["emp_no"]},
                                   {"$set": doc})
    return result


if __name__ == "__main__":
    try:
        conn = pymongo.MongoClient(demo_settings.URI_STRING)
        print("Connected to MongoDB")

        collection = conn.test.employees

        print("Adding fields to ", demo_settings.NUM_SAMPLING, " documents ...")
        alter_model(collection)

        print("Operation completed successfully!!!")

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
    conn.close()
