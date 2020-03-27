const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');

const user = encodeURIComponent('root');
const password = encodeURIComponent('mongo');
const authMechanism = 'DEFAULT';

const url = `mongodb://${user}:${password}@localhost:27017?authMechanism=${authMechanism}`;

const client = new MongoClient(url, {useNewUrlParser: true });

const dbName = 'test';
const collectionName = 'easy';

var doc2 = {
    "name": "Bob Brown",
    "balance": 492.45,
    "accountNo": 489275482,
    "accountType": 2,
    "phone": [ "555-3456325", "1800-mongodb" ],
    "address": {
       "building": "MongoDB HQ",
       "city": "NYC",
       "zip": 10036
    }
}

client.connect(function(err, client) {
  assert.equal(null, err);
  console.log("Connected correctly to server");

  const db = client.db(dbName);
  db.collection(collectionName).insertOne(doc2, function(err, r) {
    assert.equal(null, err);
    assert.equal(1, r.insertedCount);
    console.log("1 document inserted");
  });

  client.close();
});
