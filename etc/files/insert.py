#!/usr/bin/env python
import random, time, pymongo
from datetime import datetime
from pprint import pprint

connection = pymongo.MongoClient('mongodb://root:mongo@localhost:27017/')
db = connection['bankdata']
db.companies.drop()
db.customers.drop()
seed_companies_amount = 10000
customers_amount = 50000
print('\nAdding company and customer records - may take about 30 seconds...\n')


#################
#
# COMPANIES
#
#################
ADJECTIVES = ['Best', 'Better', 'Big', 'Clear', 'Different', 'Early', 'Easy', 'Economic', 'Federal', 'Full', 'Good', 'Great', 'Hard', 'High', 'International', 'Large', 'Late', 'Long', 'Low', 'Major','National', 'New', 'Old', 'Public', 'Real', 'Recent', 'Right', 'Small', 'Social', 'Special', 'Strong', 'Sure', 'True', 'Whole', 'Young']
NOUNS = ['Cumulus', 'Stratus', 'Stratocumulus', 'Altocumulus', 'Nimbostratus', 'Altostratus', 'Cirrocumulus', 'Cirrostratus', 'Cirrus', 'Cumulonimbus', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Planet-Nine', 'Tornado', 'Hurricane', 'Cyclone', 'Waterspout', 'Monsoon', 'Downburst', 'Alligator', 'Alpaca', 'Ant', 'Antelope', 'Ape', 'Armadillo', 'Baboon', 'Badger', 'Bat', 'Bear', 'Beaver', 'Bee', 'Beetle', 'Buffalo', 'Butterfly', 'Camel', 'Carabao', 'Caribou', 'Cat', 'Cattle', 'Cheetah', 'Chimpanzee', 'Chinchilla', 'Cicada', 'Clam', 'Cockroach', 'Cod', 'Coyote', 'Crab', 'Crocodile', 'Crow', 'Deer', 'Dinosaur', 'Dog', 'Dolphin', 'Duck', 'Eel', 'Elephant', 'Elk', 'Ferret', 'Fish', 'Fly', 'Fox', 'Frog', 'Gerbil', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfish', 'Gorilla', 'Grasshopper', 'Hamster', 'Hare', 'Hedgehog', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Hound', 'Hyena', 'Impala', 'Insect', 'Jackal', 'Jellyfish', 'Kangaroo', 'Koala', 'Leopard', 'Lion', 'Lizard', 'Llama', 'Locust', 'Louse', 'Mallard', 'Mammoth', 'Manatee', 'Marten', 'Mink', 'Minnow', 'Mole', 'Monkey', 'Moose', 'Mosquito', 'Mouse', 'Mule', 'Muskrat', 'Otter', 'Ox', 'Oyster', 'Panda', 'Pig', 'Platypus', 'Porcupine', 'Pug', 'Rabbit', 'Raccoon', 'Reindeer', 'Rhinoceros', 'Salmon', 'Sardine', 'Scorpion', 'Seal', 'Serval', 'Shark', 'Sheep', 'Skunk', 'Snail', 'Snake', 'Spider', 'Squirrel', 'Swan', 'Termite', 'Tiger', 'Trout', 'Turtle', 'Walrus', 'Wasp', 'Weasel', 'Whale', 'Wolf', 'Wombat', 'Woodchuck', 'Worm', 'Yak', 'Yellowjacket', 'Zebra']
SUFFIXES = ['PLC', 'Ltd', 'GmbH', 'Pty', 'AG', 'SA', 'LLC', 'Corp', 'LLP', 'LP']

conpanies_num = 0

# Populate COMPANIES collection with RANDOM records
for count in range(seed_companies_amount): 
    inserted_id = ''

    # Hierarchy of parent companies can be 1 to 9 levels deep, randomly
    for position in range(random.randint(1,9)):
        inserted_id = db.companies.insert_one({                                
            'name': '%s %s %s' % (random.choice(ADJECTIVES), random.choice(NOUNS), random.choice(SUFFIXES)),
            'watch': True if (random.randint(1,9) == 1) else False,
            'part_of': inserted_id
        }).inserted_id

        conpanies_num +=1

# Populate COMPANIES collection with hierachy of FIXED KNOWN records
# Hierachy 1:
db.companies.insert_one({'_id': 'Antartic LLP', 'name': 'Antartic LLP', 'watch': True, 'part_of': ''})  # Has WATCH flag!
db.companies.insert_one({'_id': 'Indian GmbH', 'name': 'Indian GmbH', 'watch': False, 'part_of': 'Antartic LLP'})
db.companies.insert_one({'_id': 'Arctic PLC', 'name': 'Arctic PLC', 'watch': False, 'part_of': 'Indian GmbH'})
db.companies.insert_one({'_id': 'Pacific Co', 'name': 'Pacific Co', 'watch': False, 'part_of': 'Arctic PLC'})
db.companies.insert_one({'_id': 'Atlantic Ltd', 'name': 'Atlantic Ltd', 'watch': False, 'part_of': 'Pacific Co'})
# Hierachy 2:
db.companies.insert_one({'_id': 'Next Ventures GmbH', 'name': 'Next Ventures GmbH', 'watch': False, 'part_of': ''})
db.companies.insert_one({'_id': 'Browns Conglomerate Corp', 'name': 'Browns Conglomerate Corp', 'watch': False, 'part_of': 'Next Ventures GmbH'})
db.companies.insert_one({'_id': 'Lewis Group PLC', 'name': 'Lewis Group PLC', 'watch': False, 'part_of': 'Browns Conglomerate Corp'})
db.companies.insert_one({'_id': 'Smiths Ltd', 'name': 'Smiths Ltd', 'watch': False, 'part_of': 'Lewis Group PLC'})


print("%d company records added\n" % (conpanies_num + 9))


#################
#
# CUSTOMERS
#
#################
FIRSTNAMES = ['Mary', 'Patricia', 'Linda', 'Barbara', 'Elizabeth', 'Jennifer', 'Maria', 'Susan', 'Margaret', 'Dorothy', 'Lisa', 'Nancy', 'Karen', 'Betty', 'Helen', 'Sandra', 'Donna', 'Carol', 'Ruth', 'Sharon', 'Michelle', 'Laura', 'Sarah', 'Kimberly', 'Deborah', 'Jessica', 'Shirley', 'Cynthia', 'Angela', 'Melissa', 'Brenda', 'Amy', 'Anna', 'Rebecca', 'Virginia', 'Kathleen', 'Pamela', 'Martha', 'Debra', 'Amanda', 'Stephanie', 'Carolyn', 'Christine', 'Marie', 'Janet', 'Catherine', 'Frances', 'Ann', 'Joyce', 'Diane', 'Alice', 'Julie', 'Heather', 'Teresa', 'Doris', 'Gloria', 'Evelyn', 'Jean', 'Cheryl', 'Mildred', 'Katherine', 'Joan', 'Ashley', 'Judith', 'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas', 'Christopher', 'Daniel', 'Paul', 'Mark', 'Donald', 'George', 'Kenneth', 'Steven', 'Edward', 'Brian', 'Ronald', 'Anthony', 'Kevin', 'Jason', 'Matthew', 'Gary', 'Timothy', 'Jose', 'Larry', 'Jeffrey', 'Frank', 'Scott', 'Eric', 'Stephen', 'Andrew', 'Raymond', 'Gregory', 'Joshua', 'Jerry', 'Dennis', 'Walter', 'Patrick', 'Peter', 'Harold', 'Douglas', 'Henry', 'Carl', 'Arthur', 'Ryan', 'Roger', 'Joe', 'Juan', 'Jack', 'Albert', 'Jonathan', 'Justin', 'Terry', 'Gerald', 'Keith', 'Samuel', 'Willie', 'Ralph', 'Lawrence', 'Nicholas', 'Roy', 'Benjamin']
SURNAMES = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker', 'Hall', 'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams', 'Baker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Stewart', 'Sanchez', 'Morris', 'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres', 'Peterson', 'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Price', 'Bennett', 'Wood', 'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long', 'Patterson', 'Hughes', 'Flores', 'Washington', 'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant', 'Alexander', 'Russell', 'Griffin', 'Diaz', 'Hayes', 'Myers', 'Ford', 'Hamilton', 'Graham', 'Sullivan', 'Wallace', 'Woods', 'Cole', 'West', 'Jordan', 'Owens', 'Reynolds', 'Fisher', 'Ellis', 'Harrison', 'Gibson', 'Mcdonald', 'Cruz', 'Marshall', 'Ortiz', 'Gomez', 'Murray', 'Freeman', 'Wells', 'Webb', 'Simpson', 'Stevens', 'Tucker', 'Porter', 'Hunter', 'Hicks', 'Crawford', 'Henry', 'Boyd', 'Mason', 'Morales', 'Kennedy', 'Warren', 'Dixon', 'Ramos', 'Reyes', 'Burns', 'Gordon', 'Shaw', 'Holmes', 'Rice', 'Robertson', 'Hunt', 'Black', 'Daniels', 'Palmer', 'Mills', 'Nichols', 'Grant', 'Knight', 'Ferguson', 'Rose', 'Stone', 'Hawkins', 'Dunn', 'Perkins', 'Hudson', 'Spencer', 'Gardner', 'Stephens', 'Payne', 'Pierce', 'Berry', 'Matthews', 'Arnold', 'Wagner', 'Willis']

# Populate CUSTOMERS collection with RANDOM records
for count in range(customers_amount): 
    db.customers.insert_one({                                
        'firstname': random.choice(FIRSTNAMES),
        'lastname': random.choice(SURNAMES),
        'balance': random.randint(-9999,9999)
    })

# Populate CUSTOMERS collection with a FIXED KNOWN record
db.customers.insert_one({
    '_id': 123456, 
    'firstname': 'Mandy', 
    'lastname': 'Morrison', 
    'balance': 89788, 
    'pending_transactions': [
        {'amount': 6423, 'to_party': 'Atlantic Ltd'},
        {'amount': 7582, 'to_party': 'Lewis Group PLC'},
    ]
})

print("%d customer records added\n" % (customers_amount + 1))



