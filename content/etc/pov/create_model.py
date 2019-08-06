#!/usr/bin/env python3

import pymongo
import datetime
import random
import demo_settings

def create_documents(collection):
    collection.drop()
    collection.create_index([("emp_no", pymongo.ASCENDING) ], unique=True)
    generate_data(collection, demo_settings.NUM_ITEMS)


def generate_data(collection, items):
    for n in range(items):
        doc = create_model(n)
        write_data(collection,doc)

def create_model(item):
    # create a new employee document
    female_names = ["Ana","Elizabeth", "Helen", "Diana", "Maria", "Patricia", "Teresa"]
    male_names = ["Alex", "Bart" ,"Charles", "John", "Michael", "Paul", "Peter"]
    first_names ={"F" : female_names, "M": male_names}
    last_names = ["Anderson", "Brown","Davis", "Jones", "Johnson", "Smith", "Williams"]
    gender = random.choice(["F","M"])
    base_emp_no = 1000
    base_salary = 40000
    base_hire_year = 2000
    employee={
            "emp_no": int(base_emp_no + item),
            "first_name": random.choice(first_names[gender]),
            "last_name": random.choice(last_names),
            "gender": gender,
            "annual_salary": base_salary + round(random.random() * base_salary),
            "hire_date": datetime.datetime(int(base_hire_year + random.choice(range(17))),
                                            int(1 + (random.choice(range(11)))),
                                            int(1 + (random.choice(range(28)))))
            }

    return employee

def write_data(collection, doc):
    #print("inserting employee: ", doc["emp_no"])
    result = collection.insert_one(doc)
    return result


if __name__ == "__main__":
    try:
        conn = pymongo.MongoClient(demo_settings.URI_STRING)
        print("Connected to MongoDB")

        collection = conn.test.employees

        print("Creating new ", demo_settings.NUM_ITEMS ," documents ...")
        create_documents(collection)

        print("Operation completed successfully!!!")

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)
    conn.close()
