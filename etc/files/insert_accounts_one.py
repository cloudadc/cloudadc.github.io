#!/usr/bin/env python
import random
import time
from datetime import datetime
import pymongo


record_amount = 1000000
connection = pymongo.MongoClient('mongodb://root:root123@localhost:27017/')
db = connection['bankdata']
db.customers.drop()





## THIS IS ALL ABOUT FAST TO WORK WITH DATA

# Create first main record
##  this is object in python
main_record = { 
    'cust_id': '32727191229',
    'name': 'Jon Mac',
    'branch': 'EDI-1',
    'manager': 'Barry Mongo',
    'rank_level': 3,
    'customer_since': datetime.strptime('1989-02-22 13:43:55','%Y-%m-%d %H:%M:%S'),
    'contact_tel_nums': ['0131 123 456', '0724 822 4878'],
    'accounts': [ 
        { 'acc_num': '05627331',
          'account_type': 'current',
          'account_subtype': 'classic',
          'overdraft_limit': 1000,
          'balance': -354 },
        { 'acc_num': '38673499',
          'account_type': 'save',
          'account_subtype': 'super-saver',
          'interest_pct_rate': 2.5,
          'balance': 4691 }
    ]
}

#This is what i need to insert my object 1:1 c

db.customers.insert(main_record);
#This is what i need to insert my object 1:1







## lets generate a ramdom set of users and accounts

# Create a load of randomly generated records
##
FIRST_NAMES = ['Patricia', 'Paco', 'Ruben', 'Gustavo', 'Mandy', 'Sandy', 'Randy', 'Candy', 'Bambi']
LAST_NAMES = ['Botin', 'Molero', 'Terceno', 'Loewe', 'Barrett', 'Saunders', 'Reid', 'Whittington-Smythe', 'Parker-Tweed']
BRANCHES = ['EDI-1', 'EDI-1', 'LON-1', 'LON-2', 'LON-3', 'MAN-1', 'MAN-2', 'MAN-3', 'NEW-1']
MANAGERS = ['Sally Smith', 'Wendy Watson', 'Nick Dickens', 'Harvey Schmarvey', 'Penelope Pitstop']

collection=db.customers



for count in xrange(record_amount):


        single_digit = random.randint(1,9)

        new_record = {
            'cust_id': str(random.randint(10000000000,77777777777)),
            'name': '%s %s' % (random.choice(FIRST_NAMES), random.choice(LAST_NAMES)),
            'branch': random.choice(BRANCHES),
            'manager': random.choice(MANAGERS),
            'rank_level': random.randint(1,5),
            'customer_since': datetime.strptime('200%d-02-22 1%d:4%d:5%d' % (single_digit, single_digit,single_digit, single_digit),'%Y-%m-%d %H:%M:%S'),
            'contact_tel_nums': ['01%d' % random.randint(11111111,88888888), '07%d' % random.randint(11111111,88888888)]
        }

        # Give each either or both a current account and a savings account
        choices = random.randint(1,3)
        new_record['accounts'] = []

        if (choices in [1,3]):
            new_record['accounts'].append({
                'acc_num': str(random.randint(10000000,44444444)),
                'account_type': 'current',
                'account_subtype': 'classic',
                'overdraft_limit': random.randint(0,9999),
                'balance': random.randint(-4999,4999)
            })

        if (choices in [2,3]):
            new_record['accounts'].append({
                'acc_num': str(random.randint(55555555,88888888)),
                'account_type': 'savings',
                'account_subtype': 'super-saver',
                'interest_pct_rate': random.uniform(1.1, 4.9),
                'balance': random.randint(0,99999)
            })

        collection.insert(new_record)




#
# Summary
#
print "%d records inserted" % record_amount
print
